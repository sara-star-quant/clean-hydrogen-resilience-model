"""Scenario builders. Compose tech params + scenario YAML into LCOE/TCO results.

Policy toggles:
  - 45V: applies to US scenarios when policy_45v is True. Tier-1 $3/kg.
  - ETS/RFNBO: EU scenarios; modelled via grid-import surcharge.

Shock toggles (supply-chain resilience): see supply.py. When shock != "bau",
parameters are perturbed before LCOE/TCO computation.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, cast

import yaml

from .constants import HOURS_PER_YEAR
from .lcoe import LcoeInputs, lcoe, lcoh_pem
from .paths import DATA_DIR
from .supply import apply_shock
from .tco import TruckTcoInputs, truck_tco_per_km
from .tech import Param, ParamSet, RawParamsYaml, RawScenariosYaml, load_params, load_scenarios
from .tech_registry import district_annual_opex, district_capex

__all__ = [
    "DistrictResult",
    "TruckResult",
    "evaluate_district",
    "evaluate_truck",
    "clear_caches",
]


@lru_cache(maxsize=1)
def _raw_params_cached() -> RawParamsYaml:
    with (DATA_DIR / "tech_params.yaml").open() as f:
        return cast(RawParamsYaml, yaml.safe_load(f))


def _materialise(shocked: RawParamsYaml) -> dict[str, ParamSet]:
    out: dict[str, ParamSet] = {}
    for tech, fields in shocked.items():
        parsed: dict[str, Param] = {}
        for fname, body in fields.items():
            parsed[fname] = Param(
                value=float(body["value"]),
                range_low=float(body["range_low"]),
                range_high=float(body["range_high"]),
                unit=str(body["unit"]),
                year=int(body["year"]),
                source=str(body["source"]),
                notes=str(body.get("notes", "")),
            )
        out[tech] = ParamSet(name=tech, fields=parsed)
    return out


@lru_cache(maxsize=16)
def _params_with_shock(shock: str) -> dict[str, ParamSet]:
    """Load raw YAML, apply shock, materialise as ParamSet dict. Cached per shock name."""
    if shock == "bau":
        return load_params()
    raw = _raw_params_cached()
    shocked = apply_shock(raw, shock)
    return _materialise(shocked)


@lru_cache(maxsize=1)
def _scenarios_cached() -> RawScenariosYaml:
    return load_scenarios()


def clear_caches() -> None:
    """Reset all module-level caches. Use in tests that mutate YAML on disk."""
    _raw_params_cached.cache_clear()
    _params_with_shock.cache_clear()
    _scenarios_cached.cache_clear()


@dataclass(frozen=True, slots=True)
class DistrictResult:
    """Output of a district-scenario evaluation: economics plus capex breakdown."""

    name: str
    capex_total_usd: float
    annual_opex_usd: float
    lcoe_per_mwh: float
    lcoh_per_kg: float
    fits_36m_envelope: bool
    capex_breakdown: dict[str, float]


@dataclass(frozen=True, slots=True)
class TruckResult:
    """Output of a truck-scenario evaluation: per-km TCO and fuel cost."""

    name: str
    powertrain: str
    tco_per_km: float
    fuel_per_km: float
    annual_fuel_cost: float


# Track B stage 2 removed the legacy if/elif paths after the registry equivalence test
# proved byte-identical output. The registry-driven `district_capex` and
# `district_annual_opex` (in tech_registry.py) are now the only implementation.

_district_capex = district_capex
_district_annual_opex = district_annual_opex


def evaluate_district(
    scenario_name: str,
    *,
    discount_rate: float | None = None,
    params: dict[str, ParamSet] | None = None,
    scenarios: dict[str, dict[str, Any]] | None = None,
    envelope_usd: float = 36_000_000,
    shock: str = "bau",
) -> DistrictResult:
    """Evaluate a district scenario and return capex breakdown plus LCOE/LCOH.

    The shock kwarg perturbs tech_params before computation per supply.PROFILES; "bau" is
    identity. The envelope_usd kwarg sets the budget cap used for the fits/does-not-fit
    flag in the returned record.
    """
    if params is None:
        params = _params_with_shock(shock)
    scenarios = scenarios or _scenarios_cached()
    s = scenarios[scenario_name]

    if discount_rate is None:
        # Use private-investor discount as the headline LCOE so numbers compare to
        # commercial reality, not subsidised public-money LCOE.
        discount_rate = params["financial"].v("discount_rate_private")

    breakdown = _district_capex(s, params)
    capex_total = sum(breakdown.values())
    annual_opex = _district_annual_opex(s, params)

    annual_load_mwh = s["load_mw"] * HOURS_PER_YEAR
    annual_fuel_cost = 0.0
    if s.get("grid_import_allowed"):
        # Coarse: 20% of load covered from grid as backup; H2 covers nighttime/long-duration.
        grid_share = 0.20
        annual_fuel_cost = grid_share * annual_load_mwh * s["grid_import_price_per_mwh"]

    inputs = LcoeInputs(
        capex_total=capex_total,
        opex_yr=annual_opex,
        fuel_yr=annual_fuel_cost,
        energy_mwh_yr=annual_load_mwh,
        lifetime_years=25,
        discount_rate=discount_rate,
    )
    district_lcoe = lcoe(inputs)

    credit = 0.0
    if s.get("policy_45v"):
        credit = params["policy"].v("ira_45v_credit_per_kg")

    lcoh = lcoh_pem(
        electrolyzer_capex_per_kw=params[s.get("electrolyzer_type", "pem_electrolyzer")].v("capex_per_kw"),
        electrolyzer_kw=s["electrolyzer_mw"] * 1000,
        electrolyzer_opex_per_kw_yr=params[s.get("electrolyzer_type", "pem_electrolyzer")].v("opex_per_kw_yr"),
        electricity_price_per_mwh=s.get("grid_import_price_per_mwh", 80) * 0.4,
        # 0.4 multiplier reflects that most input is curtailed-renewable, not grid-import
        efficiency_lhv=params[s.get("electrolyzer_type", "pem_electrolyzer")].v("efficiency_lhv"),
        capacity_factor=0.45,
        lifetime_years=20,
        discount_rate=discount_rate,
        ira_45v_credit_per_kg=credit,
    )

    return DistrictResult(
        name=scenario_name,
        capex_total_usd=capex_total,
        annual_opex_usd=annual_opex,
        lcoe_per_mwh=district_lcoe,
        lcoh_per_kg=lcoh,
        fits_36m_envelope=capex_total <= envelope_usd,
        capex_breakdown=breakdown,
    )


def evaluate_truck(
    scenario_name: str,
    *,
    discount_rate: float = 0.08,
    h2_price_per_kg: float | None = None,
    params: dict[str, ParamSet] | None = None,
    scenarios: dict[str, dict[str, Any]] | None = None,
    shock: str = "bau",
) -> TruckResult:
    """Evaluate a vehicle scenario and return per-km TCO + fuel cost.

    The h2_price_per_kg kwarg overrides the scenario's central H2 price. The shock kwarg
    follows the same supply.PROFILES contract as evaluate_district.
    """
    if params is None:
        params = _params_with_shock(shock)
    scenarios = scenarios or _scenarios_cached()
    s = scenarios[scenario_name]
    pt = s["powertrain"]

    annual_km = params["reference_loads"].v("truck_class8_annual_km")
    energy_kwh_per_km = params["reference_loads"].v("truck_class8_kwh_per_km")

    if pt == "fcev":
        h2_price = h2_price_per_kg if h2_price_per_kg is not None else s["h2_price_per_kg_central"]
        inputs = TruckTcoInputs(
            capex_truck=425_000,
            annual_km=annual_km,
            energy_kwh_per_km=energy_kwh_per_km,
            powertrain_efficiency=0.55,
            fuel_unit_cost=h2_price,
            fuel_unit="kg_h2",
            annual_maintenance=18_000,
            insurance_yr=10_000,
            lifetime_years=10,
            discount_rate=discount_rate,
            residual_value=30_000,
        )
    elif pt == "bev":
        inputs = TruckTcoInputs(
            capex_truck=400_000,
            annual_km=annual_km,
            energy_kwh_per_km=energy_kwh_per_km,
            powertrain_efficiency=0.85,
            fuel_unit_cost=s["electricity_price_per_mwh"],
            fuel_unit="kwh_electric",
            annual_maintenance=14_000,
            insurance_yr=10_000,
            lifetime_years=10,
            discount_rate=discount_rate,
            residual_value=40_000,
        )
    elif pt == "ice_diesel":
        inputs = TruckTcoInputs(
            capex_truck=180_000,
            annual_km=annual_km,
            energy_kwh_per_km=energy_kwh_per_km,
            powertrain_efficiency=0.40,
            fuel_unit_cost=s["diesel_price_per_l"],
            fuel_unit="l_diesel",
            annual_maintenance=22_000,
            insurance_yr=10_000,
            lifetime_years=10,
            discount_rate=discount_rate,
            residual_value=20_000,
        )
    else:
        raise ValueError(f"unsupported powertrain {pt}")

    out = truck_tco_per_km(inputs)
    return TruckResult(
        name=scenario_name,
        powertrain=pt,
        tco_per_km=out["tco_per_km"],
        fuel_per_km=out["fuel_per_km"],
        annual_fuel_cost=out["annual_fuel_cost"],
    )
