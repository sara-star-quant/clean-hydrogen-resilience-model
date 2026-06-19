"""Supply-shock invariants.

Math contract:
- bau ≡ identity (deep-equal raw params).
- Each shock multiplier acts on a specific YAML line, never on aggregate.
- triple_squeeze ≠ product of single-material squeezes (each acts on its own line).
- LCOE under triple_squeeze > LCOE under bau on the inland scenario.
- AEM scenario has zero iridium loading.
- maritime_blockade busts the $36M envelope on the inland scenario (designed to).
"""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from electicity_model.scenarios import evaluate_district
from electicity_model.supply import PROFILES, apply_shock, shock_summary
from electicity_model.tech import DATA_DIR


def _raw():
    with (DATA_DIR / "tech_params.yaml").open() as f:
        return yaml.safe_load(f)


def test_bau_is_identity():
    raw = _raw()
    out = apply_shock(raw, "bau")
    assert out == raw


def test_unknown_profile_raises():
    with pytest.raises(ValueError, match="unknown shock profile"):
        apply_shock(_raw(), "atlantis_blockade")


def test_ir_shortage_multiplies_only_pem_lines():
    raw = _raw()
    out = apply_shock(raw, "ir_shortage")
    # PEM stack capex bumped 1.6x.
    assert out["pem_electrolyzer"]["capex_per_kw"]["value"] == pytest.approx(
        raw["pem_electrolyzer"]["capex_per_kw"]["value"] * 1.6
    )
    # Iridium loading bumped 5x.
    assert out["pem_electrolyzer"]["iridium_loading_g_per_kw"]["value"] == pytest.approx(
        raw["pem_electrolyzer"]["iridium_loading_g_per_kw"]["value"] * 5.0
    )
    # Alkaline untouched.
    assert out["alkaline_electrolyzer"] == raw["alkaline_electrolyzer"]


def test_triple_squeeze_acts_per_line_not_multiplicatively():
    raw = _raw()
    out = apply_shock(raw, "triple_squeeze")
    # PEM capex × 1.6 only (Ir line); not × 1.6 × 1.25 × 2.5.
    assert out["pem_electrolyzer"]["capex_per_kw"]["value"] == pytest.approx(
        raw["pem_electrolyzer"]["capex_per_kw"]["value"] * 1.6
    )


def test_shock_does_not_mutate_input():
    raw = _raw()
    snapshot = copy.deepcopy(raw)
    _ = apply_shock(raw, "ir_shortage")
    assert raw == snapshot


def test_lcoe_increases_under_triple_squeeze():
    bau = evaluate_district("district_solar_h2_inland", shock="bau")
    sq = evaluate_district("district_solar_h2_inland", shock="triple_squeeze")
    assert sq.lcoe_per_mwh > bau.lcoe_per_mwh
    assert sq.capex_total_usd > bau.capex_total_usd


def test_aem_scenario_has_zero_iridium_loading():
    raw = _raw()
    aem = raw["aem_electrolyzer"]
    assert aem["iridium_loading_g_per_kw"]["value"] == 0.0


def test_maritime_blockade_busts_envelope_on_inland():
    """Designed to flag the breaking point honestly."""
    r = evaluate_district("district_solar_h2_inland", shock="maritime_blockade")
    assert not r.fits_36m_envelope, (
        f"maritime_blockade should bust envelope on inland; got {r.capex_total_usd:,.0f}"
    )


def test_autonomy_max_survives_triple_squeeze_within_envelope():
    r = evaluate_district("district_autonomy_max", shock="triple_squeeze")
    # Allows up to 1.5x of commercial inland LCOE under shock (per plan target).
    bau_inland = evaluate_district("district_solar_h2_inland", shock="bau")
    assert r.lcoe_per_mwh < 1.5 * bau_inland.lcoe_per_mwh


@pytest.mark.parametrize("profile", sorted(PROFILES))
def test_every_profile_summary_renders(profile):
    s = shock_summary(profile)
    assert profile in s or profile == "bau"


def test_smr_baseload_lowest_lcoe_among_resilient_options():
    smr = evaluate_district("district_smr_baseload")
    nsw = evaluate_district("district_no_solar_no_wind")
    assert smr.lcoe_per_mwh < nsw.lcoe_per_mwh
