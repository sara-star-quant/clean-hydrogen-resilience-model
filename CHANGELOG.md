# Changelog

> **Disclaimer.** Project history record. Not financial, legal, engineering, or tax advice. See [DISCLAIMER.md](DISCLAIMER.md).

All notable changes to this project. Format follows the spirit of Keep a Changelog. Dates
are in ISO 8601. Versions follow semantic versioning where the public surface is the
Python package (`electicity_model`) and the CLI command (`electicity`).

## [0.5.0] - 2026-06-19

Playground feature track plus diplomacy realism. Version bumped from 0.4.0 to 0.5.0 for the
new shareable playground surfaces (save/share, local leaderboard), the trust
decay/defection/retaliation mechanics mirrored across `microgrid_sim.js` and `diplomacy.py`,
and the refreshed dependency floors. The headless Monte Carlo distributions are unchanged.

### Added
- Playground save and share: "Copy share link" encodes build, posture, region, toggles, and
  challenge index into a versioned URL hash that reopens the exact scenario. No backend.
- Playground local leaderboard: best score per challenge or campaign in localStorage; each row
  reloads the build that earned it. Score payload is share-link compatible.
- Diplomacy realism: trust now decays on neglected blocs, a bloc ground to zero trust defects
  (no protection that year), and defection triggers retaliation that raises hostile-shock odds.
  Implemented in both `microgrid_sim.js` and `diplomacy.py`; the headless Monte Carlo treats a
  fixed posture as always maintained, so its distributions are unchanged.
- Four decision cards: EAST FRIEND re-export (betrayal), retaliation risk plus a chained
  aftermath, and alliance upkeep. Card total 16 to 20.
- [REFRESH.md](REFRESH.md) gate recording dependency pins and the data/citation refresh checklist.
- [grants/CALL_TRACKER.md](grants/CALL_TRACKER.md), [grants/PARTNER_ONEPAGER.md](grants/PARTNER_ONEPAGER.md), and `grants/letters/` (LOI template
  plus status tracker).
- Explicit user-responsibility clause in [DISCLAIMER.md](DISCLAIMER.md): the user is solely responsible for
  deployment and all actions and outcomes from using the software, model, or outputs.

### Changed
- Version bumped to 0.5.0 across the authoritative source (`electicity_model.__version__`),
  packaging, citation, the playground footer and export stamp, and the regenerated
  [report/_generated_tables.md](report/_generated_tables.md).
- Dependency floors pinned to latest verifiable as of 2026-06-19 (pyyaml 6.0.3, matplotlib
  3.11, pytest 9.1, pytest-cov 7.1, hypothesis 6.155, openpyxl 3.1.5, python-pptx 1.0.2,
  python-docx 1.2, setuptools 82); pre-commit-hooks v5 to v6.
- `monte_carlo` cache now keys on the actual trust map rather than a synthesized monotonic
  one, so it stays correct under trust decay. Distributions are unchanged.
- Slider drags coalesce to one render per animation frame; leaderboard writes only on an
  improved score.

## [0.4.0] - 2026-05-05

Phase 3: conventions baseline plus follow-on tracks. Repository made publication-ready.
Version bumped from 0.3.0 to 0.4.0 because Phase 3 added a new CLI subcommand
(`package`), a behaviour-preserving refactor of the cost path (`tech_registry.py`),
strict pyright as a CI gate, a real CI workflow at `.github/workflows/ci.yml`,
pre-commit and Make-based developer ergonomics, and the full governance set for public
release.

### Added
- `model/src/electicity_model/constants.py` for cross-module physical constants.
- `model/src/electicity_model/paths.py` for repository path discovery.
- `model/src/electicity_model/tech_registry.py` (Track B): registry-driven district
  capex and opex computation. Adding a tech is one row in the registry.
- `model/src/electicity_model/packaging.py` (Track C): `electicity package --scheme X`
  bundles a scheme-specific submission archive with a budget XLSX (or CSV fallback) and
  a manifest.json carrying sha256 per file.
- `model/requirements.lock` (Track D) pinned via pip-compile.
- `pyrightconfig.json` (Track E) for static type checking. The package passes pyright
  strict with zero errors and ten or fewer suppressions, all matplotlib-stubs-related.
- `model/src/electicity_model/py.typed` marker (PEP 561).
- New CLI subcommand: `electicity package`.
- New tests: `test_tech_registry.py` (registry shape and basic outputs),
  `test_packaging.py` (archive creation, manifest sha256, CSV fallback, byte-stable
  output across runs).
- `LICENSE` (Apache License 2.0) for code, `LICENSE-DOCS` (CC BY 4.0) for documentation
  and data.
- [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), `CITATION.cff`.
- [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md), [.github/ISSUE_TEMPLATE/bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md),
  [.github/ISSUE_TEMPLATE/feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md).
- [BACKLOG.md](BACKLOG.md) recording deferred work (Money type, mutmut roll-out, CI workflow
  install).
- [CHANGELOG.md](CHANGELOG.md) split out of README.
- `.pre-commit-config.yaml` with the non-ASCII scanner, the tech-params schema check,
  fast pytest, and pyright strict on commit; full pytest on push.
- `Makefile` with `install`, `test`, `test-fast`, `test-perf`, `coverage`, `lint`,
  `scan`, `render`, `summary`, `publish-check`, `precommit-install`, `clean` targets.
- [docs/mutation_baseline.md](docs/mutation_baseline.md) documenting the deferred mutmut pilot and the rationale.

