"""Tech registry for the district capex/opex computation.

Replaces the long if/elif chain in scenarios.py with a declarative table of TechSpec rows.
Adding a new technology becomes a single registry append plus a tech_params.yaml entry.

Math contract preserved from the legacy code:
- Three capex bases: per_kW, per_kWh, per_kg.
- BoS/EPC factor (0.20) is applied to the running base_sum AFTER all techs are added.
- Premium line items (on_site_spares_premium, control_premium) are scenario-level
  multipliers applied to base_sum AFTER BoS, listed last in the breakdown.
- Truthy semantics: scenario.get("foo") is falsy for missing keys AND for 0; both fall
  through.
- Stack-replacement reserve in opex follows the legacy formula: 0.5 * capex amortised
  over an effective stack life derived from declared stack_lifetime_hours and an assumed
  capacity factor of 0.45.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from .constants import HOURS_PER_YEAR
from .tech import ParamSet


class CapexBasis(Enum):
    """Three cost bases used in the district capex breakdown."""

    PER_KW = "per_kw"     # capacity in MW * 1000 * capex_per_kw
    PER_KWH = "per_kwh"   # capacity in MWh * 1000 * capex_per_kwh
    PER_KG = "per_kg"     # capacity in kg * capex_per_kg


@dataclass(frozen=True, slots=True)
class TechSpec:
    """One row in the district registry. Resolves to one entry in the capex breakdown.

    `params_key` is either a static string referencing a top-level YAML key, or None when
    the key is dynamic and resolved via `params_key_scenario_field`.
    `params_key_scenario_field` lets a scenario pick which parameter set to use
    (electrolyzer_type, fuel_cell_type, battery_chemistry).
    """

    scenario_key: str
    label: str
    params_key: str | None
    basis: CapexBasis
    has_opex: bool = True
    params_key_scenario_field: str | None = None
    params_key_default: str | None = None
    # opex_extra receives capacity, the resolved ParamSet, and the full params dict so it
    # can reach across to a different params key when the legacy formula does (e.g. fuel
    # cell opex computed against pem_fuel_cell_stationary regardless of chemistry).
    opex_extra: Callable[[float, ParamSet, dict[str, ParamSet]], float] | None = None


@dataclass(frozen=True, slots=True)
class PremiumSpec:
    """Scenario-level multiplier on base_sum after BoS, e.g. on_site_spares_premium."""

    scenario_key: str
    label: str


def _resolve_params_key(scenario: dict[str, Any], spec: TechSpec) -> str:
    """Pick the YAML key for this tech in this scenario."""
    if spec.params_key is not None:
        return spec.params_key
    if spec.params_key_scenario_field is None or spec.params_key_default is None:
        raise ValueError(
            f"TechSpec({spec.scenario_key}) has no static or dynamic params_key"
        )
    return scenario.get(spec.params_key_scenario_field, spec.params_key_default)


def _capex_value(capacity: float, ps: ParamSet, basis: CapexBasis) -> float:
    if basis is CapexBasis.PER_KW:
        return capacity * 1000 * ps.v("capex_per_kw")
    if basis is CapexBasis.PER_KWH:
        return capacity * 1000 * ps.v("capex_per_kwh")
    if basis is CapexBasis.PER_KG:
        return capacity * ps.v("capex_per_kg")
    raise ValueError(f"unknown CapexBasis {basis!r}")


def _electrolyzer_opex_extra(
    capacity_mw: float, ps: ParamSet, _all_params: dict[str, ParamSet]
) -> float:
    """Electrolyzer stack-replacement reserve, against the chosen chemistry."""
    ekw = capacity_mw * 1000
    stack_life_yr = ps.v("stack_lifetime_hours") / (HOURS_PER_YEAR * 0.45)
    return 0.5 * ekw * ps.v("capex_per_kw") / stack_life_yr


def _fuel_cell_opex_extra(
    capacity_mw: float, _ps: ParamSet, all_params: dict[str, ParamSet]
) -> float:
    """Fuel-cell base opex plus stack reserve, both against pem_fuel_cell_stationary.

    Note: this preserves the legacy formula which uses PEMFC opex/capex regardless of the
    chosen fuel-cell chemistry. A follow-up commit fixes this and updates the test.
    """
    fckw = capacity_mw * 1000
    pemfc = all_params["pem_fuel_cell_stationary"]
    base_opex = fckw * pemfc.v("opex_per_kw_yr")
    stack_reserve = 0.5 * fckw * pemfc.v("capex_per_kw") / 9.0
    return base_opex + stack_reserve


DISTRICT_TECHS: list[TechSpec] = [
    TechSpec("solar_pv_mwp", "solar_pv", "solar_pv_utility", CapexBasis.PER_KW),
    TechSpec("micro_hydro_mw", "micro_hydro", "micro_hydro_run_of_river", CapexBasis.PER_KW),
    TechSpec("tidal_mw", "tidal", "tidal_stream", CapexBasis.PER_KW),
    TechSpec("smr_nuclear_mw", "smr_nuclear", "smr_nuclear", CapexBasis.PER_KW, has_opex=False),
    TechSpec("micro_reactor_mw", "micro_reactor", "micro_reactor", CapexBasis.PER_KW, has_opex=False),
    TechSpec("geothermal_egs_mw", "geothermal_egs", "geothermal_egs", CapexBasis.PER_KW, has_opex=False),
    TechSpec("biomass_backup_mw", "biomass_chp", "biomass_chp", CapexBasis.PER_KW, has_opex=False),
    TechSpec(
        "electrolyzer_mw",
        "electrolyzer",
        params_key=None,
        basis=CapexBasis.PER_KW,
        params_key_scenario_field="electrolyzer_type",
        params_key_default="pem_electrolyzer",
        opex_extra=_electrolyzer_opex_extra,
    ),
    TechSpec(
        "fuel_cell_mw",
        "fuel_cell",
        params_key=None,
        basis=CapexBasis.PER_KW,
        params_key_scenario_field="fuel_cell_type",
        params_key_default="pem_fuel_cell_stationary",
        # has_opex=False because base opex is computed inside opex_extra (against PEMFC).
        has_opex=False,
        opex_extra=_fuel_cell_opex_extra,
    ),
    TechSpec(
        "h2_storage_kg",
        "h2_storage",
        params_key="h2_storage_buffer_district",
        basis=CapexBasis.PER_KG,
        has_opex=False,
    ),
    TechSpec(
        "battery_buffer_mwh",
        "battery",
        params_key=None,
        basis=CapexBasis.PER_KWH,
        has_opex=False,
        params_key_scenario_field="battery_chemistry",
        params_key_default="li_ion_battery_grid",
    ),
]


DISTRICT_PREMIUMS: list[PremiumSpec] = [
    PremiumSpec("on_site_spares_premium", "on_site_spares"),
    PremiumSpec("control_premium", "zta_zte_controls"),
]


BOS_FACTOR: float = 0.20


def district_capex(
    scenario: dict[str, Any], params: dict[str, ParamSet]
) -> dict[str, float]:
    """Registry-driven district capex breakdown. See module docstring for the math contract."""
    breakdown: dict[str, float] = {}
    for spec in DISTRICT_TECHS:
        capacity = scenario.get(spec.scenario_key)
        if not capacity:
            continue
        params_key = _resolve_params_key(scenario, spec)
        breakdown[spec.label] = _capex_value(capacity, params[params_key], spec.basis)
    base_sum = sum(breakdown.values())
    breakdown["bos_epc_interconnect"] = BOS_FACTOR * base_sum
    for premium in DISTRICT_PREMIUMS:
        mult = scenario.get(premium.scenario_key)
        if mult:
            breakdown[premium.label] = mult * base_sum
    return breakdown


def district_annual_opex(
    scenario: dict[str, Any], params: dict[str, ParamSet]
) -> float:
    """Registry-driven district opex (fixed O&M plus stack-replacement reserves)."""
    opex = 0.0
    for spec in DISTRICT_TECHS:
        capacity = scenario.get(spec.scenario_key)
        if not capacity:
            continue
        params_key = _resolve_params_key(scenario, spec)
        ps = params[params_key]
        if spec.has_opex:
            if spec.basis is CapexBasis.PER_KW:
                opex += capacity * 1000 * ps.v("opex_per_kw_yr")
            elif spec.basis is CapexBasis.PER_KWH:
                opex += capacity * 1000 * ps.v("opex_per_kwh_yr")
            elif spec.basis is CapexBasis.PER_KG:
                opex += capacity * ps.v("opex_per_kg_yr")
        if spec.opex_extra is not None:
            opex += spec.opex_extra(capacity, ps, params)
    return opex
