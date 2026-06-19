"""Financial primitives — including pathological / edge cases."""

from __future__ import annotations

import math

import pytest

from electicity_model.finance import (
    annuity_factor,
    cashflow_series,
    irr,
    levelised_cost,
    npv,
    payback_years,
)


def test_npv_zero_discount_is_sum():
    assert npv([-100, 50, 50, 50], 0.0) == pytest.approx(50.0)


def test_npv_handles_negative_only():
    assert npv([-100, -50], 0.10) == pytest.approx(-100 - 50 / 1.10)


def test_npv_rejects_invalid_discount():
    with pytest.raises(ValueError):
        npv([1, 2, 3], -1.5)


def test_irr_simple_case():
    # An investment of -100 returning 110 in one year => IRR = 10%.
    r = irr([-100, 110])
    assert r == pytest.approx(0.10, rel=1e-3)


def test_irr_no_sign_change_returns_none():
    assert irr([100, 50, 50]) is None
    assert irr([-100, -50, -25]) is None


def test_irr_steady_annuity():
    # CF: -1000 then +200 for 10 years. IRR around 15.1%.
    cf = [-1000] + [200] * 10
    r = irr(cf)
    assert r is not None
    assert 0.14 < r < 0.16


def test_irr_short_series():
    assert irr([100]) is None
    assert irr([]) is None


def test_payback_simple():
    assert payback_years(1000, 100) == pytest.approx(10.0)


def test_payback_zero_capex_is_zero():
    assert payback_years(0, 100) == pytest.approx(0.0)


def test_payback_negative_cashflow_returns_none():
    assert payback_years(1000, -50) is None
    assert payback_years(1000, 0) is None


def test_payback_with_discount_is_longer_than_simple():
    simple = payback_years(1000, 100)
    discounted = payback_years(1000, 100, discount_rate=0.08)
    assert discounted is not None and discounted > simple


def test_payback_never_recovered():
    # Discount rate so high recovery never happens within 200 years.
    assert payback_years(10_000, 100, discount_rate=0.50) is None


def test_annuity_factor_zero_discount_is_years():
    assert annuity_factor(0.0, 10) == pytest.approx(10.0)


def test_annuity_factor_known_value():
    # 5% for 10 years should be 7.7217.
    assert annuity_factor(0.05, 10) == pytest.approx(7.7217, abs=0.001)


def test_levelised_cost_zero_output_raises():
    with pytest.raises(ValueError):
        levelised_cost(100, 10, 0, 0.07, 25)


def test_cashflow_series_length():
    cf = cashflow_series(capex=1000, annual_revenue=200, annual_opex=50, years=10)
    assert len(cf) == 11  # capex + 10 years


def test_cashflow_series_with_salvage():
    cf = cashflow_series(capex=1000, annual_revenue=200, annual_opex=50, years=5, salvage=300)
    assert cf[-1] == pytest.approx(150 + 300)


def test_npv_irr_consistency():
    cf = cashflow_series(capex=1000, annual_revenue=200, annual_opex=50, years=10)
    r = irr(cf)
    assert r is not None
    assert npv(cf, r) == pytest.approx(0.0, abs=1.0)


def test_irr_zero_years_returns_none():
    assert irr([-100]) is None
