# 01 - Problem & Scope

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

## The energy crisis we are addressing

Two pressures act in parallel. Decarbonisation deadlines make continued reliance on fossil liquid fuels economically irrational by 2030-2040 in most OECD jurisdictions [IEA-NZE-2023]. Electricity-grid bottlenecks delay direct-electrification pathways in heavy-duty transport and in remote or islanded districts where interconnection queues run 3-7 years [FERC-Order-2023, AEMO-ISP-2024]. The result is a window in which water-medium energy systems, using water as the working fluid that stores energy chemically as hydrogen and recovers it through fuel cells, fill the gap that batteries and direct electrification cannot reach economically today.

Three framing commitments anchor the work.

- Hydrogen is an energy carrier, not an energy source. Primary energy in every scenario here comes from renewable generation (PV, wind, micro-hydro, tidal). Claims of "free energy from water" violate thermodynamics and are not part of this project.
- Cold fusion, LENR, hydrinos, and "water-fuelled" claims are surveyed in Appendix 09 against a fixed evidence rubric. None are treated as investable. The Berlinguette et al. *Nature* 2019 multi-year null result [Berlinguette-2019] is the anchor citation.
- Battery-electric vehicles already dominate passenger-car economics [BNEF-EV-Outlook-2024, IEA-EV-Outlook-2024]. The project does not claim hydrogen passenger cars beat BEVs. The car track targets the segment where FCEVs hold a defensible niche: heavy-duty, long range, fast-refuel, back-to-base operations.

## Methods

The study combines a parametric techno-economic model (`model/`) with a structured literature review and a fixed KPI rubric defined later in this chapter. In scope: capex and opex bands for mature components, LCOE and LCOH at site-archetype resolution, TCO at vehicle-segment resolution, and a safety-case envelope sized against published codes. Deferred to follow-on programmes: site-specific civil engineering, electrochemical stack-level CFD, on-road homologation, and any active grant-portal automation. Numerical outputs are regenerated from the model and cross-referenced in [report/_generated_tables.md](_generated_tables.md).

Out of scope:

- Site-specific civil engineering and permitting (deferred until host district selected).
- Detailed CFD or electrochemical stack-level simulation (the project model is economic).
- On-road vehicle trials and homologation.
- Live grant-portal scraping or auto-submission.
- Any treatment of LENR or cold fusion as an investable path.

## Reference vehicle (car track), locked

Budget envelope: <= $1.0 M R&D, 24 months.

| Field | Value |
|---|---|
| Segment | Heavy-duty, Class 8 regional drayage truck OR 12 m city bus |
| Powertrain | Fuel-cell-electric, 80-120 kW PEMFC stack with 30-60 kWh Li-ion buffer |
| H2 storage | 30-60 kg at 350-700 bar gaseous |
| Daily duty cycle | 250-400 km, 1-2 refuels/day, back-to-base |
| Deliverable at end of programme | Bench-validated powertrain on instrumented dyno + safety case + defended TCO |
| Explicitly out of scope | Road-legal homologation, on-road trials, fuelling-station construction |

Rationale. $1 M does not buy a road-legal new HD vehicle. It buys a credible bench-level techno-economic validation that de-risks a follow-on round (typical follow-on $5-15 M for on-road demonstrators). That follow-on round is where ARENA Hydrogen Headstart, DOE H2Hubs, or Innovation Fund small-scale projects step in. Stating this up front prevents the common proposal failure of promising a road truck for $1 M and being rejected as unserious.

## Reference district (district track), locked

Budget envelope: <= $36.0 M total deployed capex, 36 months from grant award to commissioning.

| Field | Value |
|---|---|
| Continuous electrical load | 2 MW average, ~17.5 GWh/year |
| Population equivalent | ~5,000 residents, mixed residential + light commercial |
| Architecture envelope | 5-10 MWp solar PV; 2-5 MW PEM electrolyzer; 5-20 t H2 storage; 1-2 MW fuel cell; 1-2 MWh Li-ion buffer; grid interconnect |
| Annual water draw (electrolysis) | ~2,000-4,000 m^3 (process water; cooling water additional) |
| Site variants compared | (a) coastal-with-tidal; (b) river-adjacent-with-microhydro; (c) inland-solar-only |
| Deliverable at end of programme | Commissioned, instrumented, 12-month performance dataset published |

Three site variants are carried in parallel until a host community is selected. This keeps the project site-agnostic for the funding round and lets the model produce credible LCOE numbers for each.

## What "stable, reliable, low-maintenance, ecologic, economic" means here, quantified

The user's plain-English requirements are translated into testable KPIs against which every architecture is scored in Chapter 05.

| User requirement | KPI | Target |
|---|---|---|
| Stable | District availability | >= 99.5 % over 12-month measured operation |
| Reliable | Mean time between fuel-cell stack overhauls | >= 20,000 operating hours |
| Low-maintenance | Annual O&M as % of capex | <= 3.5 % |
| Economic | Levelised cost of energy delivered | Within 1.5x best alternative for the same site |
| Powerful (district) | Continuous output | 2 MW @ >= 95 % availability |
| Powerful (vehicle) | Sustained powertrain output | 80 kW continuous, 200 kW peak 30 s |
| Ecologic | Lifecycle GHG | < 0.45 kg CO2e per kg H2 (45V Tier 1 threshold) |
| Ecologic | H2 leakage budget | < 1 % of value-chain throughput |
| Ecologic | Water draw vs local renewal | < 0.1 % of basin annual renewal |

Any architecture that fails one of these KPIs is reported in the comparison. A solution that wins on cost but fails availability is not the recommended solution.

## Out of scope (deferred to follow-on programmes)

- Site-specific civil engineering and permitting (deferred until host district selected).
- Detailed CFD or electrochemical stack-level simulation (the project model is economic).
- On-road vehicle trials and homologation.
- Live grant-portal scraping or auto-submission.
- Any treatment of LENR or cold fusion as an investable path.
