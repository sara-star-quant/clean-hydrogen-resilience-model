"""Render markdown tables and matplotlib charts. Embed version and params hash."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

from . import __version__
from .paths import ASSETS, MODEL_ROOT, REPO_ROOT, REPORT
from .scenarios import DistrictResult, TruckResult, evaluate_district, evaluate_truck
from .sensitivity import TornadoResult, tornado_lcoh

__all__ = [
    "stamp",
    "md_table",
    "render_district_table",
    "render_truck_table",
    "render_tornado_chart",
    "render_all",
    "render_summary_json",
]

# Backwards-compat alias for callers that imported the old name.
REPO = REPO_ROOT


def _git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=REPO, check=False,
        )
        return out.stdout.strip() or "no-git"
    except FileNotFoundError:
        return "no-git"


def _params_hash() -> str:
    p = MODEL_ROOT / "data" / "tech_params.yaml"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def stamp() -> str:
    """Return the HTML comment stamp embedded in every rendered artifact.

    Encodes the model version, git short-sha (or ``no-git``), and a 12-char prefix of the
    sha256 of ``tech_params.yaml`` so a reader can tie any number to its inputs.
    """
    return f"<!-- model v{__version__} @ {_git_sha()} | params {_params_hash()} -->"


def md_table(headers: list[str], rows: Iterable[list[Any]]) -> str:
    """Render a list of rows as a GitHub-flavoured markdown table."""
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def render_district_table(scenarios: list[str]) -> str:
    """Render a markdown table summarising several district scenarios."""
    rows: list[list[Any]] = []
    for name in scenarios:
        r = evaluate_district(name)
        rows.append([
            name,
            f"${r.capex_total_usd / 1e6:.1f}M",
            "yes" if r.fits_36m_envelope else "**no**",
            f"${r.lcoe_per_mwh:.0f}/MWh",
            f"${r.lcoh_per_kg:.2f}/kg",
        ])
    return stamp() + "\n<!-- caption: scenario output, not a forecast -->\n\n" + md_table(
        ["Scenario", "CapEx", "Fits $36M?", "LCOE", "LCOH"],
        rows,
    )


def render_truck_table(
    scenarios: list[str],
    h2_prices: tuple[float, ...] = (4.0, 6.0, 9.0),
) -> str:
    """Render a markdown table comparing FCEV vs BEV vs diesel TCO across H2 prices."""
    rows: list[list[Any]] = []
    for name in scenarios:
        for h2 in h2_prices:
            r = evaluate_truck(name, h2_price_per_kg=h2)
            rows.append([
                name,
                r.powertrain,
                f"${h2:.0f}/kg" if r.powertrain == "fcev" else "n/a",
                f"${r.tco_per_km:.3f}/km",
                f"${r.fuel_per_km:.3f}/km",
            ])
            if r.powertrain != "fcev":
                break
    return stamp() + "\n<!-- caption: scenario output, not a forecast -->\n\n" + md_table(
        ["Scenario", "Powertrain", "H2 price", "TCO", "Fuel cost"],
        rows,
    )


def render_tornado_chart(out_path: Path, ira_45v: bool = False) -> Path:
    """Render a tornado chart of LCOH sensitivity to top drivers, optionally with 45V."""
    # matplotlib's bundled type stubs are incomplete in 2026; pyright strict flags every
    # plotting call. The chart is exercised by tests; the type ignores are scoped tightly.
    import matplotlib  # pyright: ignore[reportMissingTypeStubs]
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt  # pyright: ignore[reportMissingTypeStubs]

    results: list[TornadoResult] = tornado_lcoh(
        ira_45v_credit_per_kg=3.0 if ira_45v else 0.0,
    )
    drivers = [r.driver for r in results][::-1]
    base = results[0].base_output
    lows = [r.low_output - base for r in results][::-1]
    highs = [r.high_output - base for r in results][::-1]

    # Matplotlib bundled stubs are partial in 2026; the per-line ignores quiet pyright
    # without disabling type-check for the whole module. Tests exercise this function.
    fig, ax = plt.subplots(figsize=(8, 4.5))  # pyright: ignore[reportUnknownMemberType]
    ax.barh(drivers, lows, color="#3b6ea8", label="Low end")  # pyright: ignore[reportUnknownMemberType]
    ax.barh(drivers, highs, color="#a83b3b", label="High end", alpha=0.85)  # pyright: ignore[reportUnknownMemberType]
    ax.axvline(0, color="black", linewidth=0.7)  # pyright: ignore[reportUnknownMemberType]
    title = "LCOH sensitivity (USD/kg), "
    title += "with IRA 45V Tier-1 credit" if ira_45v else "no subsidy"
    ax.set_title(title)  # pyright: ignore[reportUnknownMemberType]
    ax.set_xlabel(f"$\\Delta$ from base ${base:.2f}/kg")  # pyright: ignore[reportUnknownMemberType]
    ax.legend(loc="lower right", fontsize=8)  # pyright: ignore[reportUnknownMemberType]
    fig.tight_layout()  # pyright: ignore[reportUnknownMemberType]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140)  # pyright: ignore[reportUnknownMemberType]
    plt.close(fig)  # pyright: ignore[reportUnknownMemberType]
    return out_path


def render_all() -> dict[str, Any]:
    """One-call rebuild of every embedded artifact."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    out = {
        "stamp": stamp(),
        "district_table": render_district_table([
            "district_solar_h2_inland",
            "district_microhydro_river",
            "district_tidal_coastal",
        ]),
        "truck_table": render_truck_table([
            "car_fcev_class8",
            "car_bev_class8_ref",
            "car_diesel_class8_ref",
        ]),
        "tornado_unsubsidised": str(render_tornado_chart(ASSETS / "tornado_lcoh_unsubsidised.png")),
        "tornado_45v": str(render_tornado_chart(ASSETS / "tornado_lcoh_45v.png", ira_45v=True)),
    }
    (REPORT / "_generated_tables.md").write_text(
        f"# Generated tables {stamp()}\n\n"
        "Do not edit by hand. Run `python -m electicity_model.cli render-all` to regenerate.\n\n"
        "## District scenarios\n\n" + out["district_table"] + "\n\n"
        "## Heavy-duty truck scenarios\n\n" + out["truck_table"] + "\n"
    )
    return out


def render_summary_json(path: Path) -> Path:
    """Machine-readable summary for downstream tools."""
    data: dict[str, Any] = {
        "version": __version__,
        "git_sha": _git_sha(),
        "params_hash": _params_hash(),
        "districts": {},
        "trucks": {},
    }
    for name in ("district_solar_h2_inland", "district_microhydro_river", "district_tidal_coastal"):
        r: DistrictResult = evaluate_district(name)
        data["districts"][name] = {
            "capex_total_usd": r.capex_total_usd,
            "lcoe_per_mwh": r.lcoe_per_mwh,
            "lcoh_per_kg": r.lcoh_per_kg,
            "fits_36m_envelope": r.fits_36m_envelope,
            "capex_breakdown": r.capex_breakdown,
        }
    for name in ("car_fcev_class8", "car_bev_class8_ref", "car_diesel_class8_ref"):
        rt: TruckResult = evaluate_truck(name)
        data["trucks"][name] = {
            "tco_per_km": rt.tco_per_km,
            "fuel_per_km": rt.fuel_per_km,
            "annual_fuel_cost": rt.annual_fuel_cost,
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    return path
