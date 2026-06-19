# Mutation testing baseline

## Status: deferred, not gated

The Phase 3 plan called for a mutmut pilot on `model/src/electicity_model/lcoe.py`. The
attempt landed against two ecosystem issues:

1. `mutmut < 3` fails on Python 3.14 with a serialization error during the runner's
   deepcopy (the underlying `itertools.count` object cannot be deep-copied under 3.14).
   The 2.x line was last released before 3.14 shipped.
2. `mutmut >= 3` rewrote its runner to copy the tested package into a `mutants/`
   directory and re-run pytest from that layout. The default copy strategy does not
   resolve our editable install correctly, so test collection fails with
   `ModuleNotFoundError: No module named 'electicity_model.tech'`.

Either path is fixable, but neither is a 30-minute fix on a project with this layout.
mutmut was always positioned as diagnostic, never a CI gate, so this baseline is
deferred without blocking Phase 3.

## What we rely on instead

Direct evidence of test quality:

- Line coverage: `lcoe.py` 98 percent, `tco.py` 97 percent, `scenarios.py` 97 percent,
  `tech_registry.py` 93 percent, `finance.py` 75 percent. Total package coverage 92
  percent.
- Validation gates V1 through V6 in `tests/test_lcoe.py` and `tests/test_tco.py` pin
  outputs against published reference cases (IRENA, IEA, NREL ATB, DOE).
- Monotonicity invariants in `tests/test_lcoe_invariants.py` cover directional
  sensitivity of LCOE to capex, opex, capacity factor, lifetime, electrolyzer
  efficiency, and electricity price.
- Edge-case tests in `tests/test_lcoe_edges.py` cover zero-energy, zero-lifetime,
  negative-discount, very-long-lifetime, and full-credit-yields-negative-LCOH paths.

## How to retry when the ecosystem catches up

```
# Option A: pin a Python the 2.x line still supports as a one-shot diagnostic.
python3.12 -m venv .venv-mutmut
.venv-mutmut/bin/pip install "mutmut<3" pyyaml matplotlib pytest
.venv-mutmut/bin/pip install -e model
cd model && ../.venv-mutmut/bin/mutmut run

# Option B: mutmut 3.x with a wrapper that puts model/src on sys.path before pytest
# collects. Open question upstream; revisit when resolved.
```

## What to record when the pilot eventually succeeds

- Total mutants generated.
- Killed, survived, timeout, suspicious counts.
- Specific surviving mutants with one-line description and verdict
  (genuine gap, semantically equivalent, or intentional behaviour).
- Decision rule:
  - Survival rate under 10 percent and no genuine gap survives: pilot done.
  - Survival rate at or above 10 percent OR a genuine gap survives: file a follow-on
    test task per gap.
- mutmut still does not gate CI. Diagnostic only.
