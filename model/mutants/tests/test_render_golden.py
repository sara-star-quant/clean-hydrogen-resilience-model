"""Golden-file regression for render output. Drift from baseline fails loudly.

Run `pytest --update-golden` semantics: just delete the golden file to recapture.
"""

from __future__ import annotations

from pathlib import Path

from electicity_model.render import render_district_table, render_truck_table

GOLDEN_DIR = Path(__file__).parent / "_golden"


def _check_or_capture(name: str, content: str) -> None:
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    path = GOLDEN_DIR / f"{name}.md"
    if not path.exists():
        path.write_text(content)
        # First run captures the baseline; do not fail.
        return
    expected = path.read_text()
    # Strip the version stamp line which embeds a hash that legitimately changes when
    # tech_params.yaml is edited; the rest of the table content is the golden.
    def _strip_stamps(s: str) -> str:
        return "\n".join(
            line for line in s.splitlines() if not line.strip().startswith("<!-- model")
        )
    if _strip_stamps(expected) != _strip_stamps(content):
        diff_msg = (
            f"Golden drift for {name}.\n"
            f"--- expected (in {path}) ---\n{expected}\n"
            f"--- actual ---\n{content}\n"
            f"If the change is intentional, delete {path} and rerun to recapture."
        )
        raise AssertionError(diff_msg)


def test_district_table_golden():
    out = render_district_table([
        "district_solar_h2_inland",
        "district_microhydro_river",
        "district_tidal_coastal",
    ])
    _check_or_capture("district_table", out)


def test_truck_table_golden():
    out = render_truck_table([
        "car_fcev_class8",
        "car_bev_class8_ref",
        "car_diesel_class8_ref",
    ])
    _check_or_capture("truck_table", out)
