"""Tech parameter loading. Every value carries source/year/range for traceability.

Schema validation runs at load time so a malformed YAML entry fails loudly rather than
surfacing as a confusing KeyError deep in `_district_capex`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import yaml

from .paths import DATA_DIR

# Type alias for the raw YAML structure: tech_name -> field_name -> body dict.
RawParamsYaml = dict[str, dict[str, dict[str, Any]]]
RawScenariosYaml = dict[str, dict[str, Any]]

__all__ = [
    "DATA_DIR",
    "Param",
    "ParamSchemaError",
    "ParamSet",
    "load_params",
    "load_scenarios",
]

REQUIRED_PARAM_FIELDS = ("value", "range_low", "range_high", "unit", "year", "source")


class ParamSchemaError(ValueError):
    """Raised when tech_params.yaml fails schema validation."""


def _validate_param_dict(tech: str, field: str, body: object) -> None:
    if not isinstance(body, dict):
        raise ParamSchemaError(
            f"{tech}.{field}: expected mapping, got {type(body).__name__}"
        )
    body_typed = cast(dict[str, Any], body)
    missing = [k for k in REQUIRED_PARAM_FIELDS if k not in body_typed]
    if missing:
        raise ParamSchemaError(
            f"{tech}.{field}: missing required keys {missing}"
        )
    for num_key in ("value", "range_low", "range_high"):
        val = body_typed[num_key]
        if not isinstance(val, (int, float)):
            raise ParamSchemaError(
                f"{tech}.{field}.{num_key}: expected number, got {type(val).__name__}"  # pyright: ignore[reportUnknownArgumentType]
            )
    if body_typed["range_low"] > body_typed["range_high"]:
        raise ParamSchemaError(
            f"{tech}.{field}: range_low ({body_typed['range_low']}) > "
            f"range_high ({body_typed['range_high']})"
        )
    if not (body_typed["range_low"] <= body_typed["value"] <= body_typed["range_high"]):
        raise ParamSchemaError(
            f"{tech}.{field}: value {body_typed['value']} outside range "
            f"[{body_typed['range_low']}, {body_typed['range_high']}]"
        )
    year_val = body_typed["year"]
    if not isinstance(year_val, int):
        raise ParamSchemaError(
            f"{tech}.{field}.year: expected int, got {type(year_val).__name__}"  # pyright: ignore[reportUnknownArgumentType]
        )
    if not body_typed["source"]:
        raise ParamSchemaError(f"{tech}.{field}.source: empty")


@dataclass(frozen=True, slots=True)
class Param:
    """A single tech parameter with provenance.

    Every numeric value carries the citation key it traces to and the year of the source,
    so a reviewer can audit any number end-to-end without leaving the repository.
    """

    value: float
    range_low: float
    range_high: float
    unit: str
    year: int
    source: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class ParamSet:
    """All parameters for one technology, keyed by field name."""

    name: str
    fields: dict[str, Param]

    def get(self, field: str) -> Param:
        """Return the full Param record for a named field."""
        return self.fields[field]

    def v(self, field: str) -> float:
        """Return just the central value of a named field. Convenience accessor."""
        return self.fields[field].value


def load_params(path: Path | None = None) -> dict[str, ParamSet]:
    """Read and validate tech_params.yaml. Returns ParamSet per technology.

    Schema violations raise ParamSchemaError at load time so a malformed entry surfaces
    before any scenario evaluation runs.
    """
    path = path or (DATA_DIR / "tech_params.yaml")
    with path.open() as f:
        loaded = yaml.safe_load(f)
    if not isinstance(loaded, dict):
        raise ParamSchemaError("top-level YAML must be a mapping")
    raw = cast(dict[str, Any], loaded)
    out: dict[str, ParamSet] = {}
    for tech, fields in raw.items():
        if not isinstance(fields, dict):
            raise ParamSchemaError(
                f"tech {tech!r}: expected mapping of fields, got {type(fields).__name__}"
            )
        fields_typed = cast(dict[str, dict[str, Any]], fields)
        parsed: dict[str, Param] = {}
        for fname, body in fields_typed.items():
            _validate_param_dict(tech, fname, body)
            parsed[fname] = Param(
                value=float(body["value"]),
                range_low=float(body["range_low"]),
                range_high=float(body["range_high"]),
                unit=str(body["unit"]),
                year=int(body["year"]),
                source=str(body["source"]),
                notes=str(body.get("notes", "")),
            )
        out[tech] = ParamSet(name=tech, fields=parsed)
    return out


def load_scenarios(path: Path | None = None) -> RawScenariosYaml:
    """Read scenarios.yaml as a plain dict-of-dicts. No schema check at this layer."""
    path = path or (DATA_DIR / "scenarios.yaml")
    with path.open() as f:
        return cast(RawScenariosYaml, yaml.safe_load(f))
