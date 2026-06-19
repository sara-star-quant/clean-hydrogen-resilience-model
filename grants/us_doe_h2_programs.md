# US DOE Hydrogen Programs - Proposal Skeleton (HFTO / OCED / Regional Clean Hydrogen Hubs)

> **Disclaimer.** Template document for grant proposal drafting. Numbers are illustrative; placeholders must be replaced before submission. Not legal, financial, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

*Numbers in this template are illustrative scenario outputs, traceable to public sources cited in `report/references.md`. Replace each placeholder with site-specific, jurisdiction-specific, and time-current values before submission. Submission to a funding programme is the responsibility of the submitting entity, not this template.*

Target: $36M total project, 36 months, district-scale 2 MW hybrid microgrid deployment with green H2 production via electrolysis from renewables. Federal share approximately $18M (50% cost share typical for OCED demonstrations).

Citations resolve in `../report/references.md`. Live numbers in `../report/_generated_tables.md`. Reusable narrative blocks in `./_shared_narrative.md`.

---

## 1. Scheme Overview

*Indicative budget; numbers are scenario outputs derived from cited public sources. Replace before submission. See DISCLAIMER.md.*

| Program | Scope | TRL | Typical Award | Fit |
|---|---|---|---|---|
| HFTO RDD&D | Hydrogen and fuel cell research, development, demonstration, deployment | 3-7 | $1M to $10M | Component-level studies; supporting role |
| OCED Demonstration FOAs | First-of-a-kind clean energy demonstrations | 7-9 | $10M to $100M+ | Primary fit for the 2 MW district deployment |
| Regional Clean Hydrogen Hubs (H2Hubs) | Multi-billion regional consortia under the Bipartisan Infrastructure Law | 7-9 | Hub-scale | Possible satellite project to a larger Hub |

Programmatic anchors: DOE Hydrogen Shot at $1/kg by 2031 [DOE-H2Shot]; H2@Scale framework for cross-sector hydrogen integration [DOE-H2atScale].

<!-- TODO: paste current FOA from https://www.energy.gov/eere/funding -->

## 2. Strategic Fit

The project supports DOE Hydrogen Shot by validating district-scale demand-side architecture coupled to renewable generation, and by carrying a low-iridium pathway (alkaline / AEM substitution) as a documented risk mitigation route against PEM iridium supply constraints [IEA-GHR-2024].

IRA section 45V production tax credit alignment. The project commits to Tier 1 (lifecycle CI < 0.45 kgCO2e/kgH2) [IRA-45V] and to all three pillars of the Treasury final rule on the section 45V credit:

- **Additionality (incrementality).** New-build PPA covering renewable generation contracted specifically for this project, executed at financial close. No diversion from existing renewable supply, no commercial operation date earlier than the lookback window allowed by the final rule. The PPA term sheet documents the additionality test that the project meets.
- **Hourly temporal matching.** The dispatch model and meter design are built for hourly matching from the start of operations, consistent with the Treasury phase-in schedule that moves from annual matching to hourly matching by the rule's stated transition year. Annual matching is not used as a fallback; the project operates under hourly matching from day one and reports hourly EAC retirements alongside hourly electrolyser load.
- **Geographic deliverability.** Renewable generation is co-located with the electrolyser at the project site within the same DOE-defined region. No inter-regional transfer reliance, no distant-balancing-authority deliverability claim. The interconnection topology supporting deliverability is documented at FERC interconnection filing (see Section 6).

Three-pillar compliance is encoded in the operating-rule library at financial close, audited annually, and is a binding constraint not a deliverable.

## 3. Technical Approach

Pull from `_shared_narrative.md` block: "Technology approach". Summary:

- 2 MW PEM electrolyzer (alkaline / AEM substitution carried as risk mitigation per Section 10).
- On-site renewable generation co-located with electrolyzer.
- Buffer storage and dispatch model coupling renewable output to electrolyzer load.
- District load served via hybrid microgrid with H2 backup.

