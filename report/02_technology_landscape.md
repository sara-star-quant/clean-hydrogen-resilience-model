# 02 - Technology Landscape

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

The seven technologies carried through this project. Each has a TRL rating, a cost basis, and a named role in the car track, the district track, or both. Rated TRL is the level demonstrated at MW-scale or vehicle-deployed-fleet. Laboratory TRL is generally higher.

| ID | Technology | TRL (deployed) | TRL source | Role | Cost basis |
|---|---|---|---|---|---|
| T1 | PEM water electrolysis (renewable-powered) | 8-9 | [IEA-GHR-2024, fig. 3.4] | District: H2 production | [IEA-GHR-2024] |
| T1b | Alkaline electrolysis | 9 | [IEA-GHR-2024, fig. 3.4] | District: lower-cost H2 alternative | [IEA-GHR-2024] |
| T1c | SOEC (solid oxide electrolysis) | 6-7 | [IEA-GHR-2024, fig. 3.4] | District: high-efficiency variant where waste heat is available | [IEA-GHR-2024] |
| T2 | PEM fuel cell, heavy-duty vehicle | 7-8 | [DOE-HD-FCEV, sec. 2] | Car: powertrain | [DOE-HD-FCEV] |
| T3 | PEM / SOFC fuel cell, stationary | 7-8 | [DOE-H2atScale, ch. 4] | District: dispatchable power | [DOE-H2atScale] |
| T4 | Micro-hydro / run-of-river | 9 | [IRENA-RPGC-2023, p. 78] | District: primary generation when flow exists | [IRENA-RPGC-2023] |
| T5 | Pumped hydro storage | 9 | [NREL-ATB-2024, hydropower row] | District: long-duration storage | [NREL-ATB-2024] |
| T6 | Tidal stream | 6-7 | [IRENA-RPGC-2023, p. 142] | District: coastal variant | [IRENA-RPGC-2023] |
| T7 | Solar-PV + electrolyzer + H2 + FC hybrid | 8 (system-level) | [IEA-GHR-2024, ch. 5; NREL-ATB-2024 integrated cases] | District reference architecture | [IEA-GHR-2024, NREL-ATB-2024] |

## Why these and not others

- **Direct combustion of hydrogen in ICEs.** Excluded for vehicles. NOx emissions are non-trivial and efficiency is ~30 % vs ~50 % for fuel cells [DOE-HD-FCEV]. Excluded for district for the same efficiency penalty.
- **Hydrogen carriers (ammonia, LOHC, methanol).** Out of scope for a <= $36 M district deployment. Carrier conversion adds capex and round-trip losses, and only pays off at inter-regional shipping scales.
- **Underground hydrogen storage (salt caverns, depleted reservoirs).** Geographically bounded. Revisit when a host district is selected. Above-ground compressed storage modelled here is a defensible default for a 2 MW district scale.
- **Cold fusion, LENR, hydrinos, "water-as-fuel".** See chapter 09. Not investable.

## TRL bar, visual cue for funders

```
   3    4    5    6    7    8    9
   |----|----|----|----|----|----|
T1                              ##  PEM electrolyzer (deployed MW-scale)
T1b                              # Alkaline (mature)
T1c                       ##       SOEC (early commercial)
T2                          ##     HD FCEV (small fleets in service)
T3                          ##     Stationary FC MW-class
T4                              #  Micro-hydro (mature)
T5                              #  Pumped hydro (mature)
T6                       ##        Tidal (pre-commercial)
T7                         ##      Hybrid system integration
```

## Vendor and integrator landscape (illustrative, no endorsement)

The proposal does not pre-commit to any vendor. The integrator team is selected through competitive procurement at the start of the deployment phase. Public benchmarks the project will compare bids against:

- Electrolyzers: Nel, ITM Power, Plug Power, Cummins (Accelera), Siemens Energy, Thyssenkrupp nucera, Sunfire (SOEC), Topsoe (SOEC).
- Fuel cells (vehicular): Ballard, Cummins, Toyota, Hyundai HTWO, PowerCell.
- Stationary fuel cells: Bloom Energy, FuelCell Energy, AFC Energy, PowerCell.
- Micro-hydro / hydro: Andritz, Voith, Gilkes, Mavel.
- Tidal: SAE (Atlantis), Orbital Marine, Verdant.

These names scope realistic capex and opex bands. They are not endorsements of any single vendor.

## Decision criteria carried into chapters 03 and 04

Every architecture comparison scores against the KPIs locked in chapter 01: availability, stack overhaul interval, O&M as % of capex, LCOE / TCO, lifecycle GHG, H2 leakage, water draw vs basin renewal. Architectures that fail any KPI are reported even if they win on cost.
