# NZ Funding - Proposal Skeleton (EECA GIDI / Callaghan Innovation / MBIE Endeavour)

> **Disclaimer.** Template document for grant proposal drafting. Numbers are illustrative; placeholders must be replaced before submission. Not legal, financial, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

*Numbers in this template are illustrative scenario outputs, traceable to public sources cited in `report/references.md`. Replace each placeholder with site-specific, jurisdiction-specific, and time-current values before submission. Submission to a funding programme is the responsibility of the submitting entity, not this template.*

Status: skeleton. Live numbers pulled from
`report/_generated_tables.md`
(model v0.1.0, params 214a7b5cb0b0). FX is indicative at 1 USD = 1.65 NZD;
re-run before submission.

---

## 1. Schemes overview

*Indicative budget; numbers are scenario outputs derived from cited public sources. Replace before submission. See DISCLAIMER.md.*

| Scheme | Administering body | Typical envelope | Fit |
|---|---|---|---|
| EECA GIDI (Government Investment in Decarbonising Industry) | Energy Efficiency and Conservation Authority | Up to approximately 50% of project capex, process-heat focus | District H2 plus heat coupling at descoped 1 MW scale |
| Callaghan Innovation R&D Project Grants | Callaghan Innovation | NZD multi-hundred-thousand to low-millions, 24-month R&D | Car-bench FCEV validation track |
| Callaghan Innovation Getting Started Grants | Callaghan Innovation | Smaller seed R&D awards | Pre-feasibility / scoping work |
| MBIE Endeavour Fund | Ministry of Business, Innovation and Employment | Research-led, multi-year | Research consortium pathway with NZ university partner |

NZ hydrogen and emissions policy context: [MBIE-NZ-H2-2023]
(NZ Hydrogen Roadmap), [NZ-ERP2] (Emissions Reduction Plan 2).

URL placeholders:
<!-- TODO: paste current EECA GIDI round URL from https://www.eeca.govt.nz/ -->
<!-- TODO: paste current Callaghan Innovation grant URL from https://www.callaghaninnovation.govt.nz/ -->
<!-- TODO: paste current MBIE Endeavour round URL from https://www.mbie.govt.nz/ -->

---

## 2. Call fit

- **Car-bench FCEV validation track** (24 months, NZD 1.65M envelope) maps
  best to a **Callaghan Innovation R&D Project Grant**. The scope and
  timeframe match Callaghan's typical envelope and 24-month R&D horizon.
- **District deployment** (2 MW, NZD 60M at full scale) is borderline for
  NZ's market and scheme scale. Two recommended pathways:
  - **(a) Descoped 1 MW district variant** matched to a South Island town
    (for example Taupo, Westport) or other resilience-priority community,
    targeting EECA GIDI for the process-heat / industrial-decarbonisation
    component, paired with a Callaghan R&D component for the integration
    work.
  - **(b) Cross-Tasman consortium** with an Australian counterpart
    leveraging the AU ARENA application for the bulk of the capex; NZ
    funders cover the NZ-side site, iwi engagement, and integration
    research.

---

## 3. NZ-specific positioning and Hydrogen Roadmap alignment

NZ's electricity system is already approximately 80% renewable on annual
average, dominated by hydro [NZ-ERP2]. **Honest framing**: NZ does *not*
need green hydrogen for grid decarbonisation in the way Australia or the
EU do. NZ's hydrogen demand case rests on the three priority end-uses
identified in the NZ Hydrogen Roadmap [MBIE-NZ-H2-2023].

- Heavy-duty trucking (long-haul SH1 and freight corridors) where BEV
  range and refuel-time constraints bind [MBIE-NZ-H2-2023]. The car-bench
  track addresses this priority.
- Industrial process heat where electrification is hard
  (high-temperature applications). The descoped 1 MW district track
  pairs an electrolyser with a process-heat off-take and is the EECA
  GIDI target.
- South Island grid resilience and dry-year firming, where stored
  hydrogen is one option in the firming portfolio. The descoped 1 MW
  district track demonstrates the firming use case at community scale.

