# Clean Hydrogen Resilience Model (Electicity)

> **Disclaimer.** This is a research and modelling project, not financial, legal, engineering, or tax advice, and not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

Open techno-economic model for green hydrogen via electrolysis from renewables, with two grounded deployment tracks (a Class 8 FCEV truck bench-validation and a 2 MW district hybrid microgrid) and a supply-chain resilience simulation. Reports LCOE, LCOH, and per-km TCO with reproducible, stamped artifacts.

## Diplomacy as a strategic layer (a research and simulation instrument)

This is a research and visualization instrument, not a fundraising pitch. It lets a player or researcher explore the long-run reliability of an energy stack under different inter-regional alliance postures and counter-actions, with both an interactive browser surface and a batch Monte Carlo CLI.

Resilience for this stack is not a unilateral problem. Iridium and platinum concentrate in southern Africa, lithium mining in Australia and Chile, cell processing in China, alkaline-electrolyser OEM capacity in Norway, Germany, and France. No jurisdiction builds the 2 MW district at target LCOE under hard decoupling. The project therefore treats coalition design as a first-class engineering input alongside capex, LCOE, and availability.

The browser playground (`playground/microgrid_sim.html`) ships a "Friends Union" panel with seven blocs (`EU_FRIEND`, `WEST_FRIEND`, `EAST_FRIEND`, `SOUTH_CENTRAL_FRIEND`, `NORTH_FRIEND`, `AFRICA_FRIEND`, `LATAM_FRIEND`). Each bloc has a fixed diplomatic capex cost, a sovereignty cost (cap of 10), per-shock damping, baseline economic bonuses, and probability deltas that shift which shocks become more or less likely. Six pairwise relationships add synergy or friction between active blocs. A 5-year campaign mode draws stochastic shocks weighted by your posture and accumulates trust that erodes on neglected blocs: a bloc ground to zero trust defects (no protection that year) and invites retaliation that raises hostile-shock odds. It threads 20 hand-authored decision cards (including multi-year follow-up chains, 2 research-funding cards for shortage-hedge breakthroughs, and betrayal, retaliation, and alliance-upkeep events).

For batch analysis, the Python source-of-truth module `electicity_model.diplomacy` runs the same logic headlessly. The CLI exposes a Monte Carlo subcommand:

```
electicity diplomacy --posture WEST_FRIEND,LATAM_FRIEND --years 5 --runs 1000
electicity diplomacy --compare WEST_FRIEND,LATAM_FRIEND vs WEST_FRIEND,EAST_FRIEND,LATAM_FRIEND --runs 2000 --json out.json
```

Both surfaces share a single source of truth: the JSON constants block embedded in `microgrid_sim.html` and parsed by the Python module via `pathlib`. A behavioral parity test in `tests/test_diplomacy.py` runs both implementations against fixed fixtures and asserts they agree to 1e-9, so JS and Python cannot drift silently.

The teaching point is the asymmetry: friendship has a real bill, and the bill is small compared to surviving a shock alone. The model preserves the real jurisdictional names because grants and academic citations require them; the bloc tags (`friend_bloc` on each `Region`) sit alongside the geography rather than replacing it.

## Two budget envelopes

| Track | Budget cap | Duration | What it buys |
|---|---|---|---|
| Car bench-validation | under $1M | 24 months | Class 8 FCEV powertrain test rig, fuel-cell stack characterization, drive-cycle and TCO validation against diesel and BEV baselines. |
| District hybrid microgrid | under $36M | 36 months | 2 MW renewable primary (solar / micro-hydro / tidal), PEM electrolyzer, H2 storage and distribution, fuel-cell genset for firming, instrumented field deployment. |

## Honest framing

Water is the **carrier**, not the primary energy source. The chain runs renewable electricity to PEM electrolysis to H2 storage to fuel-cell reconversion (or direct combustion in the FCEV). Round-trip efficiency and capex are reported transparently in the model and chapter 04.

Only grounded technology sits in the investable envelope. LENR and "cold fusion" claims are surveyed in `report/09_lenr_appendix.md` and rated **not investable** per the calorimetry-and-reproducibility critique in [Berlinguette-2019]. They appear in the appendix for completeness, not in the budget.

## Repository layout

