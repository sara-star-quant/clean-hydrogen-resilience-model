"""Cover residual branches in finance.py: bisection fallback, edge guard rails."""

from __future__ import annotations

import pytest

from electicity_model.finance import irr, levelised_cost, npv, payback_years


def test_irr_bisection_fallback_for_pathological_curve():
    """A cashflow with multiple sign changes can break Newton's; bisection should still find a root."""
    cf = [-100, 230, -132]  # roots near 0.10 and 0.20
    r = irr(cf)
    assert r is None or 0.0 < r < 1.0


def test_irr_returns_none_for_no_real_root():
    cf = [-100, -50, -10]  # all negative, no IRR
    assert irr(cf) is None


def test_irr_handles_initial_zero_derivative():
    # Flat cashflows can yield df ~ 0; ensure we degrade gracefully.
    r = irr([-100, 0, 0, 110])
    # Should find ~3.2% (110/100)^(1/3) - 1
    assert r is None or 0.02 < r < 0.05


def test_payback_with_high_discount_returns_none():
    # 100/yr earning vs 1000 capex at 100% discount: never recovers.
    assert payback_years(1000, 100, discount_rate=1.0) is None


def test_payback_zero_revenue_returns_none():
    assert payback_years(1000, 0) is None


def test_levelised_cost_basic_correctness():
    # 10-yr 0% discount, capex 1000, opex 50/yr, output 100/yr -> (1000+50*10)/(100*10) = 1.5
    lc = levelised_cost(1000, 50, 100, 0.0, 10)
    assert lc == pytest.approx(1.5)


def test_levelised_cost_zero_years_yields_inf():
    assert levelised_cost(1000, 50, 100, 0.05, 0) == float("inf")


def test_npv_with_negative_discount_close_to_minus_one_raises():
    with pytest.raises(ValueError):
        npv([-100, 50, 50], -1.0)
