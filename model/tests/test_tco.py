"""Validation gate V4 — Class 8 FCEV TCO sanity bounds.

We do not claim a ±15% match to a specific NACFE/DOE number here without that number
in hand; instead we assert the per-mile fuel cost is in a defensible band at given H2
prices. Tighter pinning is added once the user supplies the NACFE reference figure to
match.
"""

from __future__ import annotations

import pytest

from electicity_model.tco import TruckTcoInputs, truck_tco_per_km

KM_PER_MILE = 1.609344


def _fcev_inputs(h2_price: float) -> TruckTcoInputs:
    return TruckTcoInputs(
        capex_truck=425_000,            # FCEV Class 8, low-volume present cost
        annual_km=160_000,
        energy_kwh_per_km=1.6,
        powertrain_efficiency=0.55,     # H2 LHV in -> wheels (incl FC + drivetrain)
        fuel_unit_cost=h2_price,
        fuel_unit="kg_h2",
        annual_maintenance=18_000,
        insurance_yr=10_000,
        lifetime_years=10,
        discount_rate=0.08,
        residual_value=30_000,
    )


@pytest.mark.parametrize(
    "h2_price,fuel_per_mile_low,fuel_per_mile_high",
    [
        # Bands consistent with FCEV powertrain efficiency 0.55 LHV-to-wheels
        # at 1.6 kWh/km road load. DOE H2@Scale stretch targets sit at the lower
        # edge once efficiency improves to ~0.60 and H2 reaches ~$4/kg.
        (4.0, 0.45, 0.65),
        (6.0, 0.70, 0.95),
        (9.0, 1.10, 1.40),
    ],
)
def test_v4_fcev_class8_fuel_cost_per_mile_band(h2_price, fuel_per_mile_low, fuel_per_mile_high):
    out = truck_tco_per_km(_fcev_inputs(h2_price))
    fuel_per_mile = out["fuel_per_km"] * KM_PER_MILE
    assert fuel_per_mile_low <= fuel_per_mile <= fuel_per_mile_high, (
        f"FCEV @ ${h2_price}/kg fuel cost out of band: ${fuel_per_mile:.2f}/mi"
    )


def test_v4_total_tco_above_diesel_floor_when_h2_expensive():
    """Sanity: FCEV TCO at $9/kg H2 must be above diesel TCO at $4/gal-equivalent."""
    fcev = truck_tco_per_km(_fcev_inputs(9.0))
    diesel = truck_tco_per_km(
        TruckTcoInputs(
            capex_truck=180_000,
            annual_km=160_000,
            energy_kwh_per_km=1.6,
            powertrain_efficiency=0.40,
            fuel_unit_cost=1.05,
            fuel_unit="l_diesel",
            annual_maintenance=22_000,
            insurance_yr=10_000,
            lifetime_years=10,
            discount_rate=0.08,
            residual_value=20_000,
        )
    )
    assert fcev["tco_per_km"] > diesel["tco_per_km"], (
        f"FCEV @ $9/kg should be more expensive than diesel; "
        f"got {fcev['tco_per_km']:.3f} vs {diesel['tco_per_km']:.3f}"
    )
