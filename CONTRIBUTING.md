# Contributing

> **Disclaimer.** This is a research and modelling project. See `DISCLAIMER.md`.

Thanks for considering a contribution. The project is small and the bar for changes is
clear: every quantitative claim cites a public source, and every code change keeps the
test suite green.

## Quickstart

```
git clone <fork-url>
cd electicity
make install               # one-line setup of the model venv with dev deps
make test-fast             # ~3 seconds, CI-friendly subset
make precommit-install     # wire the git pre-commit and pre-push hooks
```

If you prefer the Python tooling directly:

```
cd model
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Expect 173+ tests passing in under 4 seconds. Coverage gate is 80 percent.

## Git hooks

The repository ships a `.pre-commit-config.yaml`. After `make precommit-install`, every
commit runs the non-ASCII scanner, the tech-params schema check, the fast pytest subset,
and pyright strict. Every push runs the full pytest suite including perf and regression
marks. Skip the hooks only with explicit reason via `git commit --no-verify`.

For pinned-version installs (recommended for CI and reproducibility):

```
pip install -r model/requirements.lock
```

## How to run common tasks

```
pytest                                  # full suite including perf and regression marks
pytest -m 'not perf and not regression' # fast subset (CI-friendly)
pytest --cov=electicity_model           # with coverage report
pyright --project pyrightconfig.json    # static type check, must return 0 errors

electicity district --scenario district_solar_h2_inland
electicity district --scenario district_solar_h2_inland --shock triple_squeeze
electicity car --scenario car_fcev_class8 --h2-price 4.0
electicity render-all                   # regenerate report tables and chart PNGs
electicity summary --out _summary.json  # machine-readable JSON snapshot
```

## How to propose a new technology

The shortest path: one row in `model/data/tech_params.yaml` and one row in
`model/src/electicity_model/tech_registry.py`. Walk-through:

1. Add the parameter block to `model/data/tech_params.yaml`. Every field needs `value`,
   `range_low`, `range_high`, `unit`, `year`, `source`. The `source` value must be a
   citation key already declared in `report/references.md`. If the source is new, add it
   to `references.md` first.
2. Add a `TechSpec(...)` row to the `DISTRICT_TECHS` list in `tech_registry.py`. Pick the
   right `CapexBasis` (PER_KW, PER_KWH, or PER_KG). Set `params_key_scenario_field` and
   `params_key_default` if the chemistry or sub-type can vary by scenario.
3. Add the new key to one or more scenarios in `model/data/scenarios.yaml`.
4. Run `pytest`. The data-integrity test verifies the citation key resolves; the registry
   tests verify the new row does not collide with existing labels; the equivalence test
   verifies the registry path matches the legacy formula (until Track B stage 2 lands).
5. Run `electicity district --scenario <new>` to confirm it computes.
6. Update `CHANGELOG.md` under "Unreleased" with one line describing the addition.
7. Open a pull request with a short summary and a link to the source publication for the
   new numbers.

## How to propose a new shock profile

1. Add a profile entry to `PROFILES` in `model/src/electicity_model/supply.py`. Each
   entry is a list of `(yaml.path, multiplier)` tuples. Multipliers act on the named
   tech and field only, never on aggregates.
2. Add a parametrised test case to `model/tests/test_supply_shock.py`.
3. Add a tooltip entry for the playground at the matching `data-info-id` slug
   (`shock-<profile_name>`) in `playground/microgrid_sim.html`. Plain ASCII, no em-dashes.
4. Run `pytest` and `python3 docs/scan_non_ascii.py`.

## Commit and pull-request guidelines

- One logical change per pull request.
- Title in imperative voice, around 50 characters.
- Body explains the why and references issue numbers if any.
- Include a `tests:` line listing new or updated tests.
- Include a `docs:` line if you touched markdown.
- Cite a public source for any new quantitative claim. Citations live in
  `report/references.md`.

## Style

- Python: pyright strict mode, 80 percent coverage, no em-dashes in source string
  literals, ASCII-only in customer-facing markdown.
- Tests: descriptive `test_*` names. Use `pytest.approx` for float comparisons. Use
  `@pytest.mark.perf` for any test that times more than 100 ms.
- Documents: research-paper voice for `report/`, financial-advisor voice for
  `investor_memo.md`, professional tech-writer voice for the playground. Always plain
  ASCII. The lint script `docs/scan_non_ascii.py` is a hard gate.

## Reporting bugs and suggesting features

See `.github/ISSUE_TEMPLATE/` for templates. For security issues see `SECURITY.md` and do
not file a public issue.

## Code of Conduct

This project follows the Contributor Covenant 2.1. See `CODE_OF_CONDUCT.md`.
