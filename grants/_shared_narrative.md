# Shared Narrative Blocks

> **Disclaimer.** Template document for grant proposal drafting. Numbers are illustrative; placeholders must be replaced before submission. Not legal, financial, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

Reusable narrative blocks for grant submissions. Each block below is a self-contained
unit and may be cut-and-pasted into a specific call template. Citation keys resolve in
[report/references.md](../report/references.md).

---

## Block: Problem and opportunity

The European energy system faces a triple constraint: decarbonisation of hard-to-abate
end uses (heavy-duty road freight, high-temperature process heat, seasonal storage),
security of supply post-2022, and the need to absorb increasing volumes of variable
renewable generation without curtailment. The REPowerEU programme [EC-REPowerEU] sets
an explicit target of 10 Mt domestic renewable hydrogen production and 10 Mt imports
by 2030, and the Hydrogen Strategy [EC-H2-Strategy] frames hydrogen as the principal
chemical energy carrier bridging variable electricity supply and non-electrifiable
demand. The IPCC AR6 WG1 assessment [IPCC-AR6-WG1] underpins the urgency: cumulative
emissions, not annual flow, determine the warming budget, so deployment cadence
through 2030 dominates outcomes.

Water-medium energy pathways, including water electrolysis powered by renewables,
water as the working fluid in low-temperature thermal cycles, and water as the
moderator and coolant in distributed storage, concentrate this opportunity in a
single technology stack. Green hydrogen via low-temperature alkaline and PEM
electrolysis is at TRL 8-9 for the unit cell and TRL 6-7 at MW-scale system
integration with renewable intermittency [IEA-GHR-2024]. The remaining frontier is
not the device but the system: how to operate electrolyser fleets under variable
renewable input, deliver RFNBO-compliant hydrogen [EU-RFNBO-1184], [EU-RFNBO-1185],
and integrate with end-use sectors (heavy-duty fuel-cell electric vehicles, district
heat, ancillary services) at honest levelised cost.

This proposal addresses that integration gap with two coupled demonstrators: a
bench-validation of a Class 8 fuel-cell electric truck (FCEV) under a sub-$1M /
24-month envelope, and a 2 MW district hybrid microgrid (renewables, electrolysis,
hydrogen buffer, fuel cell) under a sub-$36M / 36-month envelope. The two scales
are deliberately chosen to exercise the same hydrogen value chain at vehicle and at
community level, producing peer-comparable measurement campaigns and a shared
open-data product. We exclude unproven concepts (LENR, hydrogen-ICE) and align
strictly with the European RFNBO additionality, temporal correlation, and
geographical correlation rules.

## Block: Why this consortium

The consortium is structured to cover the full evidence chain from electron to
end-use, with each role represented by an operational entity rather than a paper
partner. Roles are listed below; named partners are inserted at submission.

- Coordinator: research-performing organisation with prior Horizon / Innovation
  Fund delivery experience. Owns Open Science deliverables, ethics, and DMP.
  `<!-- TODO: insert coordinator legal entity, PIC, contact -->`
- FCEV OEM partner: supplier of the Class 8 platform, providing chassis, traction,
  and access to engineering data for the bench campaign.
  `<!-- TODO: insert OEM partner -->`
- Electrolyser integrator: vendor of MW-scale alkaline or PEM stack with
  variable-input control firmware and stack-overhaul telemetry.
  `<!-- TODO: insert integrator -->`
- EPC / civil works: entity carrying the 2 MW district build, permitting, grid
  connection, and decommissioning bond.
  `<!-- TODO: insert EPC -->`
- Host community / off-taker: municipality, port authority, or industrial cluster
  hosting the 2 MW site and consuming the hydrogen and heat.
  `<!-- TODO: insert host -->`
- University / national lab: measurement campaign owner, independent metrology,
  peer-review publication lead.
  `<!-- TODO: insert academic partner -->`
- Dissemination and standards partner: open-data platform operator and
  standardisation liaison (CEN/CENELEC, ISO TC 197).
  `<!-- TODO: insert disseminator -->`
- Ethics and safety advisor: independent body for safety case sign-off and
  Responsible Research and Innovation oversight.
  `<!-- TODO: insert ethics partner -->`

## Block: Technology approach

The project is grounded in seven mature or near-mature water-medium technologies,
referred to as T1 through T7. Hydrogen is treated as an energy carrier, a chemical
buffer between variable renewable supply and dispatchable end use, not as a
primary energy source.

- T1. Low-temperature water electrolysis (alkaline and PEM): MW-class commercial
  units operated under variable renewable input. Stack overhaul interval and
  efficiency at part-load are the governing economic levers.
- T2. Photovoltaic generation feeding the electrolyser bus, sized to satisfy
  RFNBO temporal-correlation rules [EU-RFNBO-1184] without fossil grid imports
  during the production hour.
