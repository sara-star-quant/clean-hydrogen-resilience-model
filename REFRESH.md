# Refresh Gate

> Dependencies and external data are pinned to the latest versions verifiable on the
> stamp date below. Nothing here is forecast. Re-run this gate before any release, grant
> submission, or investor-facing export, and update the stamp.

**Last verified:** 2026-06-19 (Q2 2026). Knowledge as of this date only; future-quarter
data must be re-verified, not assumed.

## Why a gate

The repo cites policy, market, and price data that drift, and depends on libraries that
ship new releases. "Latest" is only true on a date. This file records what was current at
the stamp, and the exact command to re-check each item. No number or version in the repo
should be treated as current past its stamp without re-running the relevant step below.

## 1. Dependency pins (verified 2026-06-19)

Floors in `model/pyproject.toml` and the rev in `.pre-commit-config.yaml` are set to these
verified-latest releases:

| Package | Pinned floor | Latest verified | Source |
|---|---|---|---|
| pyyaml | >=6.0.3 | 6.0.3 | PyPI |
| matplotlib | >=3.11 | 3.11.0 | PyPI |
| pytest | >=9.1 | 9.1.0 | PyPI |
| pytest-cov | >=7.1 | 7.1.0 | PyPI |
| hypothesis | >=6.155 | 6.155.5 | PyPI |
| openpyxl | >=3.1.5 | 3.1.5 | PyPI |
| python-pptx | >=1.0.2 | 1.0.2 | PyPI |
| python-docx | >=1.2 | 1.2.0 | PyPI |
| setuptools (build) | >=82 | 82.0.1 | PyPI |
| pre-commit-hooks | v6.0.0 | v6.0.0 | GitHub releases |
| pyright (local hook venv) | 1.1.410 | 1.1.410 | PyPI |
| python | >=3.14 | 3.14.6 (3.15 not released) | endoflife.date |

Re-verify all (network required):

```
for p in pyyaml matplotlib pytest pytest-cov hypothesis openpyxl python-pptx python-docx setuptools pre-commit pyright; do
  v=$(curl -s "https://pypi.org/pypi/$p/json" | python3 -c "import sys,json;print(json.load(sys.stdin)['info']['version'])")
  echo "$p = $v"
done
curl -s "https://api.github.com/repos/pre-commit/pre-commit-hooks/releases/latest" | python3 -c "import sys,json;print('pre-commit-hooks',json.load(sys.stdin)['tag_name'])"
```

After any bump: `cd model && .venv/bin/pytest -q` and `pyright --project pyrightconfig.json`
must stay green before committing the new floor.

## 2. Data and citation refresh

Numbers in the report, memo, and grant templates are scenario outputs and cited public
figures. Each must be re-checked at its source before external use. Re-render the model so
artifacts carry a fresh stamp:

```
cd model && .venv/bin/electicity render-all   # rewrites report/_generated_tables.md + deck/assets
git diff report/_generated_tables.md           # clean only if model + scenarios unchanged
```

Checklist (confirm each at source, record the as-of date in the citing file):

- [ ] Policy: IRA section 45V Tier-1 thresholds and Treasury rule status `[IRA-45V]`
- [ ] Policy: EU RFNBO matching rules `[EU-RFNBO-1184]`, `[EU-RFNBO-1185]`
- [ ] Targets: REPowerEU H2 volumes `[EC-REPowerEU]`, DOE Hydrogen Shot `[DOE-H2Shot]`
- [ ] Market: IEA Global Hydrogen Review latest edition `[IEA-GHR-*]`
- [ ] Market: IRENA / BNEF price and CAGR figures `[IRENA-RPGC-*]`, `[BNEF-H2-Outlook]`
- [ ] System: AEMO ISP latest `[AEMO-ISP-*]`
- [ ] FX rates in `grants/au_arena.md` (USD/AUD) and `grants/nz_eeca_callaghan.md` (USD/NZD)
- [ ] Grant call IDs and close dates in `grants/CALL_TRACKER.md` (portal confirmation)
- [ ] Bibliography URLs/DOIs in `report/references.md` still resolve

## 3. Stamp update

When the gate is re-run, bump **Last verified** above and the version/date stamps on any
re-rendered artifact. Do not ship an artifact whose stamp predates its data sources.
