"""Phase 0 contract test.

The playground HTML must contain a single <script type="application/json"
id="diplomacy-constants"> block that parses cleanly, exposes all seven blocs,
sums shock baseline probabilities to 1.0, and uses canonically-sorted relation
pairs. The Python diplomacy module (added in Phase 4) reads this same block
as its source of truth, so the schema must be locked.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


PLAYGROUND_HTML = (
    Path(__file__).resolve().parents[2] / "playground" / "microgrid_sim.html"
)
EXPECTED_BLOCS = {
    "EU_FRIEND",
    "WEST_FRIEND",
    "EAST_FRIEND",
    "SOUTH_CENTRAL_FRIEND",
    "NORTH_FRIEND",
    "AFRICA_FRIEND",
    "LATAM_FRIEND",
}
EXPECTED_SHOCKS = {
    "bau",
    "ir_shortage",
    "pt_shortage",
    "li_shortage",
    "china_decoupling",
    "triple_squeeze",
    "western_only",
    "maritime_blockade",
    "regional_autarky",
}


def _load_constants() -> dict:
    text = PLAYGROUND_HTML.read_text(encoding="utf-8")
    pattern = re.compile(
        r'<script type="application/json" id="diplomacy-constants">\s*(.*?)\s*</script>',
        re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        pytest.fail("diplomacy-constants JSON block not found in playground HTML")
    return json.loads(match.group(1))


def test_constants_block_present_and_parses():
    data = _load_constants()
    assert isinstance(data, dict)
    assert set(data) >= {
        "version",
        "blocs",
        "blocRelations",
        "shockBaseProb",
        "sovereigntyMax",
    }


def test_seven_blocs_with_required_fields():
    data = _load_constants()
    blocs = data["blocs"]
    assert set(blocs) == EXPECTED_BLOCS
    for key, b in blocs.items():
        assert {"label", "desc", "cost", "sovereignty", "damping", "bonus", "prob_delta"} <= set(b), (
            f"{key} missing fields"
        )
        assert isinstance(b["cost"], (int, float)) and b["cost"] > 0
        assert b["sovereignty"] in (1, 2)
        assert isinstance(b["damping"], dict)
        assert isinstance(b["bonus"], dict)
        assert isinstance(b["prob_delta"], dict)


def test_shock_base_prob_sums_to_one_and_covers_all_shocks():
    data = _load_constants()
    probs = data["shockBaseProb"]
    assert set(probs) == EXPECTED_SHOCKS, f"shock keys mismatch: {set(probs)}"
    total = sum(probs.values())
    assert total == pytest.approx(1.0, abs=1e-9), f"shockBaseProb sums to {total}, not 1"
    for k, v in probs.items():
        assert 0.0 <= v <= 0.5, f"{k} prob {v} outside [0, 0.5]"


def test_bloc_relations_sorted_canonical_pairs():
    data = _load_constants()
    rels = data["blocRelations"]
    assert isinstance(rels, list)
    seen_pairs: set[tuple[str, str]] = set()
    for triple in rels:
        assert len(triple) == 3, f"relation {triple!r} not a triple"
        a, b, value = triple
        assert isinstance(a, str) and isinstance(b, str)
        assert a in EXPECTED_BLOCS and b in EXPECTED_BLOCS
        assert a < b, f"relation pair ({a!r}, {b!r}) not in canonical sorted order"
        assert (a, b) not in seen_pairs, f"duplicate relation pair ({a!r}, {b!r})"
        seen_pairs.add((a, b))
        assert isinstance(value, (int, float))
        assert -1.0 <= value <= 1.0


def test_sovereignty_max_is_ten():
    data = _load_constants()
    assert data["sovereigntyMax"] == 10
