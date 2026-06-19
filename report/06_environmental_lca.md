# 06 - Environmental Lifecycle Analysis

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

## Direct GHG (operational)

The district has zero direct combustion. Fuel cells emit only water vapour. Solar PV operational emissions are zero. Embodied emissions are dominated by stack manufacturing (PGM smelting), PV modules, battery cells, and civil works.

The truck has zero tailpipe NOx, PM, and CO2. Embodied stack and tank emissions amortise over 1.6 million km of duty cycle.

The lifecycle GHG target is **less than 0.45 kg CO2e per kg H2** for the project's hydrogen, matching IRA section 45V Tier 1 and EU RFNBO criteria [IRA-45V, EU-RFNBO-1185]. This is enforced through:

- **Additionality.** New renewable capacity is contractually matched to the electrolyzer (post-2024 plant, per the US Treasury final rule and the EU 2023/1184 transitional schedule).
- **Hourly temporal correlation.** Phased per the same regulations, with a 2030 baseline.
- **Geographic deliverability.** Renewable plant on the same regional grid (per the delegated act's bidding-zone definition and FERC interconnection-region equivalents).

## Indirect GHG: hydrogen leakage

Hydrogen has indirect radiative forcing through OH and CH4 chemistry. The best current estimate is **GWP100 of about 11.6, with a 2.8 uncertainty band** [Sand-2023]. The project's leakage budget is **less than 1 percent** of value-chain throughput. Three controls support that budget:

- Continuous leak detection at the electrolyzer, storage, and fuel-cell stages (see Chapter 07).
- Annual integrity audit.
- Open public reporting of measured leakage as part of the Open Science deliverable.

If leakage rises to 3 percent (the industry whisper number for poorly maintained systems), the indirect-forcing penalty per kg of H2 is 11.6 times 0.03, or about 0.35 kg CO2e/kg H2. That value alone breaches the 45V Tier 1 threshold. **Leakage discipline is not optional for this project.**

## Water draw

- Stoichiometric: 9 L per kg H2.
- Real-world (purification plus cooling): 18 to 30 L per kg H2 [IEA-GHR-2024].
- Project model assumes 22 L/kg.
- The inland 2 MW district produces about 150 t H2/year, which is roughly 3,300 m3 process water plus 5,000 m3 cooling water.
- The project commits to host-site selection that places this draw at less than 0.1 percent of basin annual renewal per WRI Aqueduct 4.0 [WRI-Aqueduct-4].

Sites with WRI Aqueduct "Extremely High" baseline water stress are rejected unless one of the following holds:

1. Treated grey water or seawater is available, with desalination accounted for.
2. Closed-loop dry cooling reduces the cooling-water term to less than 30 percent of the totals above.

## Land use

The inland 2 MW district pairs with 8 MWp of solar at typical packing density of 0.5 ha/MWp, giving about 4 ha of PV. Add 0.5 ha for the electrolyzer, fuel-cell, and storage compound. Total footprint is about 5 ha. River-adjacent and coastal variants need less PV land but add water-side civil footprint.

## Critical minerals impact

Per Chapter 02:

- Inland scenario PEM electrolyzer (3 MW) iridium loading: about 1.5 kg Ir total.
- Stationary fuel cell (1.5 MW) Pt loading: about 0.3 kg Pt total.
- Truck stack (100 kW) Pt loading: about 20 g Pt per vehicle.

Global iridium production is 7 to 8 t per year [USGS-MCS-2025]. The inland district consumes about 0.02 percent of annual global iridium. Material is recoverable at end of life. Stacks return to the OEM for PGM recovery as a contractual condition (see the decommissioning section in Chapter 08).

## Comparison vs incumbents

| Metric | This project (inland, US, 45V) | Diesel HD trucking baseline | Grid-electric district baseline |
|---|---|---|---|
| Lifecycle CO2e per delivered MWh | ~30 kg | ~280 kg (diesel-electric grid avg) | ~250 kg (US grid avg) |
| H2 GWP from leakage at 1% | ~12 kg CO2e/kg H2 leaked | n/a | n/a |
| Water draw / MWh delivered | ~0.5 m3 | ~0.0 (combustion) | ~1.5 m3 (thermal generation cooling) |
| PGM exposure | iridium, platinum | none | none direct |
| NOx / PM at point of use | zero | high | grid-mix dependent |

These numbers are illustrative. The model emits scenario-specific lifecycle vectors as part of the deployment phase.

## Theory of Change

The intervention is a paired demonstrator: a hydrogen-anchored district at multi-MW scale and a fuel-cell heavy-duty truck on a representative duty cycle. The chain from this intervention to climate, health, and industrial outcomes is mapped below with measurable indicators at each stage.

**Short-term outcomes (months 12 to 24).** Direct outputs of the build and the bench campaign. Indicators: measured stack durability hours; measured H2 leakage rate as a fraction of throughput; commissioned district capacity in MW; published `tech_params.yaml` reflecting field-measured values; first peer-reviewed paper submitted. These are observable inside the grant period.

**Medium-term outcomes (years 2 to 5 after commissioning).** Diffusion of the demonstrator's evidence into adjacent decisions. Indicators: number of follow-on districts citing this project's published TCO and LCOE; number of insurance brokers willing to underwrite similar projects on terms benchmarked to this one; number of public procurements that adopt the project's safety-case template; cumulative tonnes of H2 delivered across the demonstrator and its replicas; cumulative diesel km displaced by trucks built to the validated spec.

**Long-term outcomes (years 5 to 15).** System-level effects on emissions, health, and industrial capacity. Indicators: avoided lifecycle CO2e attributable to the demonstrator family, measured against a counter-factual of grid plus diesel; reduction in NOx and PM exposure in served corridors, validated by air-quality monitoring where available; growth in domestic stack-manufacturing employment in the deployment region; iridium and platinum recovery rate from end-of-life stacks. The chain from intervention to long-term indicator runs through replication and policy uptake. The project does not claim direct attribution beyond the demonstrator footprint.

The theory is falsifiable. If short-term indicators miss their gates, the project reports the miss and revises the design. If medium-term replication does not occur, the open-science release still informs the next project's parameters, and that is recorded as a partial outcome rather than a success.

## GDPR and data protection (EU deployments)

EU deployments collect operational telemetry from the district, the storage assets, and the truck. Some of that data is non-personal (pressure, temperature, mass flow). Some can become personal under the GDPR when it is linked to driver identity, route patterns, or site-staff behaviour. The project treats the data plan as a compliance artefact, not a marketing line.

Three commitments apply.

First, a Data Protection Impact Assessment (DPIA) is produced before any EU site goes live. The DPIA names the controller, the processors, the legal basis (Article 6(1)(f) legitimate interests for safety-critical telemetry; explicit consent for any driver-linked data), and the retention schedule.

Second, telemetry that is published as part of the open-science deliverable is anonymised at source. Driver identifiers, GPS traces below corridor-level resolution, and shift patterns are stripped before public release. Aggregation thresholds are documented in the data dictionary.

Third, the project supports data-subject rights end to end. Access, rectification, and erasure requests are routed to a named Data Protection Officer who is contracted before commissioning. Cross-border transfers, if any, use Standard Contractual Clauses and the corresponding transfer-impact assessment. Where the German BDSG or similar national overlays apply, the project complies with the stricter rule.

The same controls apply, on a best-effort basis, to non-EU deployments where the host jurisdiction has equivalent rules (UK GDPR, California CPRA, Quebec Law 25). The project does not assume that compliance designed for the EU is sufficient elsewhere.
