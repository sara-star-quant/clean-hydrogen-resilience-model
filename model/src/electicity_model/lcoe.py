"""LCOE / LCOH / LCOS, discounted-cash-flow form following the IEA/IRENA convention.

LCOE = sum_t [(CapEx_t + OpEx_t + Fuel_t) / (1+r)^t]
       /  sum_t [E_t / (1+r)^t]

CapEx is booked at t=0 unless a construction profile is passed in.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import H2_LHV_KWH_PER_KG, HOURS_PER_YEAR

__all__ = [
    "LcoeInputs",
    "lcoe",
    "lcoh_pem",
    "lcos",
    "capacity_cost_to_capex",
    "annual_energy_mwh",
]


@dataclass(frozen=True, slots=True)
class LcoeInputs:
    """Inputs to the LCOE calculation. All flows in USD; energy in MWh/yr."""

    capex_total: float
    opex_yr: float
    fuel_yr: float
    energy_mwh_yr: float
    lifetime_years: int
    discount_rate: float


def lcoe(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def capacity_cost_to_capex(capex_per_kw: float, capacity_kw: float) -> float:
    """Convert per-kW capex and a capacity into total capex USD."""
    return capex_per_kw * capacity_kw


def annual_energy_mwh(capacity_kw: float, capacity_factor: float) -> float:
    """Return MWh/year produced by a unit at a given capacity factor."""
    return capacity_kw * capacity_factor * HOURS_PER_YEAR / 1000.0


def lcoh_pem(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def lcos(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv
