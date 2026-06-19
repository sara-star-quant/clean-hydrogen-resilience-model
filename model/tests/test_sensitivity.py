"""Sensitivity / Monte Carlo coverage."""

from __future__ import annotations

import pytest

from electicity_model.sensitivity import monte_carlo_npv, tornado_lcoh


def test_tornado_lcoh_ranks_by_impact():
    results = tornado_lcoh()
    spreads = [abs(r.high_output - r.low_output) for r in results]
    assert spreads == sorted(spreads, reverse=True)


def test_tornado_lcoh_45v_shifts_base():
    bare = tornado_lcoh(ira_45v_credit_per_kg=0.0)
    creditted = tornado_lcoh(ira_45v_credit_per_kg=3.0)
    assert creditted[0].base_output < bare[0].base_output


def test_tornado_lcoh_returns_5_drivers():
    results = tornado_lcoh()
    assert len(results) == 5
    names = {r.driver for r in results}
    assert any("capex" in n.lower() for n in names)


def test_monte_carlo_basic_shape():
    out = monte_carlo_npv(
        capex=10_000_000,
        annual_revenue_mean=2_000_000, annual_revenue_std=200_000,
        annual_opex_mean=500_000, annual_opex_std=50_000,
        discount_rate=0.08, lifetime_years=15, n_runs=500, seed=1,
    )
    assert set(out) == {"p05", "p50", "p95", "mean", "prob_negative"}
    assert out["p05"] <= out["p50"] <= out["p95"]
    assert 0.0 <= out["prob_negative"] <= 1.0


def test_monte_carlo_seed_reproducibility():
    a = monte_carlo_npv(
        capex=10_000_000,
        annual_revenue_mean=2_000_000, annual_revenue_std=200_000,
        annual_opex_mean=500_000, annual_opex_std=50_000,
        discount_rate=0.08, lifetime_years=15, n_runs=500, seed=42,
    )
    b = monte_carlo_npv(
        capex=10_000_000,
        annual_revenue_mean=2_000_000, annual_revenue_std=200_000,
        annual_opex_mean=500_000, annual_opex_std=50_000,
        discount_rate=0.08, lifetime_years=15, n_runs=500, seed=42,
    )
    assert a == b


def test_monte_carlo_negative_revenue_handled():
    # Revenue mean very low; opex high; expect prob_negative high.
    out = monte_carlo_npv(
        capex=20_000_000,
        annual_revenue_mean=500_000, annual_revenue_std=100_000,
        annual_opex_mean=400_000, annual_opex_std=50_000,
        discount_rate=0.10, lifetime_years=10, n_runs=500, seed=7,
    )
    assert out["prob_negative"] > 0.95