- T3. Run-of-river micro-hydro for inland sites with predictable head and flow,
  used as firm baseload to pair with PV to lift electrolyser duty cycle.
- T4. Tidal-stream generation, retained at pre-commercial TRL for coastal-site
  demonstrators only; classified as risk R8 (see Block: Risk top 5).
- T5. Hydrogen storage in compressed gas at 350 bar (district) and 700 bar (FCEV
  refuelling), using composite Type IV vessels with documented end-of-life
  protocol.
- T6. PEM fuel-cell re-electrification for the district buffer and for the Class
  8 truck powertrain. Membrane-electrode-assembly and platinum-group-metal supply
  is treated as a circularity input (see Block: Decommissioning and circularity).
- T7. Power and hydrogen balance-of-plant with grid-forming inverters, capable
  of islanded operation, ancillary-service provision, and RFNBO-compliant
  metering.

LENR and hydrogen-ICE are explicitly excluded; see Block: Honest positioning.
Live system-level numbers are imported from the open model:

- District CapEx envelope: $20.3M to $27.0M depending on renewable input
  (micro-hydro, PV, or tidal); LCOH range $1.90/kg to $5.22/kg [model-tables].
- FCEV Class 8 TCO range $0.91/km to $1.34/km at H2 prices of $4 to $9/kg
  [model-tables]; reference BEV $0.71/km, reference diesel $0.78/km.

(Numbers cited from [report/_generated_tables.md](../report/_generated_tables.md)
v0.1.0.)

## Block: Theory of Change

The Theory of Change frames how project activities translate into measurable
outcomes against a defensible counterfactual. Reviewers in Horizon Europe and
peer schemes expect this block to be explicit rather than assumed.

Intervention. Two coupled demonstrators (FCEV Class 8 bench at TRL 5-6, and a
2 MW RFNBO-compliant district hybrid microgrid at TRL 6-7), instrumented to
produce peer-comparable measurement campaigns and an open data product. The
intervention substitutes a measured, reproducible evidence base for the
modelled-only literature on variable-input electrolyser operation and
heavy-duty FCEV duty cycles.

Short-term outcomes (months 0 to 36). Nine quantified KPIs reported quarterly
(see Block: Quantified KPIs). Open Science deposits at Open Research Europe
and Zenodo. RFNBO compliance audited at WP5. At least two Q1 peer-reviewed
publications and one open-access dataset paper.

Medium-term outcomes (years 3 to 5 post-project). Two to four EU replication
sites adopting the published parameter set, totalling roughly 50 MW
electrolyser capacity in the same configuration. One to three commercial
fleet pilots adopting the bench-validated FCEV powertrain specification.
Operating-rule library adopted as input to CEN/CENELEC and ISO TC 197
working items.

Long-term outcomes (years 5 to 10). Replication-class deployment of 0.5 to
1.5 GW electrolyser capacity at the project's measured RFNBO duty cycle.
Cumulative GHG avoidance of 0.5 to 2.0 Mt CO2e per annum at full operating
duty against the diesel and grid-mix counterfactual.

Indicators. Each outcome is bound to an indicator with a measurement source
and frequency: KPIs 1 to 9 (project telemetry, quarterly); replication site
count (Innovation Fund knowledge-sharing reports, annual); GW deployed
(Eurostat and IEA hydrogen tracker, annual); peer-reviewed citation count
(Web of Science, annual).

Assumptions. RFNBO rules remain stable through the project period; PGM and
iridium supply does not collapse outside the headroom carried in Block:
Decommissioning and circularity; the host TSO/DSO interconnects within the
WP1 schedule; hydrogen off-take willingness-to-pay sits in the EUR 2 to 5
per kg band for the medium-term outcome.

Risk to the Theory of Change is managed in Block: Risk top 5; assumption
breaches trigger the contingency lines budgeted at WP level.

## Block: Ethics, gender equality plan, and public engagement

Ethics. The project carries no human-subject research and no animal
research. The salient ethics issues are workplace safety (high-pressure
hydrogen, electrolyser HV bus), host-community consent for district siting,
data-protection compliance for any operational telemetry that touches
personal data (see Block: GDPR and data protection), and dual-use export
control review of any bench dataset. Each issue is owned by the WP1 ethics
deliverable and signed off by the independent ethics and safety advisor.
Responsible Research and Innovation oversight runs continuously rather than
as a single gate.

Gender equality plan. The coordinator and each beneficiary maintain a
published Gender Equality Plan as required by Horizon Europe eligibility,
covering work-life balance, gender balance in leadership and recruitment,
integration of the gender dimension in research content, and measures
against gender-based violence and harassment. The consortium-level GEP
deliverable in WP1 aggregates the partner GEPs, sets a target of at least
40 percent representation of the under-represented gender in WP-lead and
deputy roles, and reports annually with corrective actions where targets
are not met.