Three site variants modeled (`_generated_tables.md`):

*Scenario output, not a forecast. Indicative numbers; replace at submission. See DISCLAIMER.md.*

| Variant | CapEx | LCOE | LCOH |
|---|---|---|---|
| District solar H2 (inland), **default** | $27.0M | $214/MWh | $1.90/kg |
| District micro-hydro (river-adjacent) | $20.3M | $160/MWh | $4.30/kg |
| District tidal (coastal) | $24.2M | $198/MWh | $5.22/kg |

All three variants fit within the $36M envelope. Inland solar plus H2 is recommended as the default deployment site type: lowest LCOH, fewest permitting dependencies, broadest geographic replicability. River and coastal variants remain available for site-specific consortia.

## 4. Milestones

Mapped to `../report/08_roadmap_milestones.md` (M1 through M10). Milestone IDs and dependencies are defined there; this section anchors them to the proposal timeline.

| ID | Approx. Month | Deliverable |
|---|---|---|
| M1 | 0 | Award and financial close; PPA executed; FERC interconnect study filed |
| M2 | 3 | Site selection and environmental scoping complete |
| M3 | 6 | Permitting package filed |
| M4 | 9 | Long-lead procurement (electrolyzer, transformer, BoP) |
| M5 | 15 | Site civil works complete |
| M6 | 21 | Electrolyzer install and commissioning |
| M7 | 27 | Renewable generation tied in; hourly matching dispatch live |
| M8 | 30 | Microgrid islanding and grid-tied test |
| M9 | 33 | Full operations begin; data publication infrastructure live |
| M10 | 36 | Final report; open dataset release; peer-reviewed LCOH/LCOE retrospective |

## 5. 45V Integration

Explicit compliance with the three-pillar Treasury final rule [IRA-45V]. The compliance commitments below are written into the PPA term sheet, the meter design, the dispatch firmware, and the project's annual 45V audit package.

- **Additionality / new-build PPA at financial close (M1).** The PPA covers renewable generation contracted specifically for this project, with commercial operation date inside the lookback window allowed by the final rule. No diversion from existing renewable supply. The PPA term sheet documents the incrementality test.
- **Hourly temporal matching from day one.** Dispatch firmware retires EACs on an hourly basis consistent with the Treasury phase-in schedule. Annual matching is not used as a fallback. Hourly EAC retirement records are reconciled to hourly electrolyser load and reported in the annual 45V audit package.
- **Geographic deliverability.** Generation is co-located with the electrolyser at the project site within the same DOE-defined region; no inter-regional or distant-balancing-authority deliverability claims. The interconnection topology and the boundary of the deliverability region are documented at the FERC interconnection filing (Section 6).

The project commits to Tier 1 carbon intensity (< 0.45 kgCO2e/kgH2). Lifecycle calculation methodology and assumptions are in `../report/06_environmental_lca.md`. The 45V auditor of record is contracted at financial close; the audit cadence is annual for the credit's ten-year window.

## 6. FERC Interconnection Plan

Interconnection study filed at Month 0 to address R4 (interconnection queue delay, see `../report/07_risk_register.md`). FERC Order 2023 reformed the interconnection queue to a cluster-study, first-ready-first-served process; project schedule assumes the post-Order-2023 timeline [FERC-Order-2023].

Filing package at M0:

- Interconnection request submitted to the host transmission provider under the cluster study window in force.
- Site control documentation (site agreement or recorded option) filed with the request to satisfy the first-ready-first-served readiness criteria.
- Interconnection deposit posted at the schedule defined by the host RTO/ISO tariff.
- Affected-system studies anticipated at neighbouring balancing authorities; the consortium budgets for participation in those studies.

Engagement plan with the host RTO/ISO. Pre-filing engagement at M-3 (before award), monthly study-coordination calls during the cluster study, formal queue-position confirmation logged at WP1 ethics and risk register update.

