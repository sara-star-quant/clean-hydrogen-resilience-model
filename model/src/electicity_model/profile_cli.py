"""Profiler helper. Run via: python -m electicity_model.profile_cli <subcommand>.

Wraps cProfile around hot paths so users can find their own bottlenecks before reporting.
"""

from __future__ import annotations

import argparse
import cProfile
import pstats
import sys
from io import StringIO

from .scenarios import evaluate_district, evaluate_truck
from .sensitivity import monte_carlo_npv, tornado_lcoh


def _profile(label: str, fn, n: int = 100) -> None:
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(n):
        fn()
    pr.disable()
    out = StringIO()
    pstats.Stats(pr, stream=out).strip_dirs().sort_stats("cumulative").print_stats(20)
    print(f"=== {label} ({n} iterations) ===")
    print(out.getvalue())


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="electicity_model.profile_cli")
    p.add_argument("--what", default="all",
                   choices=["all", "district", "truck", "tornado", "mc"])
    p.add_argument("--n", type=int, default=100)
    args = p.parse_args(argv)

    if args.what in ("all", "district"):
        _profile("evaluate_district",
                 lambda: evaluate_district("district_solar_h2_inland"),
                 n=args.n)
    if args.what in ("all", "truck"):
        _profile("evaluate_truck",
                 lambda: evaluate_truck("car_fcev_class8"),
                 n=args.n)
    if args.what in ("all", "tornado"):
        _profile("tornado_lcoh", lambda: tornado_lcoh(), n=10)
    if args.what in ("all", "mc"):
        _profile("monte_carlo_npv",
                 lambda: monte_carlo_npv(
                     capex=27_000_000,
                     annual_revenue_mean=5_500_000, annual_revenue_std=600_000,
                     annual_opex_mean=1_300_000, annual_opex_std=200_000,
                     discount_rate=0.09, lifetime_years=25, n_runs=1000,
                 ),
                 n=5)
    return 0


if __name__ == "__main__":
    sys.exit(main())
