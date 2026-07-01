# ARENA Funding Round - Proposal Skeleton

> **Disclaimer.** Template document for grant proposal drafting. Numbers are illustrative; placeholders must be replaced before submission. Not legal, financial, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

*Numbers in this template are illustrative scenario outputs, traceable to public sources cited in [report/references.md](../report/references.md). Replace each placeholder with site-specific, jurisdiction-specific, and time-current values before submission. Submission to a funding programme is the responsibility of the submitting entity, not this template.*

Status: skeleton. Live numbers pulled from
[report/_generated_tables.md](../report/_generated_tables.md)
(model v0.1.0, params 214a7b5cb0b0). FX is indicative at 1 USD = 1.5 AUD;
re-run before submission.

---

## 1. Scheme summary

Two complementary Australian Renewable Energy Agency (ARENA) channels are in
scope:

- **ARENA general funding rounds**. Competitive, theme-led calls covering
  renewables, storage, hydrogen production and end-use, and integrated
  microgrid demonstrations. Typical ARENA grant intensity is 30 to 50% of
  eligible project capex, with the balance carried by proponent and
  co-investors. Technology Readiness Level (TRL) bracket 4 to 8
  [ARENA-H2].
- **Hydrogen Headstart**. A production-credit-style program (approximately
  AUD 2 billion envelope) targeting large electrolyzer projects to close
  the cost gap toward AUD 2/kg green hydrogen [ARENA-H2]. Headstart is
  structured for GW-scale producers and is *not* a fit for the
  demonstration scales below; this proposal positions as downstream
  demand-side architecture for future Headstart-funded supply (see
  Section 5 for detailed Headstart positioning).

Australian system context for renewables build-out and hydrogen demand is
drawn from the AEMO Integrated System Plan 2024 [AEMO-ISP-2024].

URL placeholder:
<!-- TODO: paste current round URL from https://arena.gov.au/funding/ -->

---

## 2. Call fit

The project has two technical tracks, each with a distinct funding logic:

- **District track**. 2 MW district hybrid microgrid with on-site green
  hydrogen via electrolysis, 36-month build, capex envelope under
  AUD 54M. Maps directly to ARENA's hydrogen and microgrid streams.
  This track is the *primary* ARENA ask.
- **FCEV truck track**. Class 8 fuel-cell electric vehicle (FCEV)
  bench-validation rig under AUD 1.5M, 24-month timeline. Could fit
  ARENA's heavy-vehicle hydrogen demonstration program but is more
  naturally housed in a heavy-duty truck OEM partnership where the
  OEM contributes tractor and drivetrain in-kind.

**Recommendation: bifurcate.** Lead the ARENA application with the district
track. Submit the car-bench track as either an add-on co-funded line or via
a partner-led pathway with a heavy-duty OEM and a state co-funder.

---

## 3. Project description

### Block: Technology approach

Water-medium energy: green hydrogen produced by water electrolysis from
on-site renewables (PV, wind, micro-hydro, or tidal depending on site).
Hydrogen is stored on site and dispatched to (a) a stationary fuel cell for
firming the district microgrid and (b) a Class 8 truck refuelling point.
The stack is grounded in current commercial PEM/alkaline electrolyzer
technology and demonstrated PEM fuel-cell modules; no speculative
chemistries. LENR / cold-fusion pathways are explicitly excluded; see
Section 11 and [Berlinguette-2019].

### Block: Quantified KPIs

Live model output (USD; AUD figures in Section 6):

*Scenario output, not a forecast. Indicative numbers; replace at submission. See DISCLAIMER.md.*

| KPI | Value |
|---|---|
| District inland (solar plus H2) capex | $27.0M |
| District inland LCOE | $214/MWh |
| District inland LCOH | $1.90/kg |
| District river (micro-hydro) capex | $20.3M |
| District river LCOE | $160/MWh |
| District river LCOH | $4.30/kg |
| District coastal (tidal) capex | $24.2M |
| District coastal LCOE | $198/MWh |
| District coastal LCOH | $5.22/kg |
| FCEV Class 8 TCO at H2 = $4/kg | $0.907/km |
| FCEV Class 8 TCO at H2 = $6/kg | $1.082/km |
| FCEV Class 8 TCO at H2 = $9/kg | $1.343/km |
| BEV Class 8 reference TCO | $0.712/km |
| Diesel Class 8 reference TCO | $0.781/km |

All figures from [_generated_tables.md](../report/_generated_tables.md) at params hash 214a7b5cb0b0.

---

## 4. Three site variants. Australian relevance

*Scenario output, not a forecast. Indicative numbers; replace at submission. See DISCLAIMER.md.*

