"""Extended performance tests: realistic loads, batched calls, regression baselines.

Marked perf so they can be skipped on slow CI with `pytest -m 'not perf'`.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from electicity_model.scenarios import (
    clear_caches,
    evaluate_district,
    evaluate_truck,
)
from electicity_model.sensitivity import monte_carlo_npv, tornado_lcoh
from electicity_model.regions import rank_regions

pytestmark = pytest.mark.perf

BASELINE_PATH = Path(__file__).parent / "_perf_baseline.json"


def _load_baseline() -> dict:
    if BASELINE_PATH.exists():
        return json.loads(BASELINE_PATH.read_text())
    return {}


def _save_baseline(baseline: dict) -> None:
    BASELINE_PATH.write_text(json.dumps(baseline, indent=2, sort_keys=True))


def _measure(fn, n: int = 100) -> float:
    start = time.perf_counter()
    for _ in range(n):
        fn()
    return (time.perf_counter() - start) / n


def test_evaluate_district_with_warm_cache_under_2ms():
    """First call warms the YAML cache; subsequent calls hit the LRU path."""
    clear_caches()
    evaluate_district("district_solar_h2_inland")  # warm
    avg = _measure(lambda: evaluate_district("district_solar_h2_inland"), n=200)
    assert avg < 2e-3, f"warm-cache evaluate_district took {avg*1000:.2f}ms (budget 2ms)"


def test_evaluate_district_cold_cache_first_call_under_100ms():
    clear_caches()
    start = time.perf_counter()
    evaluate_district("district_solar_h2_inland")
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1, f"cold-cache first call took {elapsed*1000:.1f}ms (budget 100ms)"


def test_batched_1000_district_evaluations_under_2s():
    """Realistic load: report regen + playground driving 1000 evaluations."""
    evaluate_district("district_solar_h2_inland")  # warm
    start = time.perf_counter()
    for _ in range(1000):
        evaluate_district("district_solar_h2_inland")
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"1000 evaluations took {elapsed:.2f}s (budget 2s)"


def test_shock_cycling_does_not_thrash_cache():
    """Iterating across shock profiles should still be fast (LRU at 16 covers all)."""
    profiles = ["bau", "ir_shortage", "pt_shortage", "li_shortage",
                "china_decoupling", "triple_squeeze", "western_only",
                "regional_autarky", "maritime_blockade"]
    # Warm
    for p in profiles:
        evaluate_district("district_solar_h2_inland", shock=p)
    avg = _measure(
        lambda: [evaluate_district("district_solar_h2_inland", shock=p) for p in profiles][0],
        n=50,
    )
    # 9 shocks per call x 50 calls. Each call warm should be ~2ms, so 9 x 2ms = 18ms budget per outer iteration.
    assert avg < 0.05, f"shock-cycling avg {avg*1000:.1f}ms exceeds 50ms"


def test_evaluate_truck_warm_cache_under_2ms():
    clear_caches()
    evaluate_truck("car_fcev_class8")  # warm
    avg = _measure(lambda: evaluate_truck("car_fcev_class8"), n=200)
    assert avg < 2e-3, f"warm-cache evaluate_truck took {avg*1000:.2f}ms (budget 2ms)"


def test_region_ranking_under_5ms():
    avg = _measure(lambda: rank_regions(jurisdiction="EU"), n=500)
    assert avg < 5e-3, f"rank_regions took {avg*1000:.2f}ms (budget 5ms)"


def test_monte_carlo_50000_under_8s():
    start = time.perf_counter()
    monte_carlo_npv(
        capex=27_000_000,
        annual_revenue_mean=5_500_000, annual_revenue_std=600_000,
        annual_opex_mean=1_300_000, annual_opex_std=200_000,
        discount_rate=0.09, lifetime_years=25, n_runs=50_000,
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 8.0, f"MC 50000 took {elapsed:.2f}s (budget 8s)"


def test_tornado_with_45v_credit_under_100ms():
    start = time.perf_counter()
    tornado_lcoh(ira_45v_credit_per_kg=3.0)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1, f"tornado(45V) took {elapsed*1000:.1f}ms"


# --------- Regression: fail if metric drifts > 2x baseline ---------

def _check_or_baseline(metric: str, value: float, *, tolerance: float = 2.0) -> None:
    baseline = _load_baseline()
    prior = baseline.get(metric)
    if prior is None:
        baseline[metric] = value
        _save_baseline(baseline)
        pytest.skip(f"baseline for {metric} initialised at {value:.6f}")
    else:
        ratio = value / prior if prior > 0 else float("inf")
        assert ratio < tolerance, (
            f"{metric}: {value:.6f}s is {ratio:.2f}x baseline {prior:.6f}s "
            f"(tolerance {tolerance}x). Investigate or update baseline."
        )


@pytest.mark.regression
def test_regression_evaluate_district_warm():
    evaluate_district("district_solar_h2_inland")
    avg = _measure(lambda: evaluate_district("district_solar_h2_inland"), n=200)
    _check_or_baseline("evaluate_district_warm_avg", avg)


@pytest.mark.regression
def test_regression_tornado_lcoh():
    start = time.perf_counter()
    tornado_lcoh()
    _check_or_baseline("tornado_lcoh_total", time.perf_counter() - start)


@pytest.mark.regression
def test_regression_rank_regions():
    avg = _measure(lambda: rank_regions(), n=200)
    _check_or_baseline("rank_regions_avg", avg)
