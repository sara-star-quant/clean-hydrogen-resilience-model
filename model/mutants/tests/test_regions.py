"""Region scoring & ranking invariants."""

from __future__ import annotations

import pytest

from electicity_model.regions import (
    AXES,
    REGIONS,
    WEIGHTS_AUTONOMY,
    WEIGHTS_DEPLOY,
    filter_regions,
    rank_regions,
)


def test_every_region_scores_all_axes():
    for r in REGIONS:
        assert set(r.scores) == set(AXES), f"{r.name} missing axes"
        assert set(r.sources) == set(AXES), f"{r.name} missing sources"
        for axis in AXES:
            assert 0 <= r.scores[axis] <= 5, f"{r.name}.{axis} out of 0-5"
            assert r.sources[axis], f"{r.name}.{axis} empty source"


def test_weights_sum_to_one():
    assert sum(WEIGHTS_DEPLOY.values()) == pytest.approx(1.0)
    assert sum(WEIGHTS_AUTONOMY.values()) == pytest.approx(1.0)


def test_rank_is_deterministic():
    a = rank_regions(jurisdiction="AU")
    b = rank_regions(jurisdiction="AU")
    assert [r.name for r, _ in a] == [r.name for r, _ in b]


def test_top_n_filter():
    r = rank_regions(jurisdiction="EU", top_n=2)
    assert len(r) == 2


def test_tasmania_top_au():
    r = rank_regions(jurisdiction="AU", top_n=1)
    assert "Tasmania" in r[0][0].name


def test_filter_by_variant():
    only_tidal = filter_regions(variant="tidal")
    assert all("tidal" in r.suited_variants for r in only_tidal)


def test_autonomy_weighting_re_orders():
    deploy = {n: s for (r, s), n in zip(rank_regions(), [r.name for r in REGIONS])}
    autonomy = {n: s for (r, s), n in zip(
        rank_regions(weighting="autonomy"), [r.name for r in REGIONS]
    )}
    # At least one region's relative rank should differ.
    deploy_order = [r.name for r, _ in rank_regions()]
    autonomy_order = [r.name for r, _ in rank_regions(weighting="autonomy")]
    assert deploy_order != autonomy_order
