# ARPA-E Concept Paper Skeleton. Heavy-Duty FCEV Bench Validation Track

> **Disclaimer.** Template document for grant proposal drafting. Numbers are illustrative; placeholders must be replaced before submission. Not legal, financial, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

*Numbers in this template are illustrative scenario outputs, traceable to public sources cited in `report/references.md`. Replace each placeholder with site-specific, jurisdiction-specific, and time-current values before submission. Submission to a funding programme is the responsibility of the submitting entity, not this template.*

Target: $1M federal request, 24 months, bench validation of a Class 8 FCEV powertrain on chassis dyno.

Citations resolve in `../report/references.md`. Live numbers in `../report/_generated_tables.md`. Reusable narrative blocks in `./_shared_narrative.md`.

---

## 1. Scheme Summary

ARPA-E concept papers are short (typically 6 to 10 pages) and gate access to the full proposal stage. The package comprises:

- Cover sheet (PI, organization, requested amount, period of performance, team)
- Technical narrative (approximately 3 pages of substantive content within the page cap)
- Budget summary
- Team and management plan

Typical award range is $1M to $10M. ARPA-E targets transformational research, not incremental research, generally TRL 2 to 4. The bench-validation track sits in this bracket: a 100 kW PEMFC stack with Li-ion buffer and 700 bar storage on a Class 8 chassis dyno, instrumented to produce defensible duty-cycle data rather than incremental component improvement.

Programmatic context: DOE Hydrogen Shot targets $1/kg clean H2 by 2031 [DOE-H2Shot]. Heavy-duty FCEVs are an explicit DOE focus segment for hard-to-electrify long-haul applications [DOE-HD-FCEV].

## 2. Call Fit

The bench-validation track maps best to ARPA-E OPEN solicitations (broadest scope, biennial cadence) and to prior heavy-duty and powertrain-relevant programs:

- ARPA-E OPEN. Biennial, transformational research across all energy verticals.
- REEACH. Electrified aviation propulsion; relevant for fuel-cell plus electric architecture techniques transferable to HD ground.
- ASCEND prior cohorts. Superconducting and high-density propulsion, methodology overlap on bench instrumentation and integrated powertrain testing.

<!-- TODO: confirm current open solicitation at https://arpa-e.energy.gov/ -->

## 3. Technical Narrative (approximately 3 pages)

### 3.1 Hypothesis and Transformational Claim

Hypothesis: a defensible, segment-specific TCO and durability dataset for a 100 kW Class 8 FCEV powertrain, produced under a transparent, reproducible bench protocol, materially shifts fleet operator decision-making in long-haul corridors where BEVs face range and recharge-window constraints and diesel faces tightening NOx and CO2 regulation.

Transformational claim, stated honestly:

> Pure integration of commercially available PEMFC stacks, Li-ion buffers, and 700 bar tanks is not transformational research. The transformational element is the *defensibility model*: a published, reproducible bench protocol plus a segment-specific TCO methodology that ties measured stack degradation, hydrogen consumption, and duty-cycle efficiency to fleet-economics outcomes. Bench validation is the ground truth for that model. The transformational test is whether a fleet operator can read the published protocol, reproduce the measurements on a competing platform, and arrive at the same go / no-go decision; no current public dataset supports that test for Class 8 long-haul.

This positioning is consistent with ARPA-E's preference for measurable, falsifiable outcomes over speculative breakthroughs. See `_shared_narrative.md` block "Honest positioning".

### 3.2 Why Incumbents Have Not Solved This

Three structural reasons explain why the existing FCEV ecosystem has not produced a defensible Class 8 TCO and durability dataset, despite individual components being commercial.

- BEV passenger-car dominance has pulled R&D capital toward light-duty cells and packs; HD-specific energy-density and refueling constraints are under-invested by both auto OEMs and tier-one suppliers, who optimize for volume.
- Diesel HD economics remain favorable at fuel-cost equilibrium; without a reproducible TCO model under realistic H2 price scenarios, fleet buyers default to diesel. OEM-published consumption figures are produced under proprietary cycles, are not directly comparable across vendors, and are not reconciled to measured stack degradation under HD duty.
- H2 cost: current delivered H2 prices materially exceed the $1/kg Hydrogen Shot target [DOE-H2Shot]. Project TCO at $4/kg, $6/kg, and $9/kg pump price is $0.907/km, $1.082/km, and $1.343/km respectively, against diesel reference $0.781/km and BEV reference $0.712/km (`_generated_tables.md`). The crossover behavior between BEV, diesel, and FCEV across duty cycle, depot access, and H2 price is not characterized in any open public dataset.

Incumbent OEMs hold the relevant data internally and use it for product gating, not for fleet-buyer decision support. ARPA-E's role is to fund the public-good measurement campaign that no incumbent has commercial reason to publish.

See `_shared_narrative.md` block "Honest positioning" for the full framing.

### 3.3 Approach