Plan B. Behind-the-meter sizing carried as a documented fallback. Behind-the-meter operation reduces interconnection scope at the cost of constraining grid-export revenue and dispatch flexibility. Sizing parameters are pre-computed and held in reserve; the threshold for invoking Plan B is queue-position uncertainty exceeding the construction critical path by more than six months.

## 7. Budget

36 months, $36M total deployed CapEx. DOE OCED demonstrations typically run at 50% federal cost share; ask is approximately $18M federal plus approximately $18M private/state.

*Indicative budget; numbers are scenario outputs derived from cited public sources. Replace before submission. See DISCLAIMER.md.*

| Category | Federal ($M) | Cost Share ($M) | Total ($M) | Notes |
|---|---|---|---|---|
| Direct equipment (electrolyzer, BoP, generation) | 10.0 | 10.0 | 20.0 | Long-lead; bulk of CapEx |
| Site civil and interconnect | 3.0 | 3.0 | 6.0 | Civil works, transformer, switchgear |
| Engineering / project management | 2.0 | 2.0 | 4.0 | EPC oversight |
| Direct labor (operations and monitoring) | 1.0 | 1.0 | 2.0 | Ops staff during commissioning and Year 1 |
| Materials and supplies | 0.3 | 0.3 | 0.6 | Sensors, consumables |
| Travel | 0.1 | 0.1 | 0.2 | Site visits, DOE reviews |
| Subcontracts (university monitoring) | 0.4 | 0.4 | 0.8 | Independent measurement |
| Indirect | 1.2 | 1.2 | 2.4 | approximately 50% on modified total direct cost (placeholder pending NICRA) |
| **Total** | **18.0** | **18.0** | **36.0** | Indicative; adjust at submission |

Numbers are indicative and consistent with the inland default scenario ($27.0M base CapEx) plus contingency, integration, and reporting overhead within the $36M envelope.

## 8. Team

- **Integrator / prime**. EPC and project delivery.
- **Electrolyzer vendor**. Supply, commissioning, durability data sharing.
- **FCEV OEM**. Vehicle interfaces if H2 station retail extension is added in scope (optional Phase 2).
- **University monitoring partner**. Independent measurement of LCOH, LCOE, and lifecycle CI.
- **Host community**. Site agreement, community benefits plan, workforce development partnership.

## 9. Open Science / Data Publication

- Operational data (electrolyzer load profile, hourly matching ledger, hydrogen production, grid interactions) published quarterly during operations.
- Final retrospective LCOH/LCOE report peer-reviewed and released open-access at M10.
- Bench-protocol and dispatch-model source artifacts released under permissive license consistent with DOE open-data guidance.

## 10. Risk Register. Top 5

Pulled from `../report/07_risk_register.md`. Full register and mitigations in that file.

| ID | Risk | Mitigation Headline |
|---|---|---|
| R1 | Renewable resource shortfall vs design | Conservative capacity factor in dispatch model; storage sizing margin |
| R2 | Electrolyzer iridium / supply-chain constraint | Alkaline / AEM substitution path carried; multi-vendor sourcing |
| R4 | FERC interconnection queue delay | File Month 0; behind-the-meter Plan B |
| R6 | 45V eligibility ruling change | Three-pillar compliance built in from start; not retrofitted |
| R8 | Permitting and environmental review delay | Early scoping (M2), parallel-track filings, host-community engagement |

## 11. Anti-Fraud / Honest Scope

This proposal is grounded in commercially available electrolysis (PEM with alkaline / AEM fallback), conventional renewable generation, and standard microgrid technology. It makes no claims regarding low-energy nuclear reactions, cold fusion, or other unvalidated phenomena. The 2019 multi-laboratory investigation found no evidence for cold fusion and is referenced here as a stance marker [Berlinguette-2019].
