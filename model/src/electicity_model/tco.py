"""TCO calculations for heavy-duty vehicle scenarios.

Per-mile / per-km cost of ownership across powertrain types: FCEV, BEV, diesel ICE.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import DIESEL_LHV_KWH_PER_L, H2_LHV_KWH_PER_KG

__all__ = ["TruckTcoInputs", "truck_tco_per_km"]


@dataclass(frozen=True, slots=True)
class TruckTcoInputs:
    """Inputs to the TCO calculation. All currency values in USD per the units listed."""

    capex_truck: float
    annual_km: float
    energy_kwh_per_km: float
    powertrain_efficiency: float
    fuel_unit_cost: float
    fuel_unit: str
    h2_lhv_kwh_per_kg: float = H2_LHV_KWH_PER_KG
    diesel_lhv_kwh_per_l: float = DIESEL_LHV_KWH_PER_L
    annual_maintenance: float = 0.0
    insurance_yr: float = 0.0
    lifetime_years: int = 10
    discount_rate: float = 0.08
    residual_value: float = 0.0


def truck_tco_per_km(i: TruckTcoInputs) -> dict[str, float]:
    """Return dict with total $/km and component breakdown."""
    annual_kwh_at_wheels = i.energy_kwh_per_km * i.annual_km
    annual_fuel_kwh_in = annual_kwh_at_wheels / i.powertrain_efficiency

    if i.fuel_unit == "kwh_electric":
        annual_fuel_cost = annual_fuel_kwh_in / 1000.0 * i.fuel_unit_cost  # $/MWh input
    elif i.fuel_unit == "kg_h2":
        annual_kg_h2 = annual_fuel_kwh_in / i.h2_lhv_kwh_per_kg
        annual_fuel_cost = annual_kg_h2 * i.fuel_unit_cost
    elif i.fuel_unit == "l_diesel":
        annual_l_diesel = annual_fuel_kwh_in / i.diesel_lhv_kwh_per_l
        annual_fuel_cost = annual_l_diesel * i.fuel_unit_cost
    else:
        raise ValueError(f"unknown fuel_unit {i.fuel_unit!r}")

    r = i.discount_rate
    pv_costs = i.capex_truck
    pv_km = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        pv_costs += (annual_fuel_cost + i.annual_maintenance + i.insurance_yr) * df
        pv_km += i.annual_km * df
    pv_costs -= i.residual_value / (1.0 + r) ** i.lifetime_years
    total_per_km = pv_costs / pv_km

    return {
        "tco_per_km": total_per_km,
        "fuel_per_km": annual_fuel_cost / i.annual_km,
        "capex_per_km_amortised": (i.capex_truck - i.residual_value / (1.0 + r) ** i.lifetime_years) / pv_km,
        "annual_fuel_cost": annual_fuel_cost,
    }
