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
