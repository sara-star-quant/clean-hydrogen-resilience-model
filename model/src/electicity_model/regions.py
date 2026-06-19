"""Regional database and ranking for deployment-reliability + autonomy.

Scoring rubric is documented in report/10_supply_resilience_and_regions.md.
Scores 0..5 per axis, source cited per region per axis.

Composite weights:
- "deploy" (deployment reliability): RES 0.25, INT 0.20, WAT 0.15, REG 0.15, SUP 0.10, SOC 0.15
- "autonomy" (autarky-resilient): SUP 0.30, REG 0.20, RES 0.20, WAT 0.15, SOC 0.10, INT 0.05
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

__all__ = [
    "AXES",
    "WEIGHTS_DEPLOY",
    "WEIGHTS_AUTONOMY",
    "FRIEND_BLOCS",
    "Region",
    "REGIONS",
    "filter_regions",
    "rank_regions",
]


AXES = ("RES", "INT", "WAT", "REG", "SUP", "SOC")
WEIGHTS_DEPLOY = {"RES": 0.25, "INT": 0.20, "WAT": 0.15, "REG": 0.15, "SUP": 0.10, "SOC": 0.15}
WEIGHTS_AUTONOMY = {"RES": 0.20, "INT": 0.05, "WAT": 0.15, "REG": 0.20, "SUP": 0.30, "SOC": 0.10}

# Diplomatic / coalition layer. Each jurisdiction is also tagged with a neutral
# "friend bloc" so the model can score alliance-level resilience without
# overwriting the real jurisdiction (which grant agencies and citations need).
FRIEND_BLOCS = (
    "EU_FRIEND",
    "WEST_FRIEND",
    "EAST_FRIEND",
    "SOUTH_CENTRAL_FRIEND",
    "NORTH_FRIEND",
    "AFRICA_FRIEND",
    "LATAM_FRIEND",
)


@dataclass(frozen=True, slots=True)
class Region:
    """One candidate deployment region with axis scores and per-axis sources."""

    name: str
    jurisdiction: str
    suited_variants: tuple[str, ...]
    scores: dict[str, int]
    sources: dict[str, str]
    notes: str = ""
    friend_bloc: str = ""

    def score(self, weighting: dict[str, float]) -> float:
        """Return a weighted composite score against the supplied per-axis weights."""
        return sum(weighting[k] * self.scores[k] for k in AXES)

    def deploy_score(self) -> float:
        """Composite score under the deployment-reliability weighting."""
        return self.score(WEIGHTS_DEPLOY)

    def autonomy_score(self) -> float:
        """Composite score under the autarky/autonomy weighting."""
        return self.score(WEIGHTS_AUTONOMY)


REGIONS: list[Region] = [
    # ---- EU ----
    Region(
        name="Andalucía / Aragón (Iberian Peninsula)",
        jurisdiction="EU",
        suited_variants=("inland",),
        scores={"RES": 5, "INT": 3, "WAT": 2, "REG": 4, "SUP": 3, "SOC": 4},
        sources={
            "RES": "PVGIS solar GHI > 2000 kWh/m2/yr",
            "INT": "Spain queue 2-4 yr per ENTSO-E TYNDP-aligned figures",
            "WAT": "WRI Aqueduct 4.0 medium-high baseline",
            "REG": "EC-H2-Strategy + Spain Hydrogen Roadmap signed",
            "SUP": "PV manufacturing nascent; H2 OEMs nearby (Sunfire DE)",
            "SOC": "Strong public support; Just-Transition agreements active",
        },
        notes="Default EU inland choice when grid interconnect available.",
        friend_bloc="EU_FRIEND",
    ),
    Region(
        name="Norwegian fjords (Finnmark / Trøndelag)",
        jurisdiction="EU",  # EFTA / EEA, EU-aligned market
        suited_variants=("river-adjacent",),
        scores={"RES": 5, "INT": 3, "WAT": 5, "REG": 5, "SUP": 4, "SOC": 4},
        sources={
            "RES": "Hydro CF > 0.55; abundant ROR sites",
            "INT": "Statnett TYNDP figures",
            "WAT": "WRI Aqueduct Low; Sami consultation framework",
            "REG": "Norway Hydrogen Strategy 2020 + active scheme support",
            "SUP": "Nel ASA + REC Solar domestic",
            "SOC": "Sami consultation required; framework established",
        },
        friend_bloc="NORTH_FRIEND",
    ),
    Region(
        name="Iceland (geothermal + hydro)",
        jurisdiction="EU",  # EFTA, EU-market-aligned
        suited_variants=("river-adjacent", "inland"),
        scores={"RES": 5, "INT": 4, "WAT": 5, "REG": 4, "SUP": 2, "SOC": 4},
        sources={
            "RES": "Geothermal + hydro near 100% renewable grid",
            "INT": "Landsnet small-grid interconnect 1-2 yr",
            "WAT": "WRI Aqueduct Low",
            "REG": "Iceland H2 strategy + EU-RFNBO eligible via EEA",
            "SUP": "Limited domestic OEM presence",
            "SOC": "Strong support; small population",
        },
        notes="Hardened off-grid demonstrator candidate.",
        friend_bloc="NORTH_FRIEND",
    ),
    Region(
        name="Brittany / French Atlantic coast",
        jurisdiction="EU",
        suited_variants=("tidal",),
        scores={"RES": 5, "INT": 3, "WAT": 5, "REG": 4, "SUP": 4, "SOC": 3},
        sources={
            "RES": "Tidal stream > 2.5 m/s at Raz Blanchard etc.",
            "INT": "RTE queue 2-4 yr",
            "WAT": "WRI Aqueduct Low",
            "REG": "France hydrogen strategy + tidal support history (SAE)",
            "SUP": "McPhy + Naval Group + GE Cherbourg (HD power eq.)",
            "SOC": "Tidal community engagement variable; Brittany cooperative norms",
        },
        friend_bloc="EU_FRIEND",
    ),
    # ---- US ----
    Region(
        name="Pacific Northwest (Columbia Basin WA/OR)",
        jurisdiction="US",
        suited_variants=("river-adjacent", "inland"),
        scores={"RES": 5, "INT": 3, "WAT": 5, "REG": 4, "SUP": 3, "SOC": 3},
        sources={
            "RES": "BPA hydro CF > 0.5; abundant",
            "INT": "FERC Order 2023 study-to-energization 30-48 mo",
            "WAT": "WRI Aqueduct Low",
            "REG": "Pacific NW H2 Hub designated; DPA Title III pathways",
            "SUP": "Plug Power scaling; PNNL labs",
            "SOC": "Tribal consultation required; framework established",
        },
        notes="Top US river-adjacent pick.",
        friend_bloc="WEST_FRIEND",
    ),
    Region(
        name="Texas ERCOT (West Texas / Permian)",
        jurisdiction="US",
        suited_variants=("inland",),
        scores={"RES": 5, "INT": 5, "WAT": 1, "REG": 3, "SUP": 4, "SOC": 3},
        sources={
            "RES": "Solar GHI > 2200; strong wind concurrence",
            "INT": "ERCOT non-FERC queue ~12-18 mo",
            "WAT": "WRI Aqueduct High to Extremely High",
            "REG": "State-level supportive; H2 Hubs adjacent",
            "SUP": "Tesla TX gigafactory; LG Energy nearby",
            "SOC": "Mostly favorable; water disputes possible",
        },
        notes="Fast interconnect but water-stressed; require closed-loop cooling.",
        friend_bloc="WEST_FRIEND",
    ),
    Region(
        name="Iowa / South Dakota",
        jurisdiction="US",
        suited_variants=("inland",),
        scores={"RES": 4, "INT": 4, "WAT": 5, "REG": 3, "SUP": 3, "SOC": 4},
        sources={
            "RES": "Wind CF > 0.45; solar moderate",
            "INT": "MISO/SPP queue 24-48 mo, faster than CAISO/NYISO",
            "WAT": "WRI Aqueduct Low; Missouri/Mississippi headwaters",
            "REG": "Federal support; less specific state H2 scheme",
            "SUP": "Existing wind manufacturing (TPI, Siemens Gamesa)",
            "SOC": "Agricultural community generally supportive",
        },
        friend_bloc="WEST_FRIEND",
    ),
    Region(
        name="New Mexico (high-desert solar)",
        jurisdiction="US",
        suited_variants=("inland",),
        scores={"RES": 5, "INT": 3, "WAT": 1, "REG": 3, "SUP": 2, "SOC": 3},
        sources={
            "RES": "Solar GHI > 2200; clear skies",
            "INT": "WECC queue 36-60 mo",
            "WAT": "WRI Aqueduct High; Rio Grande contested",
            "REG": "State H2 hub program; tribal lands considerations",
            "SUP": "Limited domestic OEM presence",
            "SOC": "Tribal + acequia consultation required",
        },
        notes="Only with reuse-water / dry-cooling architecture.",
        friend_bloc="WEST_FRIEND",
    ),
    # ---- AU ----
    Region(
        name="Tasmania (hydro + tidal)",
        jurisdiction="AU",
        suited_variants=("river-adjacent", "tidal", "inland"),
        scores={"RES": 5, "INT": 4, "WAT": 5, "REG": 5, "SUP": 4, "SOC": 5},
        sources={
            "RES": "Hydro Tasmania CF > 0.5; Bass Strait tidal potential",
            "INT": "Marinus Link expansion improving cross-Strait connection",
            "WAT": "WRI Aqueduct Low; high rainfall",
            "REG": "TAS H2 Action Plan + ARENA Hydrogen Headstart eligibility",
            "SUP": "Bell Bay hydrogen industrial precinct designated",
            "SOC": "Strong public + Aboriginal partnership frameworks",
        },
        notes="Top AU pick across all variants. Best water + community profile.",
        friend_bloc="SOUTH_CENTRAL_FRIEND",
    ),
    Region(
        name="Pilbara WA (solar + hydrogen)",
        jurisdiction="AU",
        suited_variants=("inland",),
        scores={"RES": 5, "INT": 4, "WAT": 2, "REG": 5, "SUP": 4, "SOC": 3},
        sources={
            "RES": "Solar GHI > 2400 kWh/m2/yr",
            "INT": "WA grid; private microgrid path fast",
            "WAT": "WRI Aqueduct High; arid",
            "REG": "WA Renewable Hydrogen Strategy + Headstart",
            "SUP": "Fortescue / ATCO industrial base",
            "SOC": "Native Title agreements required; mature framework",
        },
        notes="Strategic for AU H2 export ambitions; flag water draw.",
        friend_bloc="SOUTH_CENTRAL_FRIEND",
    ),
    Region(
        name="Snowy Hydro region NSW",
        jurisdiction="AU",
        suited_variants=("river-adjacent",),
        scores={"RES": 4, "INT": 3, "WAT": 4, "REG": 4, "SUP": 4, "SOC": 4},
        sources={
            "RES": "Hydro + Snowy 2.0 PHES",
            "INT": "AEMO ISP 2024 Transmission Investment Test priorities",
            "WAT": "WRI Aqueduct Low-Medium",
            "REG": "AEMO ISP-aligned; Snowy 2.0 framework applies",
            "SUP": "Domestic engineering depth",
            "SOC": "Established but Snowy 2.0 process has had local pushback",
        },
        friend_bloc="SOUTH_CENTRAL_FRIEND",
    ),
    # ---- NZ ----
    Region(
        name="Otago / Canterbury South Island",
        jurisdiction="NZ",
        suited_variants=("river-adjacent", "inland"),
        scores={"RES": 5, "INT": 3, "WAT": 5, "REG": 4, "SUP": 2, "SOC": 4},
        sources={
            "RES": "South Island hydro abundant; solar moderate; wind strong",
            "INT": "Transpower queue moderate; HVDC link supports",
            "WAT": "NIWA datasets show Low stress; abundant rainfall",
            "REG": "MBIE H2 Roadmap + GIDI/EECA support",
            "SUP": "Limited NZ OEM; AU partnership likely",
            "SOC": "Iwi engagement framework mandatory and well-established",
        },
        notes="Top NZ pick. Avoid Auckland/Northland for siting (interconnect).",
        friend_bloc="SOUTH_CENTRAL_FRIEND",
    ),
    Region(
        name="Taupo / Bay of Plenty (geothermal)",
        jurisdiction="NZ",
        suited_variants=("inland",),
        scores={"RES": 5, "INT": 3, "WAT": 4, "REG": 4, "SUP": 2, "SOC": 4},
        sources={
            "RES": "Geothermal CF > 0.85; near-baseload",
            "INT": "Transpower CB upgrades 2-3 yr",
            "WAT": "WRI Aqueduct Low-Medium",
            "REG": "Active geothermal-H2 support; NZ H2 Roadmap",
            "SUP": "Contact + Mercury industrial base",
            "SOC": "Iwi as geothermal asset stakeholders; mature framework",
        },
        friend_bloc="SOUTH_CENTRAL_FRIEND",
    ),
]


def filter_regions(
    *,
    jurisdiction: str | None = None,
    variant: str | None = None,
    friend_bloc: str | None = None,
    regions: Iterable[Region] = REGIONS,
) -> list[Region]:
    """Return regions matching the given jurisdiction, variant, and/or bloc filters."""
    out = list(regions)
    if jurisdiction:
        out = [r for r in out if r.jurisdiction == jurisdiction]
    if variant:
        out = [r for r in out if variant in r.suited_variants]
    if friend_bloc:
        out = [r for r in out if r.friend_bloc == friend_bloc]
    return out


def rank_regions(
    *,
    jurisdiction: str | None = None,
    variant: str | None = None,
    friend_bloc: str | None = None,
    weighting: str = "deploy",
    top_n: int | None = None,
) -> list[tuple[Region, float]]:
    """Return [(region, score), ...] sorted descending."""
    weights = WEIGHTS_DEPLOY if weighting == "deploy" else WEIGHTS_AUTONOMY
    pool = filter_regions(jurisdiction=jurisdiction, variant=variant, friend_bloc=friend_bloc)
    scored = sorted(((r, r.score(weights)) for r in pool), key=lambda x: x[1], reverse=True)
    return scored[:top_n] if top_n else scored