| Variant | AU regional fit | Capex (USD) | LCOE | LCOH |
|---|---|---|---|---|
| Coastal-tidal | Tasmania (Bass Strait), WA south coast | $24.2M | $198/MWh | $5.22/kg |
| River-adjacent micro-hydro | Tasmania, Snowy region, NE NSW | $20.3M | $160/MWh | $4.30/kg |
| Inland solar-only | Pilbara, SA Mid-North, NSW Western | $27.0M | $214/MWh | $1.90/kg |

Numbers from [_generated_tables.md](../report/_generated_tables.md). Inland solar-only is the lowest-LCOH
variant and aligns with the Pilbara hydrogen hub mapping in
[AEMO-ISP-2024]. Tidal LCOH is materially higher and is presented as a
resilience-led variant for islanded coastal communities, not as a
cost-leader.

---

## 5. Strategic fit with Australia's Pathway to AUD 2/kg and Hydrogen Headstart

Australia's stated industrial-policy aim is to drive green hydrogen toward
AUD 2/kg via large electrolyzer deployments under Hydrogen Headstart
[ARENA-H2]. This proposal positions explicitly as a Headstart-complement,
not a Headstart-competitor.

Headstart targets GW-scale supply via a production-credit instrument
covering an annual subsidy on each kilogram of contracted green hydrogen
delivered. The instrument's structural requirement is a credible
GW-scale offtake stack; that requirement is the binding constraint on
Headstart project economics, not on the per-kilogram production cost
alone. Demand-side architecture at community scale is a missing input to
the Headstart offtake case.

How this project supports Headstart-funded supply.

- The 2 MW district platform proves integrated electrolyzer / fuel-cell /
  microgrid operation at a community scale, generating telemetry that
  Headstart-funded supply projects need to size downstream offtake.
- The inland solar-only LCOH of $1.90/kg sits inside the Pathway-to-AUD 2
  trajectory and provides early evidence that demand-side architecture
  can absorb hydrogen at the target price band [ARENA-H2].
- The published parameter set lets Headstart applicants integrate
  community-scale demand into their offtake stack without proprietary
  handover, which compresses the Headstart financial-close timeline.
- The truck-bench track produces the heavy-duty TCO envelope that
  Headstart-funded supply projects can use to underwrite long-haul
  transport offtake.

The proposal does not duplicate Headstart and does not seek Headstart
funding. It de-risks the offtake side.

---

## 6. Budget (AUD, indicative at 1 USD = 1.5 AUD)

District track, 36 months:

*Indicative budget; numbers are scenario outputs derived from cited public sources. Replace before submission. See DISCLAIMER.md.*

| Line | AUD (indicative) |
|---|---|
| District build, 2 MW (mid case capex USD 36M cap) | AUD 54M |
| ARENA grant ask (40% intensity) | AUD 22M |
| CEFC concessional debt (placeholder) | AUD 18M |
| State government co-funding (placeholder) | AUD 8M |
| Community / proponent equity (placeholder) | AUD 6M |
| **Total** | **AUD 54M** |

FX and co-funding are indicative; refresh against current spot and against
specific co-funder term sheets before lodgement. Live USD numbers per site
variant ($20.3M to $27.0M) sit below the AUD 54M envelope ceiling; the
envelope is sized for the upper-bound site plus contingency.

Car-bench track (24 months, optional add-on): under AUD 1.5M; ARENA share
indicative 40% = AUD 0.6M; OEM in-kind balance.

---

## 7. Knowledge sharing (ARENA standard terms)

ARENA-funded projects carry a mandatory knowledge-sharing obligation under
the ARENA standard funding terms. The obligation is a contractual
deliverable, not a discretionary best-effort, and ARENA's standard terms
require both ongoing sharing during the project and a final lessons-learned
report at completion. This proposal sets out how each component of the
standard terms is met.

Ongoing knowledge-sharing during the project:

- Public release of the techno-economic model and assumption set (the
  `electicity_model` codebase and `tech_params.yaml`) at month three,
  updated at every milestone gate.
- Public release of all configurable parameters with traceable citations
  (per the maintenance rule in [references.md](../report/references.md)).
- Quarterly operational telemetry release covering electrolyzer load
  factor, fuel-cell dispatch, microgrid SAIDI/SAIFI proxies, and hydrogen
  throughput, beginning at first commissioning (M5).
- Presentation at each ARENA Insights Forum during the project lifetime.
- Knowledge-sharing milestone reports filed at M3, M6, M9, and at every
  payment milestone, in the ARENA template.

End-of-project deliverables:

- Final lessons-learned report covering technical performance against
  forecast, financial performance against forecast, and a candid
  assessment of what would be done differently at a replication site.
- At least one peer-reviewed publication on integrated operation.
- Conference presentations at ARENA knowledge-sharing forums and at one
  international hydrogen forum.
