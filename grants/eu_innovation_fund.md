# EU Innovation Fund (CINEA) - Proposal Skeleton

> **Disclaimer.** Template document for grant proposal drafting. Numbers are illustrative; placeholders must be replaced before submission. Not legal, financial, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

*Numbers in this template are illustrative scenario outputs, traceable to public sources cited in [report/references.md](../report/references.md). Replace each placeholder with site-specific, jurisdiction-specific, and time-current values before submission. Submission to a funding programme is the responsibility of the submitting entity, not this template.*

This skeleton is structured to mirror the Innovation Fund Part B template as
operated by the European Climate, Infrastructure and Environment Executive
Agency (CINEA). Reusable narrative blocks are imported by quote from
[_shared_narrative.md](_shared_narrative.md) in this directory.

Indicative numbers are marked "indicative" and must be reset to call-specific
unit costs at submission. URL placeholders use the format
`<!-- TODO: paste current call URL from https://ec.europa.eu/info/funding-tenders/opportunities/ -->`;
the portal root is shown as a hint to the human writer and is not a citation.

---

## 1. Scheme summary

The Innovation Fund is operated by CINEA on behalf of the European
Commission and funds the demonstration of innovative low-carbon
technologies at near-commercial readiness. Two project tracks are
relevant:

- Large-scale projects, with total capital expenditure greater than
  EUR 7.5M, evaluated against five award criteria: GHG emission avoidance,
  degree of innovation, project maturity, scalability, and cost efficiency
  (measured as GHG avoidance per EUR of Innovation Fund support).
- Small-scale projects, with total capital expenditure not exceeding
  EUR 7.5M, with a simplified evaluation that retains the same five
  criteria.

Funding intensity is up to 60% of the project's "relevant cost", defined as
the incremental cost of the innovative project relative to a conventional
reference scenario, including capex and ten years of operating cost delta
under the published CINEA cost methodology. Disbursement is up to fifteen
years and is split between a project-development grant (front-loaded) and
milestone-based payments across construction and operation. Innovation Fund
projects are expected at TRL >= 7, that is, close to commercial deployment.

CINEA imposes a 10-year monitoring and reporting obligation on funded
projects, starting from entry into operation. Annual operating reports
cover measured GHG avoidance, knowledge sharing outputs, and any material
changes to the operating envelope; failure to meet committed avoidance
without justification can trigger clawback.

The strategic framing is REPowerEU [EC-REPowerEU], which makes
demonstration of replicable RFNBO-compliant production at scale a
priority for Innovation Fund support.

`<!-- TODO: paste current call URL from https://ec.europa.eu/info/funding-tenders/opportunities/ -->`

## 2. Call fit narrative

The 2 MW district hybrid microgrid track is a small-to-medium-scale
Innovation Fund replication candidate. Its CapEx envelope of $20.3M to
$27.0M [model-tables] (indicative EUR 19M to 25M at 1.08 USD/EUR) places
it above the small-scale threshold and within the medium-large band.
The project is RFNBO-compliant by design [EU-RFNBO-1184],
[EU-RFNBO-1185], it is at TRL 6 to 7 progressing to TRL 8 at commissioning,
and it is explicitly framed for replication across at least four EU
geographies (see Section 7).

The FCEV Class 8 truck bench-validation track is honestly NOT a fit for
the Innovation Fund. The bench envelope of $1M / 24 months is below the
practical Innovation Fund threshold; the bench campaign is at TRL 5 to 6
rather than the >= 7 expected by the Fund; and the deliverable is a
measurement campaign rather than a deployable revenue-generating asset.
The FCEV track is better routed via Horizon Europe Cluster 5 (see the
Cluster 5 skeleton in this directory) or via the Clean Hydrogen Joint
Undertaking. This proposal recommends the bifurcation: district to
Innovation Fund, FCEV bench to Cluster 5 / CHJU.

## 3. Project description

The project description is built from three reusable narrative blocks
imported from [_shared_narrative.md](_shared_narrative.md):

- Block: Technology approach. The seven grounded water-medium
  technologies T1 through T7, hydrogen as an energy carrier, with
  live CapEx and LCOH numbers from the open model.
- Block: Quantified KPIs. The nine measured KPIs covering
  availability, stack overhaul, O&M, lifecycle GHG, leakage, water
  draw, round-trip efficiency, FCEV consumption, and open-data
  publication latency.