This proposal targets all three priorities in proportion to the
proposing tracks. It does not claim hydrogen is the cheapest grid-firming
option in NZ; it claims hydrogen is a defensible component of a
diversified resilience portfolio for specific sites, consistent with
[MBIE-NZ-H2-2023] and the firming options discussed in [NZ-ERP2].

The project's published parameter set and quarterly telemetry are
designed for direct ingestion into MBIE's Hydrogen Roadmap monitoring,
including a feedback channel to the roadmap's responsible officials at
six-month intervals during the project.

---

## 4. Project description

### Block: Technology approach

Water-medium energy: green hydrogen produced by water electrolysis from
on-site renewables (hydro-coupled or PV depending on site). Hydrogen is
stored on site and dispatched to (a) a stationary fuel cell for firming
and (b) a Class 8 truck refuelling point for the bench-validation track.
The stack is grounded in current commercial PEM/alkaline electrolyzer
technology and demonstrated PEM fuel-cell modules; no speculative
chemistries. LENR / cold-fusion pathways are explicitly excluded;
see Section 10 and [Berlinguette-2019].

---

## 5. Knowledge sharing

- **Callaghan Innovation** R&D Project Grants offer flexible IP-sharing
  arrangements: this proposal commits to background-IP retention by
  proponent, with foreground IP either jointly held with Callaghan or
  released under permissive licence subject to negotiation.
- **MBIE Endeavour** carries an open-publication expectation: this
  proposal commits to peer-reviewed publication of integrated-operation
  results and to public release of the techno-economic model and
  parameter set, consistent with the maintenance rule in
  `references.md`.
- Quarterly operational telemetry will be released for the district
  variant in alignment with NZ open-data norms.

---

## 6. Budget (NZD, indicative at 1 USD = 1.65 NZD)

*Indicative budget; numbers are scenario outputs derived from cited public sources. Replace before submission. See DISCLAIMER.md.*

| Track | USD basis | NZD (indicative) |
|---|---|---|
| Car-bench FCEV (24 months) | $1.0M | NZD 1.65M |
| District descoped 1 MW (24 to 30 months) | $18M (approximately scaled inland solar plus H2) | NZD 30M |
| District full 2 MW (36 months) | $36M envelope | NZD 60M |

Live USD basis from `_generated_tables.md`: inland solar plus H2 $27.0M,
river micro-hydro $20.3M, coastal tidal $24.2M (all 2 MW). The NZD 30M
descoped figure assumes approximately 50% capex scaling for the 1 MW
variant; refresh with a model run before lodgement.

The full 2 MW (NZD 60M) is likely too large for any single NZ scheme and
should be bundled with an Australian co-funder (see Section 2 pathway b)
or staged.

Car-bench track (NZD 1.65M) sits inside Callaghan R&D Project Grant
envelopes. Callaghan grant intensity placeholder: 40% = NZD 0.66M;
balance via OEM in-kind and proponent.

---

## 7. Te Tiriti o Waitangi and iwi engagement framework

Engagement with mana whenua is mandatory for any siting in Aotearoa New
Zealand and is reviewer-sensitive across EECA, Callaghan, and MBIE. Crown
funders carry Te Tiriti obligations that flow through to grant
recipients; the framework below is the operating model for the project
and is referenced in the project ethics deliverable.

Te Tiriti principles in operation. The project recognises the three
guiding principles applied by Crown agencies in funding decisions:
partnership, participation, and active protection. Each principle is
operationalised below.

Partnership.

- Pre-application engagement with the host iwi for any candidate site,
  initiated before scheme lodgement.
- A formal partnership agreement with the host iwi or its delegated
  authority (runanga or post-settlement governance entity), executed
  before financial close, covering scope, decision rights, and
  dispute resolution.
- Iwi representation on the project steering committee with voting
  rights on site-selection and consenting decisions.

Participation.

- Co-design of the site-selection and consenting plan with iwi
  representatives.
- Cultural impact assessment commissioned and led by the host iwi
  under their preferred methodology, before any ground disturbance.
- Iwi-led training and employment pathway during construction and
  operation, with documented places, mentoring, and progression.

Active protection.

