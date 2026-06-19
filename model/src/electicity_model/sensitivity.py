"""Sensitivity analysis: tornado on top drivers and Monte Carlo NPV."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .lcoe import lcoh_pem

__all__ = ["TornadoResult", "tornado_lcoh", "monte_carlo_npv"]


@dataclass(frozen=True, slots=True)
class TornadoResult:
    """One row of a tornado: driver name with low/high inputs and resulting outputs."""
    driver: str  # display name of the driver (e.g. "Capacity factor")
    low_value: float
    high_value: float
    low_output: float
    high_output: float
    base_output: float


def tornado_lcoh(
    *,
    base_capex_per_kw: float = 1500,
    base_electricity_per_mwh: float = 30,
    base_capacity_factor: float = 0.50,
    base_efficiency: float = 0.62,
    base_lifetime: int = 20,
    base_discount: float = 0.08,
    ira_45v_credit_per_kg: float = 0.0,
) -> list[TornadoResult]:
    """One-at-a-time sensitivity on LCOH drivers. Returns list ranked by impact."""

    def f(**overrides: float) -> float:
        kw: dict[str, float | int] = {
            "electrolyzer_capex_per_kw": base_capex_per_kw,
            "electrolyzer_kw": 1.0,
            "electrolyzer_opex_per_kw_yr": 45,
            "electricity_price_per_mwh": base_electricity_per_mwh,
            "efficiency_lhv": base_efficiency,
            "capacity_factor": base_capacity_factor,
            "lifetime_years": base_lifetime,
            "discount_rate": base_discount,
            "ira_45v_credit_per_kg": ira_45v_credit_per_kg,
        }
        kw.update(overrides)
        return lcoh_pem(
            electrolyzer_capex_per_kw=float(kw["electrolyzer_capex_per_kw"]),
            electrolyzer_kw=float(kw["electrolyzer_kw"]),
            electrolyzer_opex_per_kw_yr=float(kw["electrolyzer_opex_per_kw_yr"]),
            electricity_price_per_mwh=float(kw["electricity_price_per_mwh"]),
            efficiency_lhv=float(kw["efficiency_lhv"]),
            capacity_factor=float(kw["capacity_factor"]),
            lifetime_years=int(kw["lifetime_years"]),
            discount_rate=float(kw["discount_rate"]),
            ira_45v_credit_per_kg=float(kw["ira_45v_credit_per_kg"]),
        )

    base = f()
    drivers: list[tuple[str, dict[str, float], dict[str, float]]] = [
        ("Electrolyzer capex (USD/kW)",
            {"electrolyzer_capex_per_kw": 800}, {"electrolyzer_capex_per_kw": 2400}),
        ("Electricity price (USD/MWh)",
            {"electricity_price_per_mwh": 15}, {"electricity_price_per_mwh": 60}),
        ("Capacity factor",
            {"capacity_factor": 0.30}, {"capacity_factor": 0.70}),
        ("Stack efficiency (LHV)",
            {"efficiency_lhv": 0.55}, {"efficiency_lhv": 0.70}),
        ("Discount rate",
            {"discount_rate": 0.05}, {"discount_rate": 0.12}),
    ]
    out: list[TornadoResult] = []
    for name, lo_kw, hi_kw in drivers:
        out.append(TornadoResult(
            driver=name,
            low_value=next(iter(lo_kw.values())),
            high_value=next(iter(hi_kw.values())),
            low_output=f(**lo_kw),
            high_output=f(**hi_kw),
            base_output=base,
        ))
    out.sort(key=lambda r: abs(r.high_output - r.low_output), reverse=True)
    return out


def monte_carlo_npv(
    *,
    capex: float,
    annual_revenue_mean: float,
    annual_revenue_std: float,
    annual_opex_mean: float,
    annual_opex_std: float,
    discount_rate: float,
    lifetime_years: int,
    n_runs: int = 5000,
    seed: int = 42,
) -> dict[str, float]:
    """Triangular-input Monte Carlo over revenue/opex; returns NPV percentiles."""
    rng = random.Random(seed)
    npvs: list[float] = []
    for _ in range(n_runs):
        rev = rng.gauss(annual_revenue_mean, annual_revenue_std)
        opex = max(0.0, rng.gauss(annual_opex_mean, annual_opex_std))
        npv = -capex
        for t in range(1, lifetime_years + 1):
            npv += (rev - opex) / (1.0 + discount_rate) ** t
        npvs.append(npv)
    npvs.sort()
    n = len(npvs)
    return {
        "p05": npvs[int(0.05 * n)],
        "p50": npvs[int(0.50 * n)],
        "p95": npvs[int(0.95 * n)],
        "mean": sum(npvs) / n,
        "prob_negative": sum(1 for x in npvs if x < 0) / n,
    }
