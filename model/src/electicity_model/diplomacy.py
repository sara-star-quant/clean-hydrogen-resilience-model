"""Diplomacy simulation: 7-bloc Friends Union, posture math, campaign mode.

Source-of-truth Python port of the diplomacy mechanics that ship in the browser
playground (``playground/microgrid_sim.html``). Both surfaces read the same JSON
constants block (``<script type="application/json" id="diplomacy-constants">``)
so they cannot drift on values. A behavioral parity test (Phase 5) ties their
outputs together at run time.

Values are teaching-grade. They are calibrated to make the trade-offs in the
playground legible, not to forecast real geopolitics.

The seven blocs:
    EU_FRIEND, WEST_FRIEND, EAST_FRIEND, SOUTH_CENTRAL_FRIEND,
    NORTH_FRIEND, AFRICA_FRIEND, LATAM_FRIEND.

Composition pipeline (numbered, applied in order):
    1. BASE tech params from tech_params.yaml.
    2. Bloc tech_capex_mult applied per (tech, field).
    3. Bloc tech_opex_mult applied per (tech, field).
    4. Shock multipliers, dampened by combined_damping(shock, posture, trust).
    5. LCOE / LCOH / availability computed by evaluate_district.
    6. solar_kill (if challenge mode); not used in standalone simulate_campaign.
    7. availability_add bonus from posture (post-result, capped at 1.0).
    8. Diplomacy capex (sum of bloc.cost) added to capex_total.
    9. ptc_capex_rebate_pct applied last, multiplying capex_total by (1 - rebate).
   10. Trust effect rolled into combined_damping in step 4 (campaign mode only).
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import statistics
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, cast

from .scenarios import evaluate_district
from .supply import PROFILES
from .tech import Param, ParamSet

__all__ = [
    "BlocBonus",
    "Bloc",
    "YearResult",
    "YearDebug",
    "CampaignResult",
    "MonteCarloSummary",
    "BLOCS",
    "BLOC_REL",
    "SHOCK_BASE_PROB",
    "SOVEREIGNTY_MAX",
    "SHOCK_NAMES",
    "Mulberry32",
    "combined_damping",
    "shock_distribution",
    "pick_shock",
    "sovereignty_spent",
    "pairwise_adjustment",
    "simulate_campaign",
    "monte_carlo",
    "diplomacy_hash",
]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BlocBonus:
    """Per-bloc baseline bonuses applied before shocks in the pipeline.

    Fields are tuples of ``(tech_name, multiplier)`` for parametric bonuses, or
    flat scalars for outcome-level bonuses. Empty tuples mean "no bonus".
    """

    tech_capex_mult: tuple[tuple[str, float], ...] = ()
    tech_opex_mult: tuple[tuple[str, float], ...] = ()
    lcoh_mult: float = 1.0
    availability_add: float = 0.0
    ptc_capex_rebate_pct: float = 0.0


@dataclass(frozen=True, slots=True)
class Bloc:
    """One Friends-Union bloc: cost, sovereignty footprint, damping, bonus, prob deltas."""

    name: str
    label: str
    desc: str
    cost: float
    sovereignty: int
    damping: tuple[tuple[str, float], ...]
    bonus: BlocBonus
    prob_delta: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class YearDebug:
    """Per-year intermediate values surfaced when ``debug=True``."""

    surviving_fraction_pre_shock: float
    capex_after_blocs: float
    capex_after_shock: float
    trust_damping_bonus: float


@dataclass(frozen=True, slots=True)
class YearResult:
    """One year of a campaign: drawn shock, scored capex/availability/lcoh, score."""

    year: int
    shock: str
    capex_total: float
    lcoh: float
    availability: float
    score: float
    debug: YearDebug | None = None


@dataclass(frozen=True, slots=True)
class CampaignResult:
    """Result of one full campaign: per-year details and total score."""

    posture: tuple[str, ...]
    seed: int
    years: tuple[YearResult, ...]
    total_score: float


@dataclass(frozen=True, slots=True)
class MonteCarloSummary:
    """Monte-Carlo distribution over total campaign scores."""

    posture: tuple[str, ...]
    runs: int
    years: int
    seed: int
    mean: float
    std: float
    p10: float
    p50: float
    p90: float
    min: float = 0.0
    max: float = 0.0


# ---------------------------------------------------------------------------
# Constants loaded from playground JSON block
# ---------------------------------------------------------------------------


_HTML_PATH = Path(__file__).resolve().parents[3] / "playground" / "microgrid_sim.html"
_JSON_RE = re.compile(
    r'<script type="application/json" id="diplomacy-constants">(.*?)</script>',
    re.DOTALL,
)
_REQUIRED_KEYS = frozenset({"version", "blocs", "blocRelations", "shockBaseProb", "sovereigntyMax"})


def _load_constants_from_html() -> dict[str, Any]:
    text = _HTML_PATH.read_text(encoding="utf-8")
    m = _JSON_RE.search(text)
    if m is None:
        raise RuntimeError(
            f"could not find diplomacy-constants JSON block in {_HTML_PATH}"
        )
    data = cast(dict[str, Any], json.loads(m.group(1)))
    missing = _REQUIRED_KEYS - data.keys()
    if missing:
        raise RuntimeError(f"diplomacy-constants missing keys: {sorted(missing)}")
    return data


def _build_bloc_bonus(raw: Mapping[str, Any]) -> BlocBonus:
    tcm = cast(Mapping[str, Any], raw.get("tech_capex_mult", {}) or {})
    tom = cast(Mapping[str, Any], raw.get("tech_opex_mult", {}) or {})
    return BlocBonus(
        tech_capex_mult=tuple(sorted((str(k), float(v)) for k, v in tcm.items())),
        tech_opex_mult=tuple(sorted((str(k), float(v)) for k, v in tom.items())),
        lcoh_mult=float(raw.get("lcoh_mult", 1.0)),
        availability_add=float(raw.get("availability_add", 0.0)),
        ptc_capex_rebate_pct=float(raw.get("ptc_capex_rebate_pct", 0.0)),
    )


def _build_blocs(raw_blocs: Mapping[str, Any]) -> dict[str, Bloc]:
    out: dict[str, Bloc] = {}
    for name, body in raw_blocs.items():
        damping_raw = cast(Mapping[str, Any], body.get("damping", {}))
        prob_delta_raw = cast(Mapping[str, Any], body.get("prob_delta", {}))
        out[name] = Bloc(
            name=name,
            label=str(body["label"]),
            desc=str(body.get("desc", "")),
            cost=float(body["cost"]),
            sovereignty=int(body["sovereignty"]),
            damping=tuple(sorted((str(k), float(v)) for k, v in damping_raw.items())),
            bonus=_build_bloc_bonus(cast(Mapping[str, Any], body.get("bonus", {}))),
            prob_delta=tuple(sorted((str(k), float(v)) for k, v in prob_delta_raw.items())),
        )
    return out


def _build_bloc_rel(raw_rel: list[list[Any]]) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    for entry in raw_rel:
        a, b, w = str(entry[0]), str(entry[1]), float(entry[2])
        key = (a, b) if a <= b else (b, a)
        out[key] = w
    return out


_RAW = _load_constants_from_html()
_BLOCS = _build_blocs(cast(Mapping[str, Any], _RAW["blocs"]))
_BLOC_REL = _build_bloc_rel(cast(list[list[Any]], _RAW["blocRelations"]))
_SHOCK_BASE_PROB = {str(k): float(v) for k, v in cast(Mapping[str, Any], _RAW["shockBaseProb"]).items()}

BLOCS: Mapping[str, Bloc] = MappingProxyType(_BLOCS)
BLOC_REL: Mapping[tuple[str, str], float] = MappingProxyType(_BLOC_REL)
SHOCK_BASE_PROB: Mapping[str, float] = MappingProxyType(_SHOCK_BASE_PROB)
SOVEREIGNTY_MAX: int = int(_RAW["sovereigntyMax"])
SHOCK_NAMES: tuple[str, ...] = tuple(sorted(_SHOCK_BASE_PROB.keys()))


# ---------------------------------------------------------------------------
# Mulberry32 RNG (parity with playground JS)
# ---------------------------------------------------------------------------


class Mulberry32:
    """Port of Mulberry32 from the playground JS for cross-surface seed parity.

    Reference algorithm (TC39 modular arithmetic on uint32):
        a = (a + 0x6D2B79F5) >>> 0
        t = a
        t = imul(t ^ (t >>> 15), t | 1)
        t ^= t + imul(t ^ (t >>> 7), t | 61)
        return ((t ^ (t >>> 14)) >>> 0) / 2**32
    """

    __slots__ = ("_a",)

    _MASK32 = 0xFFFFFFFF
    _STEP = 0x6D2B79F5

    def __init__(self, seed: int) -> None:
        self._a = seed & Mulberry32._MASK32

    @staticmethod
    def _imul(a: int, b: int) -> int:
        # Math.imul: 32-bit signed multiply, return low 32 bits as unsigned.
        return (a * b) & Mulberry32._MASK32

    def next_u32(self) -> int:
        self._a = (self._a + Mulberry32._STEP) & Mulberry32._MASK32
        t = self._a
        t = Mulberry32._imul(t ^ (t >> 15), t | 1)
        t = (t ^ (t + Mulberry32._imul(t ^ (t >> 7), t | 61))) & Mulberry32._MASK32
        return (t ^ (t >> 14)) & Mulberry32._MASK32

    def next_float(self) -> float:
        return self.next_u32() / 4294967296.0


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


def sovereignty_spent(posture: frozenset[str] | tuple[str, ...] | set[str]) -> int:
    """Return the total sovereignty cost of an alliance posture."""
    return sum(BLOCS[b].sovereignty for b in posture if b in BLOCS)


def pairwise_adjustment(posture: frozenset[str] | tuple[str, ...] | set[str]) -> float:
    """Return the relationship-matrix multiplier on the surviving-fraction term.

    Sum of all pairwise weights between active blocs, mapped through
    ``clamp(1 + sum, 0.3, 1.5)``.
    """
    active = sorted(posture)
    total = 0.0
    for i, a in enumerate(active):
        for b in active[i + 1:]:
            key = (a, b) if a <= b else (b, a)
            total += BLOC_REL.get(key, 0.0)
    return max(0.3, min(1.5, 1.0 + total))


def combined_damping(
    shock: str,
    posture: frozenset[str] | tuple[str, ...] | set[str],
    *,
    trust: Mapping[str, int] | None = None,
) -> float:
    """Return surviving-fraction multiplier in [0, 1] for a shock under a posture.

    BAU (no shock) returns 1.0 unconditionally. The surviving fraction is the
    product of ``(1 - d_i)`` over each held bloc's per-shock damping, with
    trust adding up to ``+0.25`` per bloc. Three or more held blocs trigger
    the Friends Union umbrella, scaling the surviving fraction by ``0.75``.
    The pairwise relationship matrix multiplies the surviving fraction around
    1.0 (clamp 0.3..1.5), then clipped back into [0, 1].

    Cross-surface parity: this matches the JS ``combinedDamping`` in
    ``playground/microgrid_sim.js``. See ``test_diplomacy.py``
    ``test_js_python_behavioral_parity``.
    """
    if shock == "bau":
        return 1.0
    surviving = 1.0
    count = 0
    for bloc_name in posture:
        bloc = BLOCS.get(bloc_name)
        if bloc is None:
            continue
        count += 1
        base = dict(bloc.damping).get(shock, 0.0)
        if trust is not None:
            t = max(0, trust.get(bloc_name, 0))
            base = min(1.0, base + min(0.25, t * 0.05))
        if base:
            surviving *= 1.0 - base
    if count >= 3:
        surviving *= 0.75
    surviving *= pairwise_adjustment(posture)
    return max(0.0, min(1.0, surviving))


def shock_distribution(
    posture: frozenset[str] | tuple[str, ...] | set[str],
) -> dict[str, float]:
    """Return the posture-adjusted probability distribution across shocks.

    Implements **water-filling normalization**:
        1. p[s] = base[s] + sum(active bloc deltas[s])
        2. clamp p[s] >= 0
        3. iterate: pin any p[s] above 0.5 to 0.5, redistribute overflow
           uniformly across the un-pinned shocks.
        4. normalize so sum == 1.
    """
    p: dict[str, float] = dict(SHOCK_BASE_PROB)
    for bloc_name in posture:
        bloc = BLOCS.get(bloc_name)
        if bloc is None:
            continue
        for shock, delta in bloc.prob_delta:
            p[shock] = p.get(shock, 0.0) + delta
    # Clamp negatives.
    for k in list(p.keys()):
        if p[k] < 0.0:
            p[k] = 0.0
    # Water-filling above 0.5.
    cap = 0.5
    for _ in range(64):
        overflow = sum(max(0.0, v - cap) for v in p.values())
        if overflow < 1e-12:
            break
        unpinned = [k for k, v in p.items() if v < cap]
        if not unpinned:
            break
        for key in list(p.keys()):
            if p[key] > cap:
                p[key] = cap
        share = overflow / len(unpinned)
        for key in unpinned:
            p[key] += share
    # Final pin (in case last redistribution pushed someone over).
    for k, v in p.items():
        if v > cap:
            p[k] = cap
    # Normalize to 1.
    total = sum(p.values())
    if total <= 0.0:
        n = len(p) or 1
        return {k: 1.0 / n for k in p}
    return {k: v / total for k, v in p.items()}


def pick_shock(
    distribution: Mapping[str, float],
    rng: Mulberry32,
) -> str:
    """Draw a shock name from a probability distribution using the supplied RNG."""
    u = rng.next_float()
    cum = 0.0
    last_key = ""
    for key in sorted(distribution.keys()):
        cum += distribution[key]
        last_key = key
        if u < cum:
            return key
    return last_key


# ---------------------------------------------------------------------------
# Composition pipeline
# ---------------------------------------------------------------------------


def _apply_bloc_mults_to_raw(
    raw: dict[str, Any],
    posture: frozenset[str] | tuple[str, ...] | set[str],
) -> dict[str, Any]:
    """Apply each bloc's tech_capex_mult and tech_opex_mult to the raw param dict.

    Multipliers compose multiplicatively across blocs (pipeline steps 2-3).
    Capex multiplier scales ``capex_per_kw`` if present, else ``capex_per_kwh``.
    Opex multiplier scales ``opex_per_kw_yr`` if present.
    """
    out = copy.deepcopy(raw)
    for bloc_name in posture:
        bloc = BLOCS.get(bloc_name)
        if bloc is None:
            continue
        for tech, mult in bloc.bonus.tech_capex_mult:
            if tech not in out:
                continue
            for fld in ("capex_per_kw", "capex_per_kwh"):
                if fld in out[tech]:
                    out[tech][fld]["value"] *= mult
                    out[tech][fld]["range_low"] *= mult
                    out[tech][fld]["range_high"] *= mult
        for tech, mult in bloc.bonus.tech_opex_mult:
            if tech not in out:
                continue
            if "opex_per_kw_yr" in out[tech]:
                out[tech]["opex_per_kw_yr"]["value"] *= mult
                out[tech]["opex_per_kw_yr"]["range_low"] *= mult
                out[tech]["opex_per_kw_yr"]["range_high"] *= mult
    return out


def _materialise(shocked: dict[str, Any]) -> dict[str, ParamSet]:
    out: dict[str, ParamSet] = {}
    for tech, fields in shocked.items():
        parsed: dict[str, Param] = {}
        for fname, body in fields.items():
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


def _diplomacy_capex_total(posture: frozenset[str] | tuple[str, ...] | set[str]) -> float:
    return sum(BLOCS[b].cost for b in posture if b in BLOCS)


def _bonus_aggregates(
    posture: frozenset[str] | tuple[str, ...] | set[str],
) -> tuple[float, float, float]:
    """Return (lcoh_mult, availability_add, ptc_rebate) summed across blocs."""
    lcoh = 1.0
    avail = 0.0
    ptc = 0.0
    for b in posture:
        bloc = BLOCS.get(b)
        if bloc is None:
            continue
        lcoh *= bloc.bonus.lcoh_mult
        avail += bloc.bonus.availability_add
        ptc += bloc.bonus.ptc_capex_rebate_pct
    return lcoh, avail, ptc


def _shock_dampened_params(
    base_raw_with_blocs: dict[str, Any],
    shock: str,
    surviving: float,
) -> dict[str, ParamSet]:
    """Apply shock multipliers reduced by ``surviving`` fraction.

    A shock multiplier ``m`` becomes ``1 + (m - 1) * (1 - surviving_inv)``? No:
    interpretation here is that ``surviving`` already denotes the *fraction of
    shock that survives the umbrella*. So the effective multiplier is
    ``1 + (m - 1) * surviving``. surviving=1 -> full shock; surviving=0 -> bau.
    """
    if shock == "bau" or surviving <= 0.0:
        return _materialise(base_raw_with_blocs)
    profile = PROFILES.get(shock, [])
    if not profile:
        return _materialise(base_raw_with_blocs)
    out = copy.deepcopy(base_raw_with_blocs)
    for path, mult in profile:
        tech, _, fld = path.partition(".")
        if tech not in out or fld not in out[tech]:
            continue
        eff = 1.0 + (mult - 1.0) * surviving
        out[tech][fld]["value"] *= eff
        out[tech][fld]["range_low"] *= eff
        out[tech][fld]["range_high"] *= eff
    return _materialise(out)


def _evaluate_year(
    *,
    posture: frozenset[str],
    shock: str,
    build: str,
    raw_with_blocs: dict[str, Any],
    bonus_lcoh: float,
    bonus_avail: float,
    bonus_ptc: float,
    diplomacy_capex: float,
    target_avail: float,
    capex_cap: float,
    trust: Mapping[str, int] | None,
    debug: bool,
) -> YearResult:
    surviving = 1.0 - combined_damping(shock, posture, trust=trust)
    materialised = _shock_dampened_params(raw_with_blocs, shock, surviving)
    r = evaluate_district(build, params=materialised, envelope_usd=capex_cap)

    capex_after_blocs = sum(r.capex_breakdown.values())  # includes bloc multipliers via params
    capex_after_shock = r.capex_total_usd
    capex_total = capex_after_shock + diplomacy_capex
    capex_total *= 1.0 - bonus_ptc
    avail_baseline = 0.92  # teaching-grade headline availability
    if surviving > 0.0:
        avail_baseline -= 0.05 * surviving
    availability = min(1.0, avail_baseline + bonus_avail)
    lcoh = r.lcoh_per_kg * bonus_lcoh

    score = 0.0
    if availability >= target_avail:
        score += 50.0
    if capex_total <= capex_cap:
        score += 30.0
    score += max(0.0, 20.0 * (1.0 - lcoh / 12.0))

    dbg = None
    if debug:
        trust_bonus = 0.0
        if trust is not None:
            for b in posture:
                trust_bonus += min(0.25, max(0, trust.get(b, 0)) * 0.05)
        dbg = YearDebug(
            surviving_fraction_pre_shock=surviving,
            capex_after_blocs=capex_after_blocs,
            capex_after_shock=capex_after_shock,
            trust_damping_bonus=trust_bonus,
        )

    return YearResult(
        year=0,  # set by caller
        shock=shock,
        capex_total=capex_total,
        lcoh=lcoh,
        availability=availability,
        score=score,
        debug=dbg,
    )


# ---------------------------------------------------------------------------
# Top-level: simulate_campaign + monte_carlo
# ---------------------------------------------------------------------------


def _normalize_posture(
    posture: frozenset[str] | tuple[str, ...] | set[str] | list[str],
) -> frozenset[str]:
    fs = frozenset(posture)
    unknown = fs - BLOCS.keys()
    if unknown:
        raise ValueError(f"unknown bloc(s): {sorted(unknown)}")
    if sovereignty_spent(fs) > SOVEREIGNTY_MAX:
        raise ValueError(
            f"posture sovereignty {sovereignty_spent(fs)} exceeds cap {SOVEREIGNTY_MAX}"
        )
    return fs


@lru_cache(maxsize=8)
def _raw_params_cached() -> dict[str, Any]:
    # Re-uses scenarios._raw_params_cached underlying YAML via _params_with_shock("bau")?
    # That returns ParamSet, not raw. Load fresh raw YAML once here; no shock yet.
    import yaml  # local to keep top-level imports tight

    from .paths import DATA_DIR
    with (DATA_DIR / "tech_params.yaml").open() as f:
        return cast(dict[str, Any], yaml.safe_load(f))


# Trust dynamics (code constants; not part of the constants-triple stamp).
# Maintained blocs gain trust; unmaintained held blocs decay toward zero. The
# headless surfaces treat every held bloc as maintained every year, so trust
# grows monotonically and Monte Carlo distributions are unchanged. The JS
# interactive campaign decides maintenance per year via decision cards, where
# neglecting a bloc lets its trust erode. Mirrors microgrid_sim.js.
TRUST_MAINTAIN_GAIN = 1
TRUST_DECAY = 1


def _update_trust(
    trust: dict[str, int],
    posture: frozenset[str],
    maintained: frozenset[str],
) -> None:
    """Apply one year of trust change in place: maintained blocs gain, the rest decay."""
    for b in posture:
        if b in maintained:
            trust[b] = trust.get(b, 0) + TRUST_MAINTAIN_GAIN
        else:
            trust[b] = max(0, trust.get(b, 0) - TRUST_DECAY)


def simulate_campaign(
    posture: frozenset[str] | tuple[str, ...] | set[str] | list[str],
    *,
    build: str = "district_solar_h2_inland",
    years: int = 5,
    seed: int = 0,
    target_avail: float = 0.95,
    capex_cap: float = 36e6,
    debug: bool = False,
) -> CampaignResult:
    """Simulate a 5-year (default) campaign under a posture, returning per-year scores.

    Deterministic given (posture, seed, build, years). Does not mutate inputs.
    """
    fs = _normalize_posture(posture)
    raw = _raw_params_cached()
    raw_with_blocs = _apply_bloc_mults_to_raw(raw, fs)
    bonus_lcoh, bonus_avail, bonus_ptc = _bonus_aggregates(fs)
    diplomacy_capex = _diplomacy_capex_total(fs)
    rng = Mulberry32(seed)
    dist = shock_distribution(fs)

    trust: dict[str, int] = {b: 0 for b in fs}
    year_results: list[YearResult] = []
    total_score = 0.0
    for y in range(1, years + 1):
        shock = pick_shock(dist, rng)
        yr = _evaluate_year(
            posture=fs,
            shock=shock,
            build=build,
            raw_with_blocs=raw_with_blocs,
            bonus_lcoh=bonus_lcoh,
            bonus_avail=bonus_avail,
            bonus_ptc=bonus_ptc,
            diplomacy_capex=diplomacy_capex,
            target_avail=target_avail,
            capex_cap=capex_cap,
            trust=trust,
            debug=debug,
        )
        year_results.append(
            YearResult(
                year=y,
                shock=yr.shock,
                capex_total=yr.capex_total,
                lcoh=yr.lcoh,
                availability=yr.availability,
                score=yr.score,
                debug=yr.debug,
            )
        )
        total_score += yr.score
        # Headless: every held bloc is maintained, so trust grows monotonically.
        _update_trust(trust, fs, maintained=fs)

    return CampaignResult(
        posture=tuple(sorted(fs)),
        seed=seed,
        years=tuple(year_results),
        total_score=total_score,
    )


def monte_carlo(
    posture: frozenset[str] | tuple[str, ...] | set[str] | list[str],
    *,
    build: str = "district_solar_h2_inland",
    years: int = 5,
    runs: int = 1000,
    seed: int = 0,
    target_avail: float = 0.95,
    capex_cap: float = 36e6,
) -> MonteCarloSummary:
    """Run ``runs`` independent campaigns (varying seed) and summarize total scores.

    Precomputes the bloc-bonus-applied raw params and bonus aggregates once,
    outside the inner loop, per audit item 16. Per-shock evaluations are also
    memoized (the trust counter has no effect when ``debug=False`` and trust
    only matters via ``combined_damping``, which we recompute per year, but the
    *un-trusted* shock evaluation is identical across years/runs for a fixed
    posture and shock name).
    """
    fs = _normalize_posture(posture)
    raw = _raw_params_cached()
    raw_with_blocs = _apply_bloc_mults_to_raw(raw, fs)
    bonus_lcoh, bonus_avail, bonus_ptc = _bonus_aggregates(fs)
    diplomacy_capex = _diplomacy_capex_total(fs)
    dist = shock_distribution(fs)

    # Cache (shock, trust_signature) -> YearResult, keyed on the actual trust map
    # so it stays correct under any trust path (including decay), not just the
    # monotonic one. Trust effect saturates above 5 (min(0.25, t*0.05)).
    cache: dict[tuple[str, tuple[tuple[str, int], ...]], YearResult] = {}

    def _cached_year(shock: str, trust: Mapping[str, int]) -> YearResult:
        sig = tuple(sorted((b, min(trust.get(b, 0), 5)) for b in fs))
        key = (shock, sig)
        hit = cache.get(key)
        if hit is not None:
            return hit
        yr = _evaluate_year(
            posture=fs,
            shock=shock,
            build=build,
            raw_with_blocs=raw_with_blocs,
            bonus_lcoh=bonus_lcoh,
            bonus_avail=bonus_avail,
            bonus_ptc=bonus_ptc,
            diplomacy_capex=diplomacy_capex,
            target_avail=target_avail,
            capex_cap=capex_cap,
            trust=trust,
            debug=False,
        )
        cache[key] = yr
        return yr

    scores: list[float] = []
    for run_ix in range(runs):
        rng = Mulberry32(seed + run_ix)
        trust: dict[str, int] = {b: 0 for b in fs}
        total = 0.0
        for _ in range(years):
            shock = pick_shock(dist, rng)
            yr = _cached_year(shock, trust)
            total += yr.score
            _update_trust(trust, fs, maintained=fs)
        scores.append(total)

    scores_sorted = sorted(scores)
    n = len(scores_sorted)

    def _pct(p: float) -> float:
        if n == 0:
            return float("nan")
        ix = max(0, min(n - 1, int(round(p * (n - 1)))))
        return scores_sorted[ix]

    mean = sum(scores) / n if n else float("nan")
    std = statistics.pstdev(scores) if n > 1 else 0.0
    return MonteCarloSummary(
        posture=tuple(sorted(fs)),
        runs=runs,
        years=years,
        seed=seed,
        mean=mean,
        std=std,
        p10=_pct(0.10),
        p50=_pct(0.50),
        p90=_pct(0.90),
        min=scores_sorted[0] if n else float("nan"),
        max=scores_sorted[-1] if n else float("nan"),
    )


# ---------------------------------------------------------------------------
# Hash for reproducibility stamp
# ---------------------------------------------------------------------------


def diplomacy_hash() -> str:
    """Return a 12-char sha256 prefix of the constants triple, for the JSON stamp."""
    payload = repr(_BLOCS) + repr(_BLOC_REL) + repr(_SHOCK_BASE_PROB)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


# Re-bind unused imports defensively so pyright sees them used.
_ = math
_ = field
