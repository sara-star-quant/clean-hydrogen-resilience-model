"""Property-style monotonicity invariants. Hand-rolled generator (no hypothesis dep)."""

from __future__ import annotations

import pytest

from electicity_model.lcoe import LcoeInputs, lcoe, lcoh_pem


# Hand-curated parameter grid (boundary + central + extreme).
CAPEX_GRID = [100, 500, 1100, 2400, 5000]
OPEX_GRID = [0, 10, 25, 50, 100]
CF_GRID = [0.10, 0.20, 0.40, 0.65, 0.95]
LIFE_GRID = [5, 15, 25, 40]
RATE_GRID = [0.03, 0.07, 0.10]


def _base(**overrides):
    base = dict(capex_total=1100, opex_yr=18, fuel_yr=0,
                energy_mwh_yr=1.93, lifetime_years=25, discount_rate=0.07)
    base.update(overrides)
    return LcoeInputs(**base)


@pytest.mark.parametrize("low,high", list(zip(CAPEX_GRID, CAPEX_GRID[1:])))
def test_lcoe_monotone_in_capex(low, high):
    a = lcoe(_base(capex_total=low))
    b = lcoe(_base(capex_total=high))
    assert b > a


@pytest.mark.parametrize("low,high", list(zip(OPEX_GRID, OPEX_GRID[1:])))
def test_lcoe_monotone_in_opex(low, high):
    a = lcoe(_base(opex_yr=low))
    b = lcoe(_base(opex_yr=high))
    assert b > a


@pytest.mark.parametrize("low,high", list(zip(CF_GRID, CF_GRID[1:])))
def test_lcoe_monotone_decreasing_in_capacity_factor(low, high):
    # Higher CF -> more energy -> lower LCOE.
    a = lcoe(_base(energy_mwh_yr=low * 8.76))
    b = lcoe(_base(energy_mwh_yr=high * 8.76))
    assert b < a


def test_lcoe_monotone_decreasing_in_lifetime_when_discount_positive():
    a = lcoe(_base(lifetime_years=10, discount_rate=0.07))
    b = lcoe(_base(lifetime_years=30, discount_rate=0.07))
    assert b < a


def test_lcoh_with_credit_strictly_less_than_without():
    base = dict(
        electrolyzer_capex_per_kw=1500, electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45, electricity_price_per_mwh=30.0,
        efficiency_lhv=0.60, capacity_factor=0.50,
        lifetime_years=20, discount_rate=0.08,
    )
    a = lcoh_pem(**base, ira_45v_credit_per_kg=0.0)
    b = lcoh_pem(**base, ira_45v_credit_per_kg=3.0)
    assert b == pytest.approx(a - 3.0)


@pytest.mark.parametrize("e_low,e_high", [(0.40, 0.60), (0.55, 0.70)])
def test_lcoh_monotone_decreasing_in_efficiency(e_low, e_high):
    base = dict(
        electrolyzer_capex_per_kw=1500, electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45, electricity_price_per_mwh=30.0,
        capacity_factor=0.50, lifetime_years=20, discount_rate=0.08,
    )
    a = lcoh_pem(**base, efficiency_lhv=e_low)
    b = lcoh_pem(**base, efficiency_lhv=e_high)
    assert b < a


@pytest.mark.parametrize("p_low,p_high", [(15, 30), (30, 60), (60, 120)])
def test_lcoh_monotone_increasing_in_electricity_price(p_low, p_high):
    base = dict(
        electrolyzer_capex_per_kw=1500, electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45, efficiency_lhv=0.60,
        capacity_factor=0.50, lifetime_years=20, discount_rate=0.08,
    )
    a = lcoh_pem(**base, electricity_price_per_mwh=p_low)
    b = lcoh_pem(**base, electricity_price_per_mwh=p_high)
    assert b > a