```
electicity/
|-- README.md                  # this file
|-- investor_memo.md           # 6-10 page investor memo (financial register)
|-- report/                    # research report (markdown chapters, research register)
|   |-- 00_executive_summary.md
|   |-- 01..08_*.md            # main chapters
|   |-- 09_appendix_fringe_tech.md  # LENR / "water-as-fuel", rated not investable
|   |-- 10_supply_resilience_and_regions.md  # critical-minerals + autonomous regions
|   |-- 11_extreme_threats_and_zta_zte.md    # weather-immune mix + Zero-Trust spec
|   |-- _generated_tables.md   # model-rendered numbers; do not edit
|   `-- references.md          # bibliography ([Citation-Key] -> source)
|-- model/                     # Python 3.14 cost-and-feasibility model
|   |-- pyproject.toml         # requires-python >=3.14; deps pyyaml/matplotlib
|   |-- src/electicity_model/  # tech.py, lcoe.py, tco.py, scenarios.py,
|   |                          #   sensitivity.py, supply.py, regions.py,
|   |                          #   finance.py, render.py, cli.py
|   |-- data/                  # tech_params.yaml, scenarios.yaml
|   `-- tests/                 # pytest, 223 tests
|-- deck/
|   |-- pitch.md               # Marp source for VC deck
|   `-- assets/                # rendered charts (regenerated from model)
|-- grants/                    # 6 grant-proposal templates
|   |-- eu_horizon_europe_cluster5.md
|   |-- eu_innovation_fund.md
|   |-- us_arpa_e.md
|   |-- us_doe_h2_programs.md
|   |-- au_arena.md
|   |-- nz_eeca_callaghan.md
|   `-- _shared_narrative.md
`-- playground/
    `-- microgrid_sim.html     # browser sim-game (no build, no deps)
```

## Skills (optional enhancements)

Anthropic publishes document-handling skills at `anthropics/skills`. To install in Claude
Code:

```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

After install, `pdf` / `docx` / `xlsx` / `pptx` skills auto-trigger when relevant
(for example, "convert chapters 00-11 to a single PDF"). The skills are an **enhancement**, not a
dependency. The project ships its own export tools (`model/src/electicity_model/export.py`,
optional `[export]` extra: `pip install -e ".[export]"`) so nothing is blocked if skills
aren't installed.

## Sim-game (browser playground)

`playground/microgrid_sim.html`, open in any modern browser. SimCity-lite microgrid:

- Build mode: drag/click tech tiles to assemble a 2 MW district; live capex / LCOE / LCOH /
  availability readouts; $36M envelope progress bar.
- Shock mode: inject `ir_shortage`, `triple_squeeze`, `maritime_blockade`, `regional_autarky`
  and similar profiles. Your build either holds or breaks, with a reason.
- Challenge mode: timed scenarios (Iberian Default, Triple Squeeze, Volcanic Year, Survival
  180) with scoring across availability x cost x shock-resilience. ZTA toggle gives a
  reliability bonus.
- Campaign mode: a 5-year run with decision cards, trust that decays on neglected blocs,
  bloc defection, and retaliation. See the diplomacy section above.
- Save and share: "Copy share link" encodes your build and posture into the URL so the exact
  scenario reopens in any browser. No backend.
- Leaderboard: best score per challenge or campaign, kept locally; each row reloads the build
  that earned it.
- Numbers baked from `model/data/tech_params.yaml`; the Python model remains the source of
  truth.

## Quickstart

```
cd model
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -v                                    # 223 tests pass
electicity district --scenario district_solar_h2_inland
electicity district --scenario district_solar_h2_inland --shock triple_squeeze
electicity car --scenario car_fcev_class8 --h2-price 4.0
electicity shock --profile maritime_blockade
electicity regions --jurisdiction AU --top 3
electicity finance --capex 27000000 --annual-revenue 5500000 --annual-opex 1300000 --years 25 --discount-rate 0.09
electicity render-all                        # regenerates report/_generated_tables.md and deck/assets/*.png
electicity summary --out _summary.json       # machine-readable JSON
```

## End-to-end verification checklist

| Step | Command | Expected result |
|---|---|---|
| 1. Environment | `python3.14 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"` | clean install, no resolver errors |
| 2. Tests | `pytest -v` | 17+ tests pass; no skips outside platform-specific |
| 3. District scenario | `electicity district --scenario district_solar_h2_inland` | capex $27.0M, LCOE $214/MWh, LCOH $1.90/kg (see model output) |
| 4. Car scenario | `electicity car --scenario car_fcev_class8 --h2-price 4.0` | TCO $0.907/km (see model output) |
| 5. Render artifacts | `electicity render-all` | `report/_generated_tables.md` and `deck/assets/*.png` rewritten with fresh stamps |
| 6. JSON summary | `electicity summary --out _summary.json` | machine-readable snapshot of all scenario outputs |
| 7. Diff check | `git diff report/_generated_tables.md` | clean if model and scenarios unchanged |

## Headline numbers

Read live from `report/_generated_tables.md` (model v0.1.0, params hash `214a7b5cb0b0`):