- Powertrain: 100 kW PEMFC stack plus Li-ion buffer plus 50 kg at 700 bar storage, integrated on a Class 8 chassis dyno.
- Bench protocol: standardized HD long-haul drive cycles, instrumented for stack voltage decay, hydrogen mass flow, balance-of-plant parasitic load, and thermal envelope.
- Innovation surface, honest:
  - *Not* novel: stack chemistry, tank certification, motor topology.
  - *Novel*: segment-specific TCO methodology tied to measured degradation; reproducible bench protocol published as open dataset; dispatch-model coupling with district-scale H2 supply scenarios.
- Outputs: open dataset, reproducible TCO model, peer-reviewed bench protocol.

### 3.4 Risk and Mitigation

| Risk | Description | Mitigation |
|---|---|---|
| R7 | Stack durability falls short of 25,000 h target under HD duty | Accelerated stress test plus post-mortem MEA analysis; fallback to lower duty assumption with documented derating |
| R12 | Stack price at low volume materially above projections | Multi-vendor sourcing during bench phase; price sensitivity carried explicitly through TCO model |

Full register in `../report/07_risk_register.md`.

### 3.5 Commercialisation transition plan

The bench campaign is scoped as a public-good measurement programme, not as a vendor R&D project. The transition to commercial impact runs in three steps.

Step 1, year 0 to 2 (project period). Open dataset and reproducible TCO model published under a permissive licence at month 24, with the bench protocol peer-reviewed and the parameter file released alongside. The dataset is structured for direct ingestion into fleet-procurement tools.

Step 2, year 2 to 4 (post-project, no further federal ask). One to three fleet operators run an internal procurement decision against the published protocol on a representative duty cycle, with the consortium providing technical assistance under a published rate sheet rather than a follow-on grant. OEM partners use the protocol as a benchmark; the bench facility is offered to commercial customers under a documented service agreement.

Step 3, year 3 to 5. The protocol is contributed to SAE J2601 / J2719 working groups and to relevant DOE H2 fleet programs as a candidate measurement standard. Commercial pilots beyond the project consortium adopt the methodology.

The plan does not require additional federal funding past the bench campaign. The exit point is methodology adoption, not equity formation; the team commits to a non-exclusive licensing posture so that competing fleet-decision-support vendors can use the protocol on equal terms.

## 4. Milestones

Mapped to `../report/08_roadmap_milestones.md`. ARPA-E-style go/no-go gates at each.

| ID | Month | Deliverable | Go/No-Go |
|---|---|---|---|
| M1 | 3 | Bench design review, stack and tank procurement contracts | Procurement signed, design review passed |
| M2 | 9 | Subsystem bring-up (stack, buffer, storage) on bench | Stack at rated power into resistive load |
| M3 | 15 | Integrated chassis-dyno commissioning | First full HD drive cycle completed within thermal envelope |
| M4 | 21 | Full duty-cycle test campaign plus degradation accelerated test | >= 1,000 h cumulative plus degradation curve fit |
| M5 | 24 | Open dataset, TCO model release, final report | Dataset published, TCO model peer-reviewed |

## 5. Budget

24 months, $1M federal request. Indicative breakdown matching `../report/03_car_track.md`. Indirect rate is a placeholder pending negotiated rate agreement.

*Indicative budget; numbers are scenario outputs derived from cited public sources. Replace before submission. See DISCLAIMER.md.*

| Category | Amount | Notes |
|---|---|---|
| Direct labor | $300k | PI plus 2 engineers plus 1 technician (partial FTE) |
| Fringe | $90k | approximately 30% of labor (placeholder) |
| Travel | $20k | Site visits to subcontractors and DOE program reviews |
| Materials and supplies | $80k | Sensors, consumables, H2 supply for test campaign |
| Equipment | $200k | PEMFC stack, Li-ion buffer, tank set, dyno instrumentation |
| Subcontracts | $140k | Stack supplier integration support, dyno facility hours, university combustion lab |
| Indirect | $170k | approximately 50% on modified total direct cost (negotiated rate placeholder) |
| **Total** | **$1,000k** | |

## 6. Team

- **PI**. `<!-- TODO: PI placeholder -->`. Responsible for technical direction and TCO methodology.
- **Co-PI, FCEV stack supplier**. Stack integration, durability protocol, MEA post-mortem.
- **Co-PI, dyno facility**. Chassis-dyno operations, drive-cycle instrumentation, data acquisition.
- **Co-PI, university combustion / propulsion lab**. Independent measurement, peer-review of bench protocol.

ARPA-E expects strong coverage across hardware integration, test infrastructure, and independent measurement. The team structure above provides this without over-staffing.

## 7. Anti-Fraud / Honest Scope

This proposal is grounded in commercially available PEMFC, Li-ion, and 700 bar storage technologies. It makes no claims regarding low-energy nuclear reactions, cold fusion, or other unvalidated phenomena. The 2019 multi-laboratory investigation found no evidence for cold fusion and is referenced here as a stance marker [Berlinguette-2019].