- Block: Honest positioning vs alternatives. The explicit comparison
  with BEV, the exclusion of H2-ICE on efficiency grounds, the
  exclusion of LENR per [Berlinguette-2019], and the
  acknowledgement that grid-only electrification is the dominant
  pathway where transmission and storage are cheap.

The Innovation Fund evaluates project maturity heavily; the
descriptions in those three blocks are written specifically to be
defensible against a maturity reviewer (named technologies, named
suppliers at submission, measured rather than modelled performance
where the model is uncertain).

## 4. Impact

GHG avoidance. The project quantifies lifecycle GHG intensity of
delivered hydrogen at < 0.45 kgCO2e per kgH2 [EU-RFNBO-1185]. Against
a hydrogen-from-natural-gas-without-CCS reference of approximately
9 to 12 kgCO2e per kgH2 [IEA-GHR-2024], one tonne of project-delivered
hydrogen avoids on the order of 9 to 11 tonnes of CO2 equivalent at
the project gate, before any further avoidance from the end-use
displacement of diesel.

GHG avoidance per EUR of Innovation Fund support. CINEA's cost
efficiency criterion is measured in tonnes of CO2 equivalent avoided
per EUR awarded. At an indicative EUR 15M IF support and an
indicative ten-year cumulative GHG avoidance of approximately 0.4 to
1.2 Mt CO2e (calculated against a realistic operating duty cycle and
a mixed counterfactual of grid electricity and diesel for stationary
and transport end-uses), the implied cost efficiency is roughly 27
to 80 tCO2e per EUR thousand awarded. This sits within the band of
recent Innovation Fund precedents in renewable hydrogen. Numbers are
indicative and recomputed against the model at submission.

Replicability. See Section 7. The project is explicitly designed for
replication, with the DMP, model, and parameter releases enabling
third parties to compute their own site-specific business case
without proprietary handover.

Financial bankability. Two scenarios are presented at submission. The
with-grant scenario brings LCOH into the EUR 2 to 5 per kg band that
matches the foreseeable EU industrial off-take willingness-to-pay
[EC-H2-Strategy]; the no-grant scenario stresses LCOH at the upper
end of the model's range and identifies the threshold off-take price
at which the project is bankable on commercial debt. The
sensitivity analysis is reproducible from the open model.

System integration. The project is RFNBO-compliant under
[EU-RFNBO-1184] additionality, temporal correlation and
geographical correlation. It is grid-forming-capable and provides
ancillary services (frequency response and reactive support) to the
host DSO under a separate ancillary-service agreement. Off-take is
contracted before financial close.

10-year monitoring obligation. CINEA's standard reporting horizon
runs from entry into operation. The project commits to annual
operating reports covering measured GHG avoidance, dispatched
hydrogen volumes, RFNBO compliance audit results, and the four
circularity streams in Block: Decommissioning and circularity. The
quarterly telemetry release is the public-facing complement to the
private CINEA report. Knowledge-sharing reports follow the
Innovation Fund template at year three, year six, and year ten.

## 5. Maturity (TRL evidence)

Component-level TRL at submission. The Innovation Fund expects
maturity evidence per critical sub-system; the table below is the
defensible position at submission.

| Component                                | TRL at submission | Evidence type                                  |
|------------------------------------------|------------------|-----------------------------------------------|
| Alkaline / PEM electrolyser stack        | 8-9              | Vendor field-fleet hours [IEA-GHR-2024]       |
| Electrolyser MW-scale system integration | 7                | Vendor reference plants under variable input   |
| PV generation (T2)                       | 9                | Mass-deployment commercial product             |
| Micro-hydro (T3)                         | 8-9              | Long-running deployments at host class         |
| Tidal-stream (T4)                        | 5-6              | Pre-commercial; ring-fenced as risk R8         |
| Compressed H2 storage Type IV (T5)       | 8                | Type-approved vessels in service               |
| PEM fuel cell stationary (T6)            | 7-8              | Vendor field deployments                        |
| Grid-forming inverters and BoP (T7)      | 8                | Vendor reference deployments                    |
| Integrated 2 MW district hybrid system   | 6 to 8           | This project's commissioning closes the gap   |

The integrated-system TRL transition from 6 to 8 across the project
period is the Innovation Fund deliverable.

## 6. Budget. Relevant cost methodology