- **Inland US district** (`district_solar_h2_inland`): $27.0M capex (fits $36M envelope), LCOE $214/MWh, LCOH $1.90/kg with 45V PTC applied (see model output).
- **Class 8 FCEV at $4/kg green H2** (`car_fcev_class8`): $0.907/km TCO, vs **BEV** $0.712/km (`car_bev_class8_ref`) and **diesel** $0.781/km (`car_diesel_class8_ref`) (see model output).
- Sensitivity band on H2 price: $4/kg gives $0.907/km, $6/kg gives $1.082/km, $9/kg gives $1.343/km (see model output).

## Honest competitive positioning

For passenger cars, BEV beats FCEV on cost, efficiency, and infrastructure maturity [IEA-GlobalEV-2024]. We do not pretend otherwise.

The defensible FCEV niche is **heavy-duty long-haul and back-to-base fleets** where battery mass, charging time, and depot energy density penalize BEVs [ICCT-HDV-2023]. The Class 8 bench-validation is scoped to that niche, not to a general "hydrogen economy" pitch.

The district microgrid is positioned as **renewable firming plus thermal/transport coupling**, not as a competitor to grid-scale storage in isolation.

## Reproducibility

Artifacts ship with a stamp combining the model version, the git SHA of the source tree, and a hash of the resolved scenario parameters. The convention is `model vX.Y.Z @ git-sha | params hash`, applied at the top of every rendered file (and at the top of each section where applicable). Re-running `electicity render-all` from the same commit on the same scenarios reproduces byte-identical artifacts, modulo the git SHA.

## Changelog and backlog

Release notes live in `CHANGELOG.md` at the repo root. Deferred work tracked in
`BACKLOG.md`.

## Pointers

- Full technical detail: `report/01_introduction.md` through `report/08_*.md`.
- Not-investable survey (LENR): `report/09_lenr_appendix.md`.
- Grant-specific narratives: `grants/horizon_europe_cluster5.md`, `grants/doe_oced.md`, `grants/arena.md`, `grants/eeca.md`, `grants/eu_innovation_fund.md`, plus `grants/_shared_narrative.md`.
- VC pitch: `deck/pitch.md` (Marp).
- Bibliography: `report/references.md`.

## License

Dual-licensed.

- Code (everything under `model/src/`, `model/tests/`, the playground HTML, the
  `docs/scan_non_ascii.py` script) is released under the **Apache License 2.0**.
  See `LICENSE`.
- Documentation, data, and prose (everything under `report/`, `grants/`, the playground
  copy, `investor_memo.md`, `README.md`, `CHANGELOG.md`, `BACKLOG.md`, `DISCLAIMER.md`,
  `model/data/*.yaml`) is released under **Creative Commons Attribution 4.0
  International (CC BY 4.0)**. See `LICENSE-DOCS`.

Cited third-party publications, datasets, and standards keep their own licences and are
referenced by URL or DOI in `report/references.md`.

If you use this project in academic work, see `CITATION.cff` for the suggested citation
format.

## Project governance

- `CODE_OF_CONDUCT.md` adopts the Contributor Covenant 2.1.
- `CONTRIBUTING.md` covers test setup, the new-tech checklist, and PR conventions.
- `SECURITY.md` covers the private-report channel.
- `.github/PULL_REQUEST_TEMPLATE.md` and `.github/ISSUE_TEMPLATE/` carry templates for
  contributions and reports.

## Publishing checklist

Before pushing this repository to a public host, run:

```
python3 docs/scan_non_ascii.py            # markdown and playground stay ASCII
cd model && .venv/bin/pytest -q           # full test suite passes
cd model && .venv/bin/pyright --project ../pyrightconfig.json   # zero type errors
grep -rn "/Users/" --include="*.md" --include="*.py" --include="*.yaml" .
grep -rn "TODO" --include="*.md" .        # confirm grant placeholders are intentional
```

A GitHub Actions workflow ships at `.github/workflows/ci.yml`. Jobs run on every push
and pull request to `main`: pytest with coverage gate at 85 percent, pytest perf
budgets, pyright strict, and a non-ASCII scan over markdown and the playground.

A second workflow at `.github/workflows/pages.yml` deploys the static site (landing
page in `docs/` plus the playground in `playground/`) to GitHub Pages on every push to
`main`. Enable Pages once on the repository settings page (Settings -> Pages -> Source
-> "GitHub Actions"). The site lands at `https://sara-star-quant.github.io/clean-hydrogen-resilience-model/`.

## Reproducibility note

Every rendered artifact carries a stamp of the form

```
<!-- model vX.Y.Z @ git-sha | params hash -->
```

at the top of the file (and at the top of each section, where applicable). The stamp ties the artifact to (a) the model version, (b) the git SHA of the source tree, and (c) a hash of the resolved scenario parameters. Re-running `electicity render-all` from the same commit on the same scenarios reproduces byte-identical artifacts, modulo the git SHA.
