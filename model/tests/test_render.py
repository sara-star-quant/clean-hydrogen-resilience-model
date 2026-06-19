"""Render path coverage: tables, charts, summary JSON, hash determinism."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electicity_model.render import (
    md_table,
    render_all,
    render_district_table,
    render_summary_json,
    render_truck_table,
    stamp,
)


def test_stamp_includes_version_and_hash():
    s = stamp()
    assert "model" in s
    assert "params" in s
    assert s.startswith("<!-- ") and s.endswith(" -->")


def test_md_table_round_trip():
    out = md_table(["a", "b"], [[1, 2], [3, 4]])
    assert out.count("\n") == 3
    assert "| a | b |" in out
    assert "| 1 | 2 |" in out


def test_render_district_table_lists_scenarios():
    out = render_district_table(["district_solar_h2_inland", "district_microhydro_river"])
    assert "district_solar_h2_inland" in out
    assert "LCOE" in out


def test_render_truck_table_emits_h2_band_for_fcev_only():
    out = render_truck_table(["car_fcev_class8", "car_bev_class8_ref"])
    assert out.count("car_fcev_class8") == 3  # one row per H2 price (4, 6, 9)
    assert out.count("car_bev_class8_ref") == 1


def test_render_all_writes_tables_and_charts():
    out = render_all()
    assert "stamp" in out
    assert Path(out["tornado_unsubsidised"]).exists()
    assert Path(out["tornado_45v"]).exists()


def test_render_summary_json_is_parseable(tmp_path):
    p = render_summary_json(tmp_path / "summary.json")
    data = json.loads(p.read_text())
    assert set(data["districts"]) >= {"district_solar_h2_inland"}
    assert set(data["trucks"]) >= {"car_fcev_class8"}
    assert "params_hash" in data
    assert len(data["params_hash"]) >= 8


def test_render_all_is_deterministic_for_same_params():
    a = render_all()
    b = render_all()
    # The stamp will tie to the same params hash; tables identical apart from possible
    # minor regen idempotence (file mtimes don't matter; content does).
    assert a["stamp"] == b["stamp"]
    assert a["district_table"] == b["district_table"]
    assert a["truck_table"] == b["truck_table"]
