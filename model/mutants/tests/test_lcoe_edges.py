"""LCOE / LCOH / LCOS edge-case + error-path tests."""

from __future__ import annotations

import math

import pytest

from electicity_model.lcoe import LcoeInputs, lcoe, lcoh_pem, lcos


def _solar_inputs(**overrides):
    base = dict(capex_total=1100, opex_yr=18, fuel_yr=0,
                energy_mwh_yr=1.93, lifetime_years=25, discount_rate=0.07)
    base.update(overrides)
    return LcoeInputs(**base)


def test_zero_energy_raises():
    with pytest.raises(ValueError, match="positive"):
        lcoe(_solar_inputs(energy_mwh_yr=0))


def test_zero_lifetime_raises():
    with pytest.raises(ValueError, match="positive"):
        lcoe(_solar_inputs(lifetime_years=0))


def test_negative_lifetime_raises():
    with pytest.raises(ValueError, match="positive"):
        lcoe(_solar_inputs(lifetime_years=-5))


def test_lifetime_one_does_not_blow_up():
    r = lcoe(_solar_inputs(lifetime_years=1))
    assert math.isfinite(r) and r > 0


def test_zero_discount_rate_well_defined():
    r = lcoe(_solar_inputs(discount_rate=0.0))
    assert math.isfinite(r) and r > 0


def test_zero_capex_lcoe_is_pure_opex():
    r = lcoe(_solar_inputs(capex_total=0, opex_yr=10, lifetime_years=10, discount_rate=0.0,
                           energy_mwh_yr=1.0))
    assert r == pytest.approx(10.0)


def test_lcoh_handles_full_credit_yielding_zero_or_negative():
    # Massive 45V credit yields net-zero/negative LCOH.
    r = lcoh_pem(
        electrolyzer_capex_per_kw=1500, electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45, electricity_price_per_mwh=30.0,
        efficiency_lhv=0.60, capacity_factor=0.50,
        lifetime_years=20, discount_rate=0.08,
        ira_45v_credit_per_kg=10.0,
    )
    assert r < 0


def test_lcoh_efficiency_one_is_finite():
    r = lcoh_pem(
        electrolyzer_capex_per_kw=1500, electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45, electricity_price_per_mwh=30.0,
        efficiency_lhv=1.0, capacity_factor=0.50,
        lifetime_years=20, discount_rate=0.08,
    )
    assert math.isfinite(r) and r > 0


def test_lcos_zero_cycles_yields_inf_or_div0():
    # Zero cycles ⇒ zero output ⇒ division leads to inf or ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        lcos(
            capex_per_kwh=130, capacity_kwh=100_000,
            capex_per_kw=1800, capacity_kw=10_000,
            opex_per_kw_yr=25, cycles_per_year=0,
            roundtrip_efficiency=0.78,
            charge_electricity_price_per_mwh=30.0,
            lifetime_years=50, discount_rate=0.07,
        )


def test_long_lifetime_50yr_completes():
    r = lcoe(_solar_inputs(lifetime_years=50))
    assert math.isfinite(r) and r > 0
