"""End-to-end CLI tests via subprocess. Covers argparse and exit codes."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

CLI = [sys.executable, "-m", "electicity_model.cli"]


def run(args, **kw):
    return subprocess.run(CLI + args, capture_output=True, text=True, **kw)


def test_cli_version():
    r = run(["--version"])
    assert r.returncode == 0
    assert r.stdout.strip()


def test_cli_no_args_exits_non_zero():
    r = run([])
    assert r.returncode != 0


def test_cli_unknown_subcommand():
    r = run(["bogus"])
    assert r.returncode != 0


def test_cli_district_happy_path():
    r = run(["district", "--scenario", "district_solar_h2_inland"])
    assert r.returncode == 0
    assert "CapEx total" in r.stdout
    assert "LCOE" in r.stdout


def test_cli_district_with_shock():
    r = run(["district", "--scenario", "district_solar_h2_inland",
             "--shock", "ir_shortage"])
    assert r.returncode == 0
    assert "ir_shortage" in r.stdout


def test_cli_district_unknown_scenario():
    r = run(["district", "--scenario", "atlantis"])
    assert r.returncode != 0


def test_cli_car_happy_path():
    r = run(["car", "--scenario", "car_fcev_class8", "--h2-price", "4.0"])
    assert r.returncode == 0
    assert "TCO" in r.stdout


def test_cli_shock_list():
    r = run(["shock", "--profile", "list"])
    assert r.returncode == 0
    assert "ir_shortage" in r.stdout
    assert "maritime_blockade" in r.stdout


def test_cli_shock_describe():
    r = run(["shock", "--profile", "triple_squeeze"])
    assert r.returncode == 0
    assert "x" in r.stdout  # multiplier table


def test_cli_regions_au():
    r = run(["regions", "--jurisdiction", "AU", "--top", "1"])
    assert r.returncode == 0
    assert "Tasmania" in r.stdout


def test_cli_finance_happy_path():
    r = run(["finance", "--capex", "27000000",
             "--annual-revenue", "5500000", "--annual-opex", "1300000",
             "--years", "25", "--discount-rate", "0.09"])
    assert r.returncode == 0
    assert "NPV" in r.stdout
    assert "IRR" in r.stdout


def test_cli_summary_emits_json(tmp_path):
    out = tmp_path / "summary.json"
    r = run(["summary", "--out", str(out)])
    assert r.returncode == 0
    data = json.loads(out.read_text())
    assert "districts" in data
    assert "trucks" in data


def test_cli_render_all_creates_charts(tmp_path):
    # render-all writes to fixed paths; just ensure exit code 0 and stamp.
    r = run(["render-all"])
    assert r.returncode == 0
    assert "model" in r.stdout.lower()


# ---------------------------------------------------------------------------
# diplomacy subcommand
# ---------------------------------------------------------------------------


def test_cli_diplomacy_happy_path():
    r = run(["diplomacy", "--posture", "WEST_FRIEND,LATAM_FRIEND",
             "--runs", "30", "--seed", "7"])
    assert r.returncode == 0, r.stderr
    assert "mean" in r.stdout
    assert "p10" in r.stdout


def test_cli_diplomacy_json_schema(tmp_path):
    out = tmp_path / "dip.json"
    r = run(["diplomacy", "--posture", "WEST_FRIEND,LATAM_FRIEND",
             "--runs", "20", "--seed", "1", "--json", str(out)])
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text())
    for key in (
        "stamp", "model_version", "git_sha", "params_hash",
        "diplomacy_constants_hash", "posture", "seed", "runs", "years", "summary",
    ):
        assert key in data, f"missing key {key}"
    s = data["summary"]
    for stat in ("mean", "p10", "p50", "p90"):
        v = s[stat]
        assert v == v, f"{stat} is NaN"  # NaN != NaN


def test_cli_diplomacy_deterministic_with_seed(tmp_path):
    out_a = tmp_path / "a.json"
    out_b = tmp_path / "b.json"
    common = ["diplomacy", "--posture", "WEST_FRIEND,LATAM_FRIEND",
              "--runs", "25", "--seed", "13", "--json"]
    run_a = run(common + [str(out_a)])
    run_b = run(common + [str(out_b)])
    assert run_a.returncode == 0 and run_b.returncode == 0
    da = json.loads(out_a.read_text())
    db = json.loads(out_b.read_text())
    # Compare summary blocks (everything but stamp/git_sha which can vary).
    assert da["summary"] == db["summary"]
    assert da["diplomacy_constants_hash"] == db["diplomacy_constants_hash"]


def test_cli_diplomacy_compare(tmp_path):
    out = tmp_path / "cmp.json"
    r = run(["diplomacy",
             "--compare", "WEST_FRIEND,LATAM_FRIEND vs WEST_FRIEND,EAST_FRIEND,LATAM_FRIEND",
             "--runs", "20", "--seed", "5", "--json", str(out)])
    assert r.returncode == 0, r.stderr
    assert "delta_median" in r.stdout
    data = json.loads(out.read_text())
    assert "posture_a" in data and "posture_b" in data
    assert "delta_median" in data
    assert "summary_b" in data


def test_cli_diplomacy_unknown_bloc():
    r = run(["diplomacy", "--posture", "ATLANTIS_FRIEND",
             "--runs", "5", "--seed", "0"])
    assert r.returncode != 0
    assert "unknown" in (r.stderr + r.stdout).lower()


def test_cli_diplomacy_sovereignty_overflow():
    # The seven valid blocs sum to exactly 10 sovereignty (the cap).
    # Repeating EAST_FRIEND (cost 2) inflates the *parsed* sovereignty
    # to 12 even though the underlying set would collapse to 10. The CLI
    # rejects this kind of malformed posture explicitly.
    r = run(["diplomacy",
             "--posture", "EU_FRIEND,WEST_FRIEND,EAST_FRIEND,EAST_FRIEND,"
             "SOUTH_CENTRAL_FRIEND,NORTH_FRIEND,AFRICA_FRIEND,LATAM_FRIEND",
             "--runs", "5", "--seed", "0"])
    assert r.returncode != 0
    assert "sovereignty" in (r.stderr + r.stdout).lower()