- Public dataset release covering the full project measurement campaign.

Confidentiality and IP. Background IP is retained by the proponent;
foreground IP is released under a permissive licence subject to ARENA
standard terms. Commercially-sensitive supplier data is excluded from
public release with a documented redaction list approved by ARENA.

---

## 8. Native Title and First Nations consultation framework

Engagement with Traditional Owners is mandatory for any siting in Australia
and is reviewer-sensitive across ARENA, CEFC, and state co-funders. The
framework below applies to every candidate site and is referenced in the
project ethics deliverable.

Pre-application stage:

- Identification of registered native title parties, registered Aboriginal
  parties, and any prescribed body corporate (PBC) with statutory authority
  over the candidate site, via the National Native Title Tribunal register
  and the relevant state register.
- Initial engagement with the PBC or representative body before scheme
  lodgement, with cultural heritage scoping in scope.
- Pre-application meeting with the relevant state Aboriginal heritage
  authority.

Project stage:

- Negotiation of an Indigenous Land Use Agreement (ILUA) where a registered
  native title determination applies, or an equivalent access agreement
  where the title status is otherwise.
- Cultural Heritage Management Plan developed jointly with the PBC under
  the relevant state heritage act, before any ground disturbance.
- Co-design of the site-selection and consenting plan with First Nations
  representatives.

Benefits-sharing:

- Equity participation, training places, operational employment, and
  revenue share to be agreed with the PBC during pre-application
  engagement under a documented benefits-sharing model.
- Local content and Indigenous procurement targets carried in the EPC
  contract.

Data sovereignty:

- Telemetry collected on First Nations land follows a documented data
  sovereignty protocol agreed with the PBC; the protocol covers data
  ownership, access, redaction rights, and the publication consent
  pathway for the quarterly telemetry release.

This is not a tick-box section. ARENA and state co-funders read it
carefully and the draft framework will be revised with First Nations input
before any final lodgement.

---

## 9. Milestones M1 to M10 and ARENA milestone-based payments

| # | Milestone | Month | Payment trigger |
|---|---|---|---|
| M1 | Site selection and host agreements signed | 3 | Mobilisation |
| M2 | Detailed engineering design frozen | 6 | Design gate |
| M3 | Long-lead procurement (electrolyzer, fuel cell) placed | 9 | PO evidence |
| M4 | Civil works complete | 15 | Practical completion certificate |
| M5 | Electrolyzer commissioned (cold) | 21 | Cold-commissioning report |
| M6 | Microgrid energised and synchronised | 24 | Energisation certificate |
| M7 | First continuous hydrogen production at nameplate | 27 | Throughput report |
| M8 | First 1,000 hours integrated operation | 30 | Telemetry release |
| M9 | Full-year telemetry public dataset | 36 | Public dataset |
| M10 | Final knowledge-sharing report and peer-reviewed paper | 36 | Publication |

ARENA payments tracked against M1 to M10 with retention released at M10.

---

## 10. Risk register (top 5)

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Electrolyzer capex overruns vs model | Med | High | Fixed-price EPC contract; supplier reference-class pricing; 15% contingency. |
| R2 | Renewables yield below P50 | Med | Med | Site-specific resource study before M2; oversize PV/wind by P90/P50 ratio. |
| R4 | Hydrogen offtake demand below model | Med | High | Pre-signed offtake heads of agreement (district anchor plus truck bench) at M1. |
| R8 | Permitting and DA delays (NFPA 2 / AS-NZS analogues) | Med | Med | Early engagement with state planning authority; pre-application reference to [NFPA-2] and [AS-NZS-1596]. |
| R6 | Skilled-labour shortage at commissioning | Med | Med | OEM commissioning crews contracted at M3; local TAFE training partnership. |

---

## 11. Honest positioning

### Block: Honest positioning. BEV vs FCEV

On the live model numbers, BEV Class 8 reference TCO is $0.712/km and
diesel reference is $0.781/km. FCEV TCO ranges $0.907 to $1.343/km across
the H2 = $4 to $9/kg band. **At today's costs, BEV beats FCEV on TCO for
Class 8 duty cycles where range and refuel time permit.** FCEV is justified
on this proposal where (i) duty cycle exceeds BEV range with current
energy density, (ii) refuel time is a binding operational constraint, or
(iii) the host site already produces hydrogen for other reasons (the
district track) and the truck bench rides the marginal-cost curve. We do
not claim FCEV beats BEV in general. We claim it is competitive in a
defined operating envelope, and we will publish the envelope.

### LENR exclusion

Low-energy nuclear reactions (LENR / "cold fusion") are out of scope.
The multi-laboratory, multi-year null result in [Berlinguette-2019]
remains the operative evidence base. No project budget line, milestone,
or KPI depends on LENR.
