# Backlog

> **Disclaimer.** Engineering backlog notes. Not financial, legal, engineering, or tax advice. See `DISCLAIMER.md`.

Items deferred from completed phases. Each entry: title, rationale for deferral, expected
effort, blast-radius note, and target phase if known.

## Item 9 - Money/currency type (item 9 in the Phase 2 audit)

**Rationale for deferral.** A `Money` type with explicit currency tagging would prevent
silent unit confusion when scenarios in different jurisdictions are compared. The right
implementation touches every cost path: `lcoe.py`, `tco.py`, `scenarios.py`,
`finance.py`, `render.py`, `packaging.py`. That is wide. Phase 3 already lands a
tech-registry refactor and a strict pyright pass; bundling Money on top of those raises
the regression surface beyond what one phase can absorb.

**Expected effort.** 3 to 4 working days. Roughly: define `Money(value, currency)` and
`FxContext`; thread the type through the public API as input/output; keep internal
arithmetic on scalars. The CLI gains a `--currency` flag; output prints the currency.
Tests assert that mixing currencies without an FxContext raises rather than coerces.

**Blast radius.** All currency-bearing paths. Failure mode: a silent unit conversion
breaks an already-published scenario number. Mitigation: lock numbers in a snapshot test
before the refactor and assert byte-equality after.

**Target phase.** Phase 4. Bundle with multi-currency grant packaging (ARENA in AUD, EECA
in NZD, Innovation Fund in EUR) so the user value is visible.

## mutmut roll-out beyond `lcoe.py`

**Rationale for deferral.** Phase 3 runs mutmut on `lcoe.py` only as a pilot. If the
pilot survival rate is low and no genuine gap surfaces, the test suite is mature enough
that scaling mutmut to `finance.py`, `scenarios.py`, `supply.py` is low return. If the
pilot finds genuine gaps, the prudent next step is to fix them, not to scale mutmut.

**Expected effort.** Hours per module to run; days per genuine gap to fix.

**Target phase.** Decision after Phase 3 Track F results land in `docs/mutation_baseline.md`.

<!-- CI workflow item resolved in Phase 3: shipped at .github/workflows/ci.yml. -->


## uv migration (faster than pip-tools)

**Rationale for deferral.** Phase 3 generates `requirements.lock` via pip-tools because
it is well-known and stable. uv produces a compatible lockfile and is faster, but
switching is a separate decision and should not be bundled with conventions work.

**Expected effort.** A few hours including documentation update.

**Target phase.** When the team chooses.

## Docker image and PyPI publish

**Rationale for deferral.** The project is currently a single-author research repo. A
container image and a PyPI release add packaging surface that is not yet justified.

**Target phase.** When external distribution becomes a concrete need.
