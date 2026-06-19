"""Financial primitives. NPV / IRR / payback. Pure stdlib."""

from __future__ import annotations

import math
from typing import Sequence


def npv(cashflows: Sequence[float], discount_rate: float) -> float:
    """Net present value. cashflows[0] is t=0 (typically -capex)."""
    if discount_rate <= -1.0:
        raise ValueError("discount_rate must be > -1")
    return sum(cf / (1.0 + discount_rate) ** t for t, cf in enumerate(cashflows))


def irr(
    cashflows: Sequence[float],
    *,
    guess: float = 0.10,
    tol: float = 1e-6,
    max_iter: int = 200,
) -> float | None:
    """Internal rate of return. Newton's method with bisection fallback.

    Returns None if no real IRR exists in (-0.99, 10.0).
    """
    if not cashflows or len(cashflows) < 2:
        return None
    if all(cf >= 0 for cf in cashflows) or all(cf <= 0 for cf in cashflows):
        return None  # No sign change => no IRR.

    # Newton's method.
    r = guess
    for _ in range(max_iter):
        f = sum(cf / (1.0 + r) ** t for t, cf in enumerate(cashflows))
        df = sum(-t * cf / (1.0 + r) ** (t + 1) for t, cf in enumerate(cashflows))
        if df == 0:
            break
        r_new = r - f / df
        if r_new <= -0.999:
            break
        if abs(r_new - r) < tol:
            return r_new
        r = r_new

    # Bisection fallback over (-0.99, 10).
    lo, hi = -0.99, 10.0
    f_lo = sum(cf / (1.0 + lo) ** t for t, cf in enumerate(cashflows))
    f_hi = sum(cf / (1.0 + hi) ** t for t, cf in enumerate(cashflows))
    if f_lo * f_hi > 0:
        return None
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        f_mid = sum(cf / (1.0 + mid) ** t for t, cf in enumerate(cashflows))
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return (lo + hi) / 2.0


def payback_years(
    capex: float,
    annual_net_cashflow: float,
    *,
    discount_rate: float = 0.0,
) -> float | None:
    """Simple or discounted payback. Returns None if never recovered."""
    if capex <= 0:
        return 0.0
    if annual_net_cashflow <= 0:
        return None
    if discount_rate <= 0:
        return capex / annual_net_cashflow
    cumulative = 0.0
    t = 0
    while cumulative < capex and t < 200:
        t += 1
        cumulative += annual_net_cashflow / (1.0 + discount_rate) ** t
    if cumulative < capex:
        return None
    # Linear interpolation within the last year.
    prev_cum = cumulative - annual_net_cashflow / (1.0 + discount_rate) ** t
    frac = (capex - prev_cum) / (cumulative - prev_cum)
    return (t - 1) + frac


def annuity_factor(discount_rate: float, years: int) -> float:
    """Standard PV-of-annuity factor: (1 - (1+r)^-n) / r."""
    if years <= 0:
        return 0.0
    if discount_rate == 0:
        return float(years)
    return (1.0 - (1.0 + discount_rate) ** -years) / discount_rate


def levelised_cost(
    capex: float,
    annual_opex: float,
    annual_output: float,
    discount_rate: float,
    years: int,
) -> float:
    """Generic levelised cost (USD per output unit). Convenience wrapper."""
    if annual_output <= 0:
        raise ValueError("annual_output must be positive")
    af = annuity_factor(discount_rate, years)
    return (capex + annual_opex * af) / (annual_output * af) if af > 0 else math.inf


def cashflow_series(
    *,
    capex: float,
    annual_revenue: float,
    annual_opex: float,
    years: int,
    salvage: float = 0.0,
) -> list[float]:
    """Build a [-capex, ANCF, ANCF, ..., ANCF + salvage] series."""
    if years <= 0:
        return [-capex]
    cf = [-capex]
    for _ in range(years - 1):
        cf.append(annual_revenue - annual_opex)
    cf.append(annual_revenue - annual_opex + salvage)
    return cf
