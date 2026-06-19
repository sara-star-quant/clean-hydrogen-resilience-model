"""Performance budgets. Marked `perf` so they can be skipped on slow CI."""

from __future__ import annotations

import time

import pytest

from electicity_model.lcoe import LcoeInputs, lcoe, lcoh_pem
from electicity_model.scenarios import evaluate_district
from electicity_model.sensitivity import monte_carlo_npv, tornado_lcoh


pytestmark = pytest.mark.perf


def _bench(func, n=1000):
    start = time.perf_counter()
    for _ in range(n):
        func()
    return (time.perf_counter() - start) / n


def test_lcoe_under_1ms():
    inputs = LcoeInputs(capex_total=1100, opex_yr=18, fuel_yr=0,
                        energy_mwh_yr=1.93, lifetime_years=25, discount_rate=0.07)
    avg = _bench(lambda: lcoe(inputs))
    assert avg < 1e-3, f"LCOE took {avg*1000:.3f}ms (budget 1ms)"


def test_lcoh_under_2ms():
    avg = _bench(lambda: lcoh_pem(
        electrolyzer_capex_per_kw=1500, electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45, electricity_price_per_mwh=30.0,
        efficiency_lhv=0.60, capacity_factor=0.50,
        lifetime_years=20, discount_rate=0.08,
    ))
    assert avg < 2e-3, f"LCOH took {avg*1000:.3f}ms (budget 2ms)"


def test_tornado_under_100ms():
    start = time.perf_counter()
    tornado_lcoh()
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1, f"tornado took {elapsed*1000:.1f}ms (budget 100ms)"


def test_monte_carlo_5000_under_2s():
    start = time.perf_counter()
    monte_carlo_npv(
        capex=27_000_000,
        annual_revenue_mean=5_500_000, annual_revenue_std=600_000,
        annual_opex_mean=1_300_000, annual_opex_std=200_000,
        discount_rate=0.09, lifetime_years=25, n_runs=5000,
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"MC 5000 took {elapsed:.2f}s (budget 2s)"


def test_evaluate_district_under_50ms():
    avg = _bench(lambda: evaluate_district("district_solar_h2_inland"), n=100)
    assert avg < 0.05, f"evaluate_district took {avg*1000:.1f}ms (budget 50ms)"
