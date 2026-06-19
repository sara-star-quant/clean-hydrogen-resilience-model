"""Schema integrity for tech_params.yaml and source-key resolution."""

from __future__ import annotations

import re
from pathlib import Path

from electicity_model.tech import load_params

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "report" / "references.md"


def _citation_keys() -> set[str]:
    text = REFERENCES.read_text()
    return set(re.findall(r"\[([A-Za-z0-9\-]+)\]", text))


def test_every_param_has_source_resolving_in_references():
    keys = _citation_keys()
    params = load_params()
    missing = []
    for tech_name, ps in params.items():
        for fname, p in ps.fields.items():
            if p.source == "project-internal":
                continue
            if p.source not in keys:
                missing.append(f"{tech_name}.{fname} -> {p.source}")
    assert not missing, f"unresolved citation keys: {missing}"


def test_every_param_has_range_bracketing_value():
    params = load_params()
    bad = []
    for tech_name, ps in params.items():
        for fname, p in ps.fields.items():
            if not (p.range_low <= p.value <= p.range_high):
                bad.append(f"{tech_name}.{fname}: {p.range_low} <= {p.value} <= {p.range_high}")
    assert not bad, f"value outside declared range: {bad}"