### Changed
- `H2_LHV_KWH_PER_KG`, `HOURS_PER_YEAR`, `KM_PER_MILE`, `DIESEL_LHV_KWH_PER_L` consumed
  from `constants.py` rather than redefined in module scope.
- `DATA_DIR`, `ASSETS`, `REPORT` resolved from `paths.py`.
- 30 public defs gained one-line docstrings stating intent.
- `__all__` declarations added to every module with a public surface.
- Coverage gate raised from 80 to 85 percent. Current coverage is 92 percent across the
  package, with `lcoe.py`, `tco.py`, `scenarios.py`, `regions.py`, and `tech.py` at 95
  percent or above.
- Investor memo, economics chapter, and grant budget tables tightened with explicit
  "indicative scenario output, not a forecast" captions and named-peer comparators
  replaced by class-level bands.
- README rewritten with a Licence section, a Project governance section, and a
  Publishing checklist.
- CONTRIBUTING.md updated with the Makefile entry points and the pre-commit install
  step.
- Playground tooltip system: hover-preview removed (it was truncating with "..."
  even when the popover had room); click-to-pin remains as the single source for the
  full content. Tooltip body adopts a callout style for tips and warnings, with
  highlighted key terms and tabular numbers.
- Playground onboarding "How scores work" tab rewritten in plain language for a wide
  audience.
- "Cyber safety on" toggle and tooltip rephrased to mention Zero Trust Architecture
  without awkward language.

### Removed
- Em-dash characters from source string literals in `render.py`, `lcoe.py`, `supply.py`.
- Unused `Path` import in `scenarios.py`, `field` import in `regions.py`, `Callable`
  import in `sensitivity.py`.
- Legacy `_district_capex` and `_district_annual_opex` if/elif paths from
  `scenarios.py` after Track B stage 1 proved byte-equivalence with the registry.
- Hard-coded absolute `/Users/peterz/...` paths in committed markdown files.

### Security and publishing
- [DISCLAIMER.md](DISCLAIMER.md) covers not-financial-advice, not-legal-advice, not-a-fundraising-
  solicitation, no-warranty, no-liability.
- Banner referencing the disclaimer is on every customer-facing markdown file.
- Repository is structured for publication on GitHub. The CI workflow ships at
  `.github/workflows/ci.yml` with jobs for pytest+coverage, pytest perf, pyright
  strict, and the non-ASCII scan.

## [0.2.0] - 2026-05-05

Phase 2: supply resilience, ZTA, performance hardening.

### Added
- Supply-shock framework with 9 profiles (`bau`, `ir_shortage`, `pt_shortage`,
  `li_shortage`, `china_decoupling`, `triple_squeeze`, `western_only`,
  `maritime_blockade`, `regional_autarky`). Math contract: each multiplier acts on its
  own YAML line, never on aggregate.
- 4 new tech-params entries: `aem_electrolyzer`, `lfp_battery_grid`, `na_ion_battery_grid`,
  plus baseload trio `smr_nuclear`, `micro_reactor`, `geothermal_egs`, `biomass_chp`.
- 3 new scenarios: `district_autonomy_max`, `district_no_solar_no_wind`,
  `district_smr_baseload`.
- `regions.py` with 12 candidate regions across EU/US/AU/NZ scored on a 6-axis 0-5 rubric.
- `finance.py` with NPV, IRR (Newton plus bisection fallback), payback, annuity factor,
  cashflow series.
- New CLI subcommands: `shock`, `regions`, `finance`, `package`.
- New report chapters: [report/10_supply_resilience_and_regions.md](report/10_supply_resilience_and_regions.md),
  [report/11_extreme_threats_and_zta_zte.md](report/11_extreme_threats_and_zta_zte.md).
- New [investor_memo.md](investor_memo.md) (financial register, separate from research register).
- New `playground/microgrid_sim.html` browser sim-game with baked params.
- LRU caches on raw YAML, scenarios YAML, and `_params_with_shock`.
- Schema validation for `tech_params.yaml` (`ParamSchemaError`).
- Golden-file regression on rendered tables.
- `pytest-cov` gate at 80 percent coverage. Achieved 93 percent.
- `mutmut` and `pip-tools` dev dependencies.

### Changed
- References bumped to 2025/2026 vintages: `IEA-GHR-2025`, `IRENA-RPGC-2024`,
  `NREL-ATB-2025`, `USGS-MCS-2026`, `IEA-CMO-2025`. Older keys retained for traceability.
- Library versions: `pytest >= 9`, `matplotlib >= 3.10`. Optional `[export]` extra adds
  `openpyxl`, `python-pptx`, `python-docx`.
- Test count: 17 to 151. Test runtime: 4.71s to 2.91s.

## [0.1.0] - 2026-05-05

Phase 1: initial shipment.

### Added
- Cost-and-feasibility model in `model/src/electicity_model/`: `tech.py`, `lcoe.py`,
  `tco.py`, `scenarios.py`, `sensitivity.py`, `render.py`, `cli.py`.
- Tech parameter database with provenance: `model/data/tech_params.yaml`.
- Validation gates V1 to V6 (utility solar LCOE, PEM LCOH unsubsidised, PEM LCOH with
  IRA section 45V, FCEV per-mile fuel cost, district hybrid economics, pumped hydro LCOS).
- Report chapters 00 to 09 covering executive summary, problem, technology landscape,
  car track, district track, economics, environmental, risk, roadmap, fringe-tech
  appendix.
- 6 grant proposal templates (Horizon Europe, EU Innovation Fund, ARPA-E, DOE H2
  programs, ARENA, EECA/Callaghan).
- Marp pitch deck.
- [report/references.md](report/references.md) bibliography with citation keys.