The Innovation Fund evaluates a "relevant cost" computed under CINEA's
published cost methodology. The methodology takes the incremental capex
and the ten-year operating cost delta against a conventional reference
scenario, with discounting and reference-case parameters as specified by
CINEA in force at the call publication date. The indicative figures
below are generated from the open model and reset at submission against
the live methodology version.

- District CapEx (project case, anchored to model): approximately
  $24.0M average across the three configurations [model-tables],
  or indicative EUR 22M.
- District CapEx (reference case, conventional grid plus diesel/gas
  thermal): indicative EUR 6M.
- Incremental CapEx: indicative EUR 16M.
- Ten-year operating cost delta (project minus reference, including
  RFNBO-compliant electricity sourcing premium and netting against
  avoided diesel and grid imports): indicative EUR 14M.
- Total relevant cost under CINEA methodology: indicative EUR 30M.
- Innovation Fund ask at 50% intensity: indicative EUR 15M (within
  the 60% ceiling, with 10% headroom held in reserve).

The relevant-cost calculation follows the CINEA methodology document
referenced at the call. All numbers are indicative; the
submission-time relevant-cost calculation is generated from the open
model at the reset parameter point and audited against the
methodology in force.

## 7. Replicability and scalability

Replication is from a 2 MW pilot to 20 MW within the EU within five
years of the pilot's commissioning. Four named candidate geographies
are identified, each matched to one of the project's renewable input
configurations.

- Iberia. High-irradiance inland sites suitable for the PV-driven
  configuration (model: $27.0M CapEx, $1.90/kg LCOH); strong RFNBO
  additionality given the existing renewable build-out and PPA
  market depth.
- Nordics. River-adjacent sites suitable for the micro-hydro
  configuration (model: $20.3M CapEx, $4.30/kg LCOH); the low LCOE
  of regulated hydropower offsets the higher CapEx of the hydraulic
  works.
- Mediterranean. Coastal demonstrators suitable for the tidal-
  stream variant (model: $24.2M CapEx, $5.22/kg LCOH); explicitly
  scoped as a pre-commercial demonstrator under risk R8, not as a
  baseline replication.
- Central Europe. Inland sites with mixed renewable input and
  district heat off-take; the project's open model permits
  site-specific re-parameterisation by replicators.

Scalability beyond 20 MW is supported by the modular electrolyser
architecture (T1) and by the independence of the grid-forming inverter
control plane from site size (T7); the limiting factors at the
50-100 MW scale are interconnection, water permitting, and PGM
supply, all three of which are flagged in Block: Risk top 5 and Block:
Decommissioning and circularity.

## 8. Open Science, DMP, Risk top 5

Open Science. Import [_shared_narrative.md](_shared_narrative.md) Block: Open Science /
data management baseline. The Innovation Fund's mandatory
knowledge-sharing reports are satisfied by the project's open model,
parameter, and quarterly telemetry releases. The
knowledge-sharing deliverable is delivered as a public-facing
version of the project's annual report at years three, six, and ten.

Data Management Plan. Delivered at month six, updated at month
eighteen, and updated at project close, following the Horizon
Europe DMP template (interoperable with the Innovation Fund's
reporting expectations).

Risk top 5. Import [_shared_narrative.md](_shared_narrative.md) Block: Risk top 5. R1
(hydrogen leakage <1% target [Sand-2023]), R2 (composite tank
bondability), R4 (grid interconnect), R6 (RFNBO compliance under
[EU-RFNBO-1184]), R8 (tidal pre-commercial, ring-fenced).

Decommissioning and circularity. Import [_shared_narrative.md](_shared_narrative.md)
Block: Decommissioning and circularity. The decommissioning bond is
posted before commissioning; the four streams (PGM recovery,
Li-ion recycling, composite tank protocol, civil works
reversibility) are tracked on the project asset register.

GDPR, ethics, and CVD. Import [_shared_narrative.md](_shared_narrative.md) Block: GDPR
and data protection, Block: Ethics, gender equality plan, and
public engagement, and Block: Coordinated vulnerability disclosure.
These apply during construction and across the 10-year monitoring
period.

---

Citations resolve in
[report/references.md](../report/references.md). Live
numbers are sourced from
[report/_generated_tables.md](../report/_generated_tables.md)
(model v0.1.0). Reusable narrative blocks live in
[grants/_shared_narrative.md](_shared_narrative.md).