Public engagement. The project runs an annual public-facing event at the
host community site, an open-data hackathon at month 24 using the released
parameter file and quarterly telemetry, and a school-outreach programme
co-designed with the host municipality. Engagement with vulnerable groups
in the host community is mediated by the host partner under a documented
community benefits framework. All engagement activity is reported in WP6.

## Block: GDPR and data protection

GDPR applies to any operational telemetry, host-community engagement
records, and consortium HR data processed during the project. The
coordinator acts as joint controller with each beneficiary under a written
joint-controller agreement signed at grant agreement entry into force.
Each beneficiary nominates a Data Protection Officer or equivalent contact.

Lawful basis. Telemetry processing rests on legitimate interest where it
covers no personal data, and on explicit consent where channels could
re-identify individuals (for example vehicle telematics linked to a named
driver). Consent forms are filed in the WP1 ethics deliverable.

Data minimisation and pseudonymisation. The published quarterly telemetry
filter list redacts personally-identifying channels by default. A
documented review by the DPO precedes each quarterly release. Pseudonyms
replace identifiers in research datasets; the re-identification key is held
by the coordinator under access control.

Cross-border transfers. Where partners outside the EEA process project
personal data, transfers rely on the European Commission's Standard
Contractual Clauses with a transfer impact assessment recorded in WP1.

Subject rights. A subject-rights handling procedure (access, rectification,
erasure, portability, objection) is documented at month three and tested
through a tabletop exercise at month twelve.

Breach response. Any personal-data breach is notified to the lead
supervisory authority within 72 hours per Article 33 GDPR; the breach
register is maintained by the coordinator.

## Block: Coordinated vulnerability disclosure

The project's grid-forming inverters, electrolyser control firmware, and
operational telemetry pipeline are in scope for cyber security review. The
consortium operates a coordinated vulnerability disclosure (CVD) policy
aligned with ISO/IEC 29147 and ISO/IEC 30111.

Reporting channel. A published security contact (security@project-domain)
and a PGP key are advertised on the project site at month three. Reports
are acknowledged within 72 hours and triaged within ten working days.

Triage and remediation. Vulnerabilities are scored using CVSS v3.1.
Critical and high findings carry a 90-day remediation target; medium and
low findings carry a 180-day target. Remediation status is tracked in a
private register held by the coordinator and the WP7 safety lead.

Disclosure timing. Coordinated public disclosure follows remediation,
typically at 90 days from the report, extendable by mutual agreement with
the reporter where remediation is non-trivial. Acknowledgement to the
reporter is offered subject to their preference.

Research safe harbour. Good-faith security research that complies with the
project's CVD policy is not pursued under computer-misuse or contract
provisions; the safe-harbour text is published alongside the policy.

NIS2 alignment. Where the host district falls under NIS2 essential or
important entity scope, the project's incident handling integrates with
the host's national cyber security authority reporting obligations, and
significant incidents are reported within the NIS2 24-hour and 72-hour
windows.

## Block: Quantified KPIs

The project commits to nine quantified key performance indicators, all measured
during the 36-month district campaign and the 24-month FCEV bench campaign, with
quarterly public telemetry release.

1. System availability >= 99.5% at the district site (excluding planned overhaul
   windows).
2. Electrolyser stack overhaul interval >= 20,000 operating hours in measured
   variable-input operation [IEA-GHR-2024].
3. O&M expenditure <= 3.5% of installed CapEx per annum, indexed.
4. Lifecycle GHG intensity of delivered hydrogen < 0.45 kgCO2e per kgH2 at the
   district gate, measured per RFNBO methodology [EU-RFNBO-1185].
5. Hydrogen leakage from production through dispense < 1% by mass, with on-site
   acoustic and tunable-diode-laser-spectroscopy verification [Sand-2023].
6. Freshwater draw from the host basin < 0.1% of basin annual renewable water
   resource, audited against the local water authority register.
7. Round-trip efficiency of the district hydrogen buffer (electricity to H2 to
   electricity) > 35% LHV measured.
8. FCEV bench fuel consumption within 10% of OEM-published kgH2/100km at the
   measured duty cycle.
9. Open-data publication latency: telemetry, model, and parameters released
   publicly within one calendar quarter of measurement.

## Block: Open Science / data management baseline

All project outputs follow the Horizon Europe and Innovation Fund Open Science and
data management defaults, with no opt-out invoked unless safety or
commercially-sensitive partner data justifies it under the Grant Agreement.

- Public model: the engineering and economic model is released under an
  OSI-approved open-source licence at project month three and updated at every
  milestone. Source, parameters, and unit tests are published together so that
  reviewers and replicators can rerun all cited tables.
- Public parameters: every techno-economic assumption (capex, opex, learning
  rate, discount rate, lifetime, RFNBO compliance assumptions) is exposed as
  a versioned parameter file with a changelog.
