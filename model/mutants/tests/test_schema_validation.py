"""Schema-validation error paths in load_params."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from electicity_model.tech import ParamSchemaError, load_params


def _write(tmp_path: Path, content: dict) -> Path:
    p = tmp_path / "params.yaml"
    p.write_text(yaml.safe_dump(content))
    return p


def test_top_level_must_be_mapping(tmp_path):
    p = tmp_path / "p.yaml"
    p.write_text("- not\n- a mapping\n")
    with pytest.raises(ParamSchemaError, match="top-level"):
        load_params(p)


def test_tech_must_be_mapping(tmp_path):
    p = _write(tmp_path, {"solar_pv_utility": "broken"})
    with pytest.raises(ParamSchemaError, match="expected mapping of fields"):
        load_params(p)


def test_field_missing_required_keys(tmp_path):
    p = _write(tmp_path, {
        "solar_pv_utility": {
            "capex_per_kw": {"value": 1100, "unit": "USD_per_kW"}  # no range, year, source
        }
    })
    with pytest.raises(ParamSchemaError, match="missing required keys"):
        load_params(p)


def test_range_inverted(tmp_path):
    p = _write(tmp_path, {
        "solar_pv_utility": {
            "capex_per_kw": {
                "value": 1100, "range_low": 2000, "range_high": 800,
                "unit": "USD_per_kW", "year": 2024, "source": "X",
            }
        }
    })
    with pytest.raises(ParamSchemaError, match=r"range_low.+>.+range_high"):
        load_params(p)


def test_value_outside_range(tmp_path):
    p = _write(tmp_path, {
        "solar_pv_utility": {
            "capex_per_kw": {
                "value": 5000, "range_low": 800, "range_high": 1500,
                "unit": "USD_per_kW", "year": 2024, "source": "X",
            }
        }
    })
    with pytest.raises(ParamSchemaError, match="outside range"):
        load_params(p)


def test_value_must_be_numeric(tmp_path):
    p = _write(tmp_path, {
        "solar_pv_utility": {
            "capex_per_kw": {
                "value": "not a number", "range_low": 0, "range_high": 0,
                "unit": "USD_per_kW", "year": 2024, "source": "X",
            }
        }
    })
    with pytest.raises(ParamSchemaError, match="expected number"):
        load_params(p)


def test_empty_source_rejected(tmp_path):
    p = _write(tmp_path, {
        "solar_pv_utility": {
            "capex_per_kw": {
                "value": 1100, "range_low": 800, "range_high": 1500,
                "unit": "USD_per_kW", "year": 2024, "source": "",
            }
        }
    })
    with pytest.raises(ParamSchemaError, match="source"):
        load_params(p)


def test_real_yaml_passes_schema():
    """The shipped tech_params.yaml must always validate."""
    params = load_params()
    assert "solar_pv_utility" in params
    assert "pem_electrolyzer" in params
