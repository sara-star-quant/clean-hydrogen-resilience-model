# 08 - Roadmap and Milestones

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

This is a 36-month plan from grant award. Two parallel tracks run side by side. Each milestone is a TRL gate with a go / no-go decision criterion, not a soft target.

## Gantt summary

```
Month            0    3    6    9   12   15   18   21   24   27   30   33   36
                 |----|----|----|----|----|----|----|----|----|----|----|----|
Car track     [PROCURE][BENCH BUILD ][DYNO TEST       ][REPORTING]
                                M3                  M5
District      [DESIGN ][PERMIT     ][PROCURE  ][BUILD       ][COMM][12-MO MEAS]
                       M2          M4          M6           M8    M10
Cross-cut     [SAFETY-CASE ALL TRACKS                       ]
              [OPEN-SCIENCE DATA PLAN                        ]
```

## Milestones (gates with explicit pass criteria)

| ID | Month | Gate | Go criterion |
|---|---|---|---|
| M1 | 3 | Car-track procurement complete | All long-lead components on PO; safety partner contracted |
| M2 | 6 | District design freeze plus permit pack submitted | NFPA 2 and ATEX compliance memo signed; interconnect study filed |
| M3 | 9 | Car-track stack on bench, first power-on | Continuous 50 kW for 1 hr; H2 leak under 1 percent |
| M4 | 12 | District procurement competitive bids closed | At least 2 bids per major package within 10 percent of model capex |
| M5 | 18 | Car-track dyno campaign complete | 80 kW continuous; 200 kW peak for 30 s; durability projection at or above 20,000 hr |
| M6 | 21 | District construction kickoff | Full insurance bondability confirmed; financial close |
| M7 | 24 | Car-track final report and TCO defended | Bench-measured TCO within 15 percent of pre-test model |
| M8 | 30 | District commissioning hot-fire | 1 MW continuous for 24 hr passing safety and GHG checks |
| M9 | 33 | District at full output | 2 MW continuous for 168 hr; availability at or above 99 percent during test |
| M10 | 36 | 12-month measurement campaign begins | Open-data platform live; first month of telemetry public |

## Open science and data deliverables

These deliverables are required by Horizon Europe. They are voluntary in other schemes but committed by this project to strengthen the case.

- Public release of the cost-and-feasibility model (this repo, MIT or Apache-2.0 licence).
- Public release of `tech_params.yaml` with sources.
- Quarterly publication of operational telemetry from the district during the 12-month measurement campaign, anonymised where required.
- Final TCO and LCOE report, peer-reviewed submission target: *Applied Energy*, *Joule*, or *International Journal of Hydrogen Energy*.
- Decommissioning and PGM-recovery plan published 6 months before end of design life.

## Ethics, gender equality plan, and public engagement

Horizon Europe makes ethics review, a Gender Equality Plan (GEP), and public engagement mandatory for participating institutions. The project treats them as substantive deliverables and applies the same controls in non-EU deployments.

**Ethics.** A formal ethics review is completed before the first telemetry stream goes live. The review covers worker safety on the bench, community exposure at the host site, and the secondary use of any data that touches identifiable persons. The output is an ethics opinion filed alongside the DPIA referenced in Chapter 06. Where Horizon Europe rules require an Ethics Advisor or Ethics Board, the project appoints one within 90 days of grant award.

**Gender Equality Plan.** A documented GEP is in place at the lead organisation and at each major partner. The plan is public, signed by the top management, and resourced. It addresses recruitment and selection, work-life balance and organisational culture, gender balance in leadership and decision-making, integration of the gender dimension into research and teaching content, and measures against gender-based violence including sexual harassment. The GEP names indicators and reports against them annually. Hires for the demonstrator team apply the plan, and the annual report tracks gender balance in the engineering, operations, and leadership functions of the project.

**Public engagement.** Engagement is scheduled, not reactive. Three layers run in parallel: a host-site community programme that begins before site selection (see R13 in Chapter 07); a wider public-communication programme that includes open-day visits, school programmes, and accessible explainers of the safety case; and a research-community programme that publishes preprints, releases code on schedule, and presents at field conferences. Each layer has a named owner, a budget line, and an indicator (attendance, downloads, citations, survey responses). The objective is informed consent at the host site and informed scrutiny in the research community. Both are necessary conditions for the demonstrator to do its job.

## Decommissioning and circularity (high-level commitment)

- Stack contracts include OEM take-back for PGM recovery (Ir, Pt).
- Lithium cells are routed through a licensed recycler, with UL 1974 second-life evaluation considered first.
- Composite H2 tanks: ASME-certified recertification or end-of-life destruction per local code. No landfill of composites.
- Civil works: foundations broken out and aggregate recycled; PV modules per the local PV-waste directive (EU WEEE or equivalent).

A full Decommissioning Management Plan is delivered at M30 as a condition of commissioning sign-off.