- Quarterly telemetry: from district commissioning onward, raw and one-minute-
  averaged operational telemetry is released quarterly under a permissive data
  licence. Personally-identifying or partner-confidential channels are
  redacted with a documented filter list.
- Peer-reviewed publication target: at minimum two Q1-journal papers (one on
  RFNBO-compliant variable-input operation, one on the lifecycle GHG and
  leakage measurement campaign) and one open-access dataset paper.
- Data Management Plan: produced at month six, updated at month eighteen and
  at project close, following the Horizon Europe DMP template.

## Block: Risk top 5

Five risks are tracked at programme level. Mitigations are budgeted in WP-level
contingency lines. Each risk is owned by a named WP lead at submission.

- R1. Hydrogen leakage exceeding the 1% mass target. Hydrogen has a global
  warming potential effect via atmospheric chemistry [Sand-2023]. Mitigation:
  redundant leak detection at every flange class, pre-commissioning helium leak
  test, and an explicit gate at WP4 commissioning that blocks operational
  acceptance until measured leakage < 0.5% over a two-week burn-in.
- R2. Bondability and durability of composite Type IV tanks under field cycling.
  Mitigation: accelerated-cycling qualification on representative tanks before
  district installation, and contracted spare inventory.
- R4. Grid interconnection delay or denial at the district site. Mitigation:
  parallel pursuit of islanded-mode acceptance criteria, so that the project
  can produce a measurement campaign even under a delayed interconnection
  agreement; early engagement with the host TSO/DSO documented at WP1.
- R6. RFNBO compliance audit failure under the additionality, temporal-
  correlation, and geographical-correlation rules of [EU-RFNBO-1184]. Mitigation:
  RFNBO-compliant PPA structure designed at WP3, third-party verification at
  WP5, and a documented fall-back accounting boundary if a renewable source
  becomes ineligible mid-project.
- R8. Tidal sub-system (T4) is pre-commercial. Mitigation: tidal is scoped as a
  variant only at coastal demonstrators and is not on the critical path for the
  inland district baseline; budget exposure to T4 is bounded and ring-fenced.

## Block: Decommissioning and circularity

Decommissioning and circularity are designed in at WP1 and bonded financially at
WP4 commissioning, not deferred to project end. Four streams are tracked.

- Platinum-group-metal recovery: PEM electrolyser and PEM fuel-cell catalyst
  layers are recovered through a contracted refiner under a take-back clause
  signed at procurement. The catalyst inventory is logged in kg-Pt and kg-Ir
  on the project asset register.
- Lithium-ion buffer recycling: any auxiliary battery storage on the district
  bus is procured under an extended-producer-responsibility contract aligned
  with the EU Batteries Regulation. End-of-life cells route to a licensed EU
  recycler with reported recovery yield.
- Composite tank protocol: Type IV hydrogen storage vessels follow a
  documented end-of-life protocol covering depressurisation, purge, mechanical
  perforation, separation of the polymer liner from the carbon-fibre overwrap,
  and recovery of the metal boss. Carbon-fibre regrind is offered to industrial
  off-takers; residual is incinerated under permit.
- Civil works: foundations and trenching are designed for full reversibility,
  with a decommissioning bond posted before commissioning.

## Block: Honest positioning vs alternatives

The project is positioned honestly against competing pathways and refuses to
claim universality.

- Battery-electric trucks (BEV) versus FCEV. For predictable duty cycles
  under approximately 500 km daily and depot-charging access, BEV is the lower-
  cost and lower-energy path; the model returns BEV TCO of $0.71/km versus
  FCEV $0.91 to $1.34/km depending on hydrogen price. FCEV is justified for
  duty cycles with long range, fast turnaround, and limited charging
  infrastructure (long-haul, port shuttle with high uptime, regional
  distribution in cold climates). The bench campaign is scoped to that
  segment, not to displace BEV in segments where BEV wins.
- Hydrogen internal-combustion engines (H2-ICE) are excluded. They retain the
  combustion-NOx pathway, deliver lower tank-to-wheel efficiency than fuel
  cells, and do not unlock the ancillary use cases (district stationary
  re-electrification, fuel-cell CHP) that justify the hydrogen infrastructure
  investment.
- Low-energy nuclear reactions (LENR) are excluded. The peer-reviewed
  assessment in [Berlinguette-2019] shows no reproducible excess-heat signal
  under controlled conditions; the project commits to TRL >= 4 grounded
  technology only.
- Grid-only electrification (no hydrogen) for the district is acknowledged as
  the dominant pathway where transmission and storage are cheap. The 2 MW
  district demonstrator is sited where seasonal mismatch, islanding
  requirements, or hard-to-abate thermal end-use justify the chemical
  carrier; the report does not generalise it to all districts.

