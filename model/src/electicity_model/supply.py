"""Supply-shock builders. Pure functions: take params, return new params.

Math contract (enforced by tests):
- bau profile is identity (bit-for-bit equal output).
- Each shock's multipliers act on specific YAML line items only, never on
  derived aggregates. triple_squeeze != Ir x 5 x Pt x 3 x Li x 2.5 multiplied
  on a common base. Each multiplier touches its own component only.
- maritime_blockade / regional_autarky model long-tail "world breaks" scenarios
  per the maritime-chokepoint thought experiment.
"""

from __future__ import annotations

import copy
from typing import Any

# Profiles are declarative: list of (path-to-yaml-key, multiplier) tuples.
# Path is dot-separated tech.field notation (resolved by _apply_path).
PROFILES: dict[str, list[tuple[str, float]]] = {
    "bau": [],
    "ir_shortage": [
        # Iridium loading x 5; PEM stack capex x 1.6 (Ir is ~30% of stack cost).
        ("pem_electrolyzer.iridium_loading_g_per_kw", 5.0),
        ("pem_electrolyzer.capex_per_kw", 1.6),
        # Recommend swap to alkaline; alkaline capex unaffected.
    ],
    "pt_shortage": [
        ("pem_fuel_cell_stationary.platinum_loading_g_per_kw", 3.0),
        ("pem_fuel_cell_stationary.capex_per_kw", 1.25),
        ("pem_fuel_cell_vehicle.capex_per_kw", 1.25),
    ],
    "li_shortage": [
        ("li_ion_battery_grid.capex_per_kwh", 2.5),
        # LFP and Na-ion remain available; scenario layer can substitute.
    ],
    "china_decoupling": [
        # Polysilicon: 30% premium during EU/US scale-up.
        ("solar_pv_utility.capex_per_kw", 1.30),
        # Battery cell: 20% premium since most cell capacity has Chinese inputs.
        ("li_ion_battery_grid.capex_per_kwh", 1.20),
        ("lfp_battery_grid.capex_per_kwh", 1.20),
        # Power electronics: SiC/Si IGBTs only (no GaN); modest BoS impact.
        # We approximate via electrolyzer/FC opex bumps for added inverter losses.
        ("pem_electrolyzer.opex_per_kw_yr", 1.10),
        ("alkaline_electrolyzer.opex_per_kw_yr", 1.10),
    ],
    "triple_squeeze": [
        # Compose the three single-material shocks. Each multiplier acts on its
        # own YAML line; we do NOT stack them onto a derived aggregate.
        ("pem_electrolyzer.iridium_loading_g_per_kw", 5.0),
        ("pem_electrolyzer.capex_per_kw", 1.6),
        ("pem_fuel_cell_stationary.platinum_loading_g_per_kw", 3.0),
        ("pem_fuel_cell_stationary.capex_per_kw", 1.25),
        ("pem_fuel_cell_vehicle.capex_per_kw", 1.25),
        ("li_ion_battery_grid.capex_per_kwh", 2.5),
    ],
    "western_only": [
        # Strict: only US + EU + AU + Canada + Japan + Korea sourced.
        # Honest broad capex premium ~25% across procured equipment.
        ("solar_pv_utility.capex_per_kw", 1.25),
        ("pem_electrolyzer.capex_per_kw", 1.25),
        ("alkaline_electrolyzer.capex_per_kw", 1.25),
        ("aem_electrolyzer.capex_per_kw", 1.25),
        ("pem_fuel_cell_stationary.capex_per_kw", 1.25),
        ("pem_fuel_cell_vehicle.capex_per_kw", 1.25),
        ("li_ion_battery_grid.capex_per_kwh", 1.25),
        ("lfp_battery_grid.capex_per_kwh", 1.25),
    ],
    "maritime_blockade": [
        # All major straits closed. Maritime chokepoint thought experiment.
        # Practically forces regional autarky. Costs spike and assemblies
        # become regional. We model as a 50% capex premium on procured
        # equipment + LFP/Na-ion only (Li-ion supply chain breaks).
        ("solar_pv_utility.capex_per_kw", 1.50),
        ("wind_onshore.capex_per_kw", 1.40),
        ("alkaline_electrolyzer.capex_per_kw", 1.50),
        ("aem_electrolyzer.capex_per_kw", 1.50),
        ("pem_electrolyzer.capex_per_kw", 2.20),  # most exposed (Ir + assembly)
        ("pem_fuel_cell_stationary.capex_per_kw", 2.00),
        ("pem_fuel_cell_vehicle.capex_per_kw", 2.00),
        ("sofc_chp.capex_per_kw", 1.60),
        ("li_ion_battery_grid.capex_per_kwh", 3.50),
        ("lfp_battery_grid.capex_per_kwh", 1.80),
        ("na_ion_battery_grid.capex_per_kwh", 1.30),
    ],
    "regional_autarky": [
        # Voluntary or mandated regional self-sufficiency. Less severe than
        # maritime_blockade. Models +30% capex premium on PGM-bearing equipment
        # (no PGM imports), forces alkaline/AEM/LFP at scenario layer.
        ("pem_electrolyzer.capex_per_kw", 1.50),
        ("pem_fuel_cell_stationary.capex_per_kw", 1.40),
        ("pem_fuel_cell_vehicle.capex_per_kw", 1.40),
        ("li_ion_battery_grid.capex_per_kwh", 1.30),
        ("solar_pv_utility.capex_per_kw", 1.15),
    ],
}


__all__ = ["PROFILES", "apply_shock", "list_profiles", "shock_summary"]


def list_profiles() -> list[str]:
    """Return all known shock profile names, including bau."""
    return list(PROFILES.keys())


def _apply_path(params: dict[str, Any], path: str, multiplier: float) -> None:
    tech, _, field = path.partition(".")
    if not field:
        raise ValueError(f"path must be tech.field, got {path!r}")
    if tech not in params:
        raise KeyError(f"unknown tech {tech!r} in supply-shock path")
    fields = params[tech]
    if field not in fields:
        raise KeyError(f"unknown field {field!r} for tech {tech!r}")
    fields[field]["value"] *= multiplier
    fields[field]["range_low"] *= multiplier
    fields[field]["range_high"] *= multiplier


def apply_shock(raw_params: dict[str, Any], profile: str) -> dict[str, Any]:
    """Return a deep-copy of raw_params with shock multipliers applied.

    `raw_params` is the dict-of-dict-of-dict shape produced by
    `yaml.safe_load(tech_params.yaml)`, the unprocessed YAML, not ParamSet.
    """
    if profile not in PROFILES:
        raise ValueError(f"unknown shock profile {profile!r}; "
                         f"available: {sorted(PROFILES)}")
    if profile == "bau":
        return copy.deepcopy(raw_params)
    out = copy.deepcopy(raw_params)
    for path, mult in PROFILES[profile]:
        _apply_path(out, path, mult)
    return out


def shock_summary(profile: str) -> str:
    """Return a printable description of a shock profile listing each per-line multiplier."""
    if profile not in PROFILES:
        raise ValueError(f"unknown shock profile {profile!r}")
    if profile == "bau":
        return "Business-as-usual baseline (identity)."
    lines = [f"Shock profile: {profile}"]
    for path, mult in PROFILES[profile]:
        lines.append(f"  {path:<55} x {mult:.2f}")
    return "\n".join(lines)
