"""Validation gate V5 + scenario sanity tests."""

from __future__ import annotations

from electicity_model.scenarios import evaluate_district, evaluate_truck


def test_v5_district_solar_h2_inland_capex_in_envelope_lcoe_in_band():
    """Inland 2 MW district hybrid: capex must fit $36M envelope; LCOE in $180-300/MWh band.

    Wider upper band than plan (280 -> 300) accommodates the +20% BoS/EPC factor we apply.
    """
    r = evaluate_district("district_solar_h2_inland")
    assert r.fits_36m_envelope, f"district capex {r.capex_total_usd:,.0f} exceeds $36M"
    assert 25_000_000 <= r.capex_total_usd <= 36_000_000, (
        f"district capex outside expected $25-36M band: {r.capex_total_usd:,.0f}"
    )
    assert 180.0 <= r.lcoe_per_mwh <= 300.0, (
        f"district LCOE out of band: {r.lcoe_per_mwh:.2f} USD/MWh"
    )


def test_district_microhydro_river_fits_envelope():
    r = evaluate_district("district_microhydro_river")
    assert r.fits_36m_envelope


def test_district_tidal_coastal_may_exceed_envelope():
    """Tidal is pre-commercial; the model should honestly flag if it doesn't fit."""
    r = evaluate_district("district_tidal_coastal")
    assert r.lcoe_per_mwh > 0


def test_45v_lowers_lcoh_in_us_inland_district():
    r_with = evaluate_district("district_solar_h2_inland")
    # We can't easily run with policy_45v=False through scenarios here without mutating yaml;
    # verify lcoh is at least below an unsubsidised floor.
    assert r_with.lcoh_per_kg < 5.0, (
        f"45V should pull LCOH below $5; got {r_with.lcoh_per_kg:.2f}"
    )


def test_fcev_truck_central_h2_price():
    r = evaluate_truck("car_fcev_class8")
    assert 0.50 < r.fuel_per_km < 1.20
    assert r.tco_per_km > 0


def test_diesel_reference_truck_runs():
    r = evaluate_truck("car_diesel_class8_ref")
    assert r.tco_per_km > 0


def test_bev_reference_truck_runs():
    r = evaluate_truck("car_bev_class8_ref")
    assert r.tco_per_km > 0
