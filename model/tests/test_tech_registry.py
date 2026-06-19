"""Tech-registry shape and basic-output tests.

Track B stage 1 ran an equivalence test against the legacy if/elif path; stage 2 removed
the legacy path because the equivalence held byte-identical across every district
scenario. This file now asserts registry well-formedness plus basic-output sanity for
each scenario.
"""

from __future__ import annotations

import pytest

from electicity_model.scenarios import _scenarios_cached
from electicity_model.tech import load_params
from electicity_model.tech_registry import (
    DISTRICT_PREMIUMS,
    DISTRICT_TECHS,
    BOS_FACTOR,
    CapexBasis,
    district_annual_opex,
    district_capex,
)


DISTRICT_SCENARIO_NAMES = (
    "district_solar_h2_inland",
    "district_microhydro_river",
    "district_tidal_coastal",
    "district_autonomy_max",
    "district_no_solar_no_wind",
    "district_smr_baseload",
)


@pytest.fixture(scope="module")
def params():
    return load_params()


@pytest.fixture(scope="module")
def scenarios():
    return _scenarios_cached()


@pytest.mark.parametrize("scenario_name", DISTRICT_SCENARIO_NAMES)
def test_capex_breakdown_well_formed(scenario_name, params, scenarios):
    s = scenarios[scenario_name]
    breakdown = district_capex(s, params)
    assert all(v >= 0 for v in breakdown.values()), (
        f"negative capex line in {scenario_name}: {breakdown}"
    )
    assert "bos_epc_interconnect" in breakdown
    assert breakdown["bos_epc_interconnect"] > 0
    base_sum = sum(v for k, v in breakdown.items() if k not in {
        "bos_epc_interconnect", "on_site_spares", "zta_zte_controls",
    })
    assert breakdown["bos_epc_interconnect"] == pytest.approx(BOS_FACTOR * base_sum)


@pytest.mark.parametrize("scenario_name", DISTRICT_SCENARIO_NAMES)
def test_opex_non_negative(scenario_name, params, scenarios):
    s = scenarios[scenario_name]
    assert district_annual_opex(s, params) >= 0


def test_capex_changes_when_solar_doubled(params, scenarios):
    base = scenarios["district_solar_h2_inland"]
    doubled = dict(base)
    doubled["solar_pv_mwp"] = base["solar_pv_mwp"] * 2
    assert district_capex(doubled, params)["solar_pv"] == pytest.approx(
        2 * district_capex(base, params)["solar_pv"]
    )


def test_registry_scenario_keys_unique():
    keys = [s.scenario_key for s in DISTRICT_TECHS]
    assert len(keys) == len(set(keys)), f"duplicate scenario keys: {keys}"


def test_registry_labels_unique():
    labels = [s.label for s in DISTRICT_TECHS]
    assert len(labels) == len(set(labels)), f"duplicate breakdown labels: {labels}"


def test_premium_labels_unique():
    labels = [p.label for p in DISTRICT_PREMIUMS]
    assert len(labels) == len(set(labels)), f"duplicate premium labels: {labels}"


def test_premium_labels_disjoint_from_techs():
    techs = {s.label for s in DISTRICT_TECHS}
    prems = {p.label for p in DISTRICT_PREMIUMS}
    assert techs.isdisjoint(prems), f"label collision: {techs & prems}"


def test_bos_factor_is_legacy_value():
    assert BOS_FACTOR == 0.20


def test_dynamic_keys_have_default():
    for spec in DISTRICT_TECHS:
        if spec.params_key is None:
            assert spec.params_key_scenario_field is not None
            assert spec.params_key_default is not None


@pytest.mark.parametrize("basis", list(CapexBasis))
def test_capex_basis_enum_complete(basis):
    assert basis.value in {"per_kw", "per_kwh", "per_kg"}
