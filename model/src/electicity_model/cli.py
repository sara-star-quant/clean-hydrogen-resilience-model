"""argparse CLI: car / district / render-all / summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .render import render_all, render_summary_json
from .scenarios import evaluate_district, evaluate_truck


def _car(args: argparse.Namespace) -> int:
    r = evaluate_truck(
        args.scenario,
        h2_price_per_kg=args.h2_price,
        discount_rate=args.discount_rate,
    )
    print(f"scenario:         {r.name}")
    print(f"powertrain:       {r.powertrain}")
    print(f"TCO:              ${r.tco_per_km:.3f}/km  (${r.tco_per_km * 1.609344:.3f}/mi)")
    print(f"Fuel cost:        ${r.fuel_per_km:.3f}/km")
    print(f"Annual fuel cost: ${r.annual_fuel_cost:,.0f}")
    return 0


def _district(args: argparse.Namespace) -> int:
    r = evaluate_district(
        args.scenario,
        envelope_usd=args.envelope * 1_000_000,
        shock=args.shock,
    )
    print(f"scenario:         {r.name}")
    print(f"shock profile:    {args.shock}")
    print(f"CapEx total:      ${r.capex_total_usd / 1e6:,.2f}M")
    print(f"Fits ${args.envelope}M envelope: {'yes' if r.fits_36m_envelope else 'NO'}")
    print(f"LCOE:             ${r.lcoe_per_mwh:.1f}/MWh")
    print(f"LCOH (system):    ${r.lcoh_per_kg:.2f}/kg")
    print("CapEx breakdown:")
    for k, v in r.capex_breakdown.items():
        print(f"  {k:<24} ${v / 1e6:>7.2f}M")
    return 0


def _shock(args: argparse.Namespace) -> int:
    from .supply import PROFILES, shock_summary
    if args.profile == "list":
        for name in PROFILES:
            print(name)
        return 0
    print(shock_summary(args.profile))
    return 0


def _regions(args: argparse.Namespace) -> int:
    from .regions import rank_regions
    ranking = rank_regions(
        jurisdiction=args.jurisdiction,
        variant=args.variant,
        weighting=args.weighting,
        top_n=args.top,
    )
    print(f"weighting={args.weighting}  jurisdiction={args.jurisdiction or 'any'}  "
          f"variant={args.variant or 'any'}")
    print()
    for region, score in ranking:
        print(f"  {score:5.2f}  [{region.jurisdiction}] {region.name}")
        print(f"          variants: {', '.join(region.suited_variants)}")
        for axis in ("RES", "INT", "WAT", "REG", "SUP", "SOC"):
            print(f"          {axis} = {region.scores[axis]}  ({region.sources[axis]})")
        if region.notes:
            print(f"          notes: {region.notes}")
        print()
    return 0


def _finance(args: argparse.Namespace) -> int:
    from .finance import npv, irr, payback_years, cashflow_series
    cf = cashflow_series(
        capex=args.capex,
        annual_revenue=args.annual_revenue,
        annual_opex=args.annual_opex,
        years=args.years,
        salvage=args.salvage,
    )
    n = npv(cf, args.discount_rate)
    r = irr(cf)
    pb = payback_years(args.capex, args.annual_revenue - args.annual_opex,
                       discount_rate=args.discount_rate)
    print(f"  CapEx:           ${args.capex:,.0f}")
    print(f"  Annual revenue:  ${args.annual_revenue:,.0f}")
    print(f"  Annual opex:     ${args.annual_opex:,.0f}")
    print(f"  Years:           {args.years}")
    print(f"  Discount rate:   {args.discount_rate:.2%}")
    print(f"  NPV:             ${n:,.0f}")
    if r is None:
        print(f"  IRR:             (no real IRR found)")
    else:
        print(f"  IRR:             {r:.2%}")
    if pb is None:
        print(f"  Payback:         (never)")
    else:
        print(f"  Payback:         {pb:.2f} years")
    return 0


def _render(args: argparse.Namespace) -> int:
    out = render_all()
    print(out["stamp"])
    print("Wrote:")
    print(f"  report/_generated_tables.md")
    print(f"  {out['tornado_unsubsidised']}")
    print(f"  {out['tornado_45v']}")
    return 0


def _package(args: argparse.Namespace) -> int:
    from .packaging import available_schemes, package_grant
    if args.scheme == "list":
        for s in available_schemes():
            print(s)
        return 0
    out_dir = Path(args.out)
    archive = package_grant(args.scheme, out_dir, total_usd=args.total_usd)
    print(f"wrote {archive}")
    return 0


def _diplomacy_git_sha() -> str:
    import subprocess
    from .paths import REPO_ROOT
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT, check=False,
        )
        return out.stdout.strip() or "no-git"
    except FileNotFoundError:
        return "no-git"


def _diplomacy_params_hash() -> str:
    import hashlib
    from .paths import MODEL_ROOT
    return hashlib.sha256(
        (MODEL_ROOT / "data" / "tech_params.yaml").read_bytes()
    ).hexdigest()[:12]


def _diplomacy_summary_to_dict(s: object) -> dict[str, object]:
    # MonteCarloSummary is a frozen dataclass with documented attributes.
    from .diplomacy import MonteCarloSummary
    assert isinstance(s, MonteCarloSummary)
    return {
        "posture": list(s.posture),
        "runs": s.runs,
        "years": s.years,
        "seed": s.seed,
        "mean": s.mean,
        "std": s.std,
        "p10": s.p10,
        "p50": s.p50,
        "p90": s.p90,
        "min": s.min,
        "max": s.max,
    }


def _diplomacy(args: argparse.Namespace) -> int:
    import sys

    from .diplomacy import (
        BLOCS,
        SOVEREIGNTY_MAX,
        diplomacy_hash,
        monte_carlo,
        sovereignty_spent,
    )

    posture_arg: str = str(args.posture)
    compare_arg: str = str(args.compare)
    json_arg: str = str(args.json)
    years_arg: int = int(args.years)
    runs_arg: int = int(args.runs)
    seed_arg: int = int(args.seed)

    def _parse(spec: str) -> tuple[str, ...]:
        items = [s.strip() for s in spec.split(",") if s.strip()]
        unknown = [b for b in items if b not in BLOCS]
        if unknown:
            print(f"error: unknown bloc(s): {unknown}", file=sys.stderr)
            raise SystemExit(2)
        sov_with_dupes = sum(BLOCS[b].sovereignty for b in items)
        if sov_with_dupes > SOVEREIGNTY_MAX or sovereignty_spent(frozenset(items)) > SOVEREIGNTY_MAX:
            print(
                f"error: posture sovereignty {sov_with_dupes} exceeds cap {SOVEREIGNTY_MAX}",
                file=sys.stderr,
            )
            raise SystemExit(2)
        return tuple(items)

    def _stamp() -> str:
        return f"model v{__version__} @ {_diplomacy_git_sha()} | params {_diplomacy_params_hash()}"

    if compare_arg:
        if " vs " not in compare_arg:
            print("error: --compare expects 'A,B vs C,D' format", file=sys.stderr)
            return 2
        left, right = compare_arg.split(" vs ", 1)
        post_a = _parse(left)
        post_b = _parse(right)
        sa = monte_carlo(post_a, years=years_arg, runs=runs_arg, seed=seed_arg)
        sb = monte_carlo(post_b, years=years_arg, runs=runs_arg, seed=seed_arg)
        delta = sb.p50 - sa.p50
        print(f"A {post_a}: mean={sa.mean:.2f} p50={sa.p50:.2f}")
        print(f"B {post_b}: mean={sb.mean:.2f} p50={sb.p50:.2f}")
        print(f"delta_median (B - A) = {delta:.2f}")
        if json_arg:
            envelope_cmp: dict[str, object] = {
                "stamp": _stamp(),
                "model_version": __version__,
                "git_sha": _diplomacy_git_sha(),
                "params_hash": _diplomacy_params_hash(),
                "diplomacy_constants_hash": diplomacy_hash(),
                "posture": list(post_a),
                "seed": seed_arg,
                "runs": runs_arg,
                "years": years_arg,
                "summary": _diplomacy_summary_to_dict(sa),
                "posture_a": list(post_a),
                "posture_b": list(post_b),
                "delta_median": delta,
                "summary_b": _diplomacy_summary_to_dict(sb),
            }
            Path(json_arg).write_text(json.dumps(envelope_cmp, indent=2))
            print(f"wrote {json_arg}")
        return 0

    if not posture_arg:
        print("error: --posture is required (or use --compare)", file=sys.stderr)
        return 2
    posture = _parse(posture_arg)
    s = monte_carlo(posture, years=years_arg, runs=runs_arg, seed=seed_arg)
    print(f"posture: {posture}")
    print(f"runs:    {s.runs}  years: {s.years}  seed: {s.seed}")
    print(f"mean:    {s.mean:.2f}")
    print(f"p10/50/90: {s.p10:.2f} / {s.p50:.2f} / {s.p90:.2f}")
    print(f"std:     {s.std:.2f}")
    if json_arg:
        envelope: dict[str, object] = {
            "stamp": _stamp(),
            "model_version": __version__,
            "git_sha": _diplomacy_git_sha(),
            "params_hash": _diplomacy_params_hash(),
            "diplomacy_constants_hash": diplomacy_hash(),
            "posture": list(posture),
            "seed": seed_arg,
            "runs": runs_arg,
            "years": years_arg,
            "summary": _diplomacy_summary_to_dict(s),
        }
        Path(json_arg).write_text(json.dumps(envelope, indent=2))
        print(f"wrote {json_arg}")
    return 0


def _summary(args: argparse.Namespace) -> int:
    path = render_summary_json(Path(args.out))
    print(f"wrote {path}")
    print(json.dumps(json.loads(path.read_text()), indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    """electicity CLI entrypoint. Returns the process exit code."""
    p = argparse.ArgumentParser(prog="electicity")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("car", help="evaluate a vehicle scenario")
    pc.add_argument("--scenario", required=True)
    pc.add_argument("--h2-price", type=float, default=None)
    pc.add_argument("--discount-rate", type=float, default=0.08)
    pc.set_defaults(func=_car)

    pd = sub.add_parser("district", help="evaluate a district scenario")
    pd.add_argument("--scenario", required=True)
    pd.add_argument("--envelope", type=float, default=36.0,
                    help="capex envelope in USD millions")
    pd.add_argument("--shock", default="bau",
                    help="supply-shock profile: bau, ir_shortage, pt_shortage, li_shortage, "
                         "china_decoupling, triple_squeeze, western_only, maritime_blockade, "
                         "regional_autarky")
    pd.set_defaults(func=_district)

    psh = sub.add_parser("shock", help="describe a supply-shock profile")
    psh.add_argument("--profile", required=True, help="profile name or 'list'")
    psh.set_defaults(func=_shock)

    preg = sub.add_parser("regions", help="rank candidate regions")
    preg.add_argument("--jurisdiction", choices=["EU", "US", "AU", "NZ"], default=None)
    preg.add_argument("--variant", choices=["inland", "river-adjacent", "tidal"], default=None)
    preg.add_argument("--weighting", choices=["deploy", "autonomy"], default="deploy")
    preg.add_argument("--top", type=int, default=None, help="show only top-N")
    preg.set_defaults(func=_regions)

    pf = sub.add_parser("finance", help="compute NPV / IRR / payback for cashflow series")
    pf.add_argument("--capex", type=float, required=True)
    pf.add_argument("--annual-revenue", type=float, required=True)
    pf.add_argument("--annual-opex", type=float, default=0.0)
    pf.add_argument("--years", type=int, default=25)
    pf.add_argument("--discount-rate", type=float, default=0.09)
    pf.add_argument("--salvage", type=float, default=0.0)
    pf.set_defaults(func=_finance)

    pr = sub.add_parser("render-all", help="regenerate every chart and embedded table")
    pr.set_defaults(func=_render)

    ppk = sub.add_parser("package", help="bundle a scheme-specific submission archive")
    ppk.add_argument("--scheme", required=True,
                     help="scheme name or 'list' to enumerate supported schemes")
    ppk.add_argument("--out", default=".", help="output directory for the zip")
    ppk.add_argument("--total-usd", type=float, default=None,
                     help="override the default total budget (USD)")
    ppk.set_defaults(func=_package)

    ps = sub.add_parser("summary", help="emit machine-readable JSON summary")
    ps.add_argument("--out", default="model/_summary.json")
    ps.set_defaults(func=_summary)

    pdp = sub.add_parser("diplomacy", help="run a diplomacy Monte Carlo or compare two postures")
    pdp.add_argument("--posture", default="",
                     help="comma-separated bloc names, e.g. WEST_FRIEND,LATAM_FRIEND")
    pdp.add_argument("--compare", default="",
                     help="'A,B vs C,D' to compare two postures (overrides --posture)")
    pdp.add_argument("--years", type=int, default=5)
    pdp.add_argument("--runs", type=int, default=200)
    pdp.add_argument("--seed", type=int, default=0)
    pdp.add_argument("--json", default="", help="optional path to write the JSON envelope")
    pdp.set_defaults(func=_diplomacy)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
