"""Cross-module physical and financial constants.

Centralised so a value change happens in one place and the codebase has a single source
of truth for unit conversions. Module-level so they can be referenced directly without
allocating an instance.
"""

from __future__ import annotations

__all__ = [
    "H2_LHV_KWH_PER_KG",
    "DIESEL_LHV_KWH_PER_L",
    "HOURS_PER_YEAR",
    "KM_PER_MILE",
]


# Hydrogen lower heating value, used for energy/mass conversions in fuel-cell and
# electrolyzer math. Source: NIST chemistry webbook.
H2_LHV_KWH_PER_KG: float = 33.33

# Diesel lower heating value for ICE-truck fuel-cost comparison. Source: US DOE AFDC.
DIESEL_LHV_KWH_PER_L: float = 9.96

HOURS_PER_YEAR: float = 8760.0

# Exact: 1 international mile = 1.609344 km. Used in TCO unit conversion only.
KM_PER_MILE: float = 1.609344