- Wahi tapu and cultural heritage values surveyed and protected under
  the Heritage New Zealand Pouhere Taonga Act 2014, with an accidental
  discovery protocol agreed before construction.
- Freshwater values addressed under Te Mana o te Wai under the
  National Policy Statement for Freshwater Management 2020, where the
  electrolyser draws from a basin within iwi rohe.

Benefits-sharing.

- Equity participation, training places, operational employment,
  and revenue share to be agreed with the host iwi during
  pre-application engagement under a documented benefits-sharing
  model.

Data sovereignty.

- Telemetry collected on iwi-associated land follows a documented data
  sovereignty protocol agreed with the host iwi, consistent with Maori
  Data Sovereignty principles. The protocol covers data ownership,
  access, redaction rights, and the publication consent pathway for
  the quarterly telemetry release.

This is not a tick-box section. Funders read it carefully and the draft
framework will be revised with iwi input before any final lodgement.

---

## 8. Milestones (NZ scheme milestone-payment alignment)

Car-bench track (Callaghan R&D, 24 months):

| # | Milestone | Month | Payment trigger |
|---|---|---|---|
| C1 | Bench rig design frozen, OEM partnership executed | 3 | Design gate |
| C2 | Long-lead components procured | 6 | PO evidence |
| C3 | Bench rig built and instrumented | 12 | Commissioning report |
| C4 | First 500 hours validated operation | 18 | Telemetry release |
| C5 | Final report and peer-reviewed publication | 24 | Publication |

District descoped 1 MW track (EECA GIDI plus Callaghan, 30 months):

| # | Milestone | Month | Payment trigger |
|---|---|---|---|
| D1 | Iwi engagement complete, host site agreements signed | 4 | Mobilisation |
| D2 | Detailed engineering design frozen | 8 | Design gate |
| D3 | Long-lead procurement placed | 11 | PO evidence |
| D4 | Civil works complete | 17 | PCC |
| D5 | Electrolyzer commissioned (cold) | 22 | Cold-commissioning report |
| D6 | Energised and operational | 26 | Energisation certificate |
| D7 | 1,000 hours integrated operation | 28 | Telemetry release |
| D8 | Final report, public dataset, publication | 30 | Publication |

---

## 9. Risk register (top 5)

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Electrolyzer capex overruns vs model | Med | High | Fixed-price EPC; reference-class pricing; 15% contingency. |
| R2 | Renewables / hydro yield below P50 in dry year | Med | Med | Site-specific resource study; dry-year sensitivity in model run; storage sizing on P90 inflows. |
| R3 | Iwi engagement timeline slippage | Med | High | Pre-application engagement before scheme lodgement; engagement budget protected; milestone D1 explicit. |
| R4 | NZ market scale insufficient for 2 MW offtake | Med | High | Descoped 1 MW pathway as default; offtake heads of agreement at D1. |
| R5 | Permitting and consenting delays under RMA | Med | Med | Early consenting strategy with planner engaged at M0; reference comparable AS/NZS gas-storage codes [AS-NZS-1596]. |

---

## 10. Honest positioning

### BEV vs FCEV (Class 8 trucking)

On the live model numbers (USD), BEV Class 8 reference TCO is $0.712/km
and diesel reference is $0.781/km. FCEV TCO ranges $0.907 to $1.343/km
across the H2 = $4 to $9/kg band. At current costs, BEV beats FCEV on TCO
for Class 8 duty cycles where range and refuel time permit. FCEV is
justified on this proposal where (i) duty cycle exceeds BEV range with
current energy density, (ii) refuel time is a binding operational
constraint, or (iii) the host site already produces hydrogen and the
truck bench rides the marginal-cost curve. We do not claim FCEV beats
BEV in general; we claim it is competitive in a defined operating
envelope, and we will publish the envelope. NZ's long-haul SH1 freight
corridors are a candidate envelope [MBIE-NZ-H2-2023].

### LENR exclusion

Low-energy nuclear reactions (LENR / "cold fusion") are out of scope.
The multi-laboratory, multi-year null result in [Berlinguette-2019]
remains the operative evidence base. No project budget line, milestone,
or KPI depends on LENR.
