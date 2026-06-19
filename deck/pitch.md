---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Water-Medium Energy, confidential'
footer: 'electicity-project, grounded technologies only'
---

# Water-Medium Energy: Heavy-Duty FCEV + 2 MW District Hybrid

> **Disclaimer.** This is a research and modelling project, not financial, legal, engineering, or tax advice, and not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

Bench truck under $1M, district under $36M, grounded technology only.

---

## The energy crisis, in one frame

- Industrial $/kWh dispersion has widened 3-5x across OECD since 2021; heavy-duty diesel sits exposed to both crude and carbon-price volatility.
- Heavy-duty road freight accounts for about 6% of global CO2 and is hard to abate without high-energy-density fuels.
- Grid emissions bend only where firm renewables and storage replace gas peakers.
- Capital is available for projects with bankable LCOE and defensible LCOH. The gap is execution-grade evidence at MW scale.

---

## Honest framing: what "energy from water" means here

- Water is the **medium**, not the source. Primary energy is renewable electricity (solar / micro-hydro / tidal).
- Stack: electricity to electrolysis to H2 to fuel cell to motive or grid power.
- This is not cold fusion, not LENR, not "water as fuel". Round-trip efficiency is bounded by thermodynamics (about 30-45% power-to-power).
- The value proposition is dispatchability, heavy-duty range, and zero tailpipe, not free energy.

---

## Two tracks at a glance

| Track | Budget cap | Deliverable | Horizon |
|---|---|---|---|
| Car (T2 PEMFC) | < $1M | Bench-validated Class 8 FCEV powertrain + safety case + TCO | 18 months |
| District (T1 + T3 + T4/T6) | < $36M | 2 MW hybrid microgrid, 12-month measurement campaign | 36 months |

Grant-first. Equity bridges between gates.

---

## Tech shortlist and TRL

```
T1 PEM electrolysis     [#########.] TRL 9
T2 PEMFC vehicle stack  [########..] TRL 8
T3 Stationary FC / SOFC [########..] TRL 8
T4 Micro-hydro          [#########.] TRL 9
T5 PHES (small)         [########..] TRL 8
T6 Tidal stream         [######....] TRL 6-7
T7 Hybrid integration   [#######...] TRL 7
```

All seven are commercially deployable or near-deployable. No speculative chemistry.

---

## Car track: Class 8 FCEV bench

- Budget: under $1M. Deliverable: bench-validated FCEV powertrain, safety case, defended TCO.
- Honest positioning: BEVs win passenger and short-haul. The FCEV niche is long-haul, back-to-base, high-duty-cycle Class 8.
- Reference TCO at $6/kg H2: **$1.082/km** vs diesel **$0.781/km** vs BEV **$0.712/km**.

| Phase | Spend cap | Exit gate |
|---|---|---|
| Procure stack + BoP | $0.45M | Stack acceptance test |
| Bench integration | $0.25M | Closed-loop control |
| Duty-cycle runs | $0.20M | 500h endurance |
| Safety case + TCO | $0.10M | HSE sign-off |

---

## District track: 3 site variants

| Variant | Primary | Storage | Notes |
|---|---|---|---|
| Inland (default) | Solar PV | PEM electrolysis + H2 + FC | Lowest siting risk |
| River-adjacent | Micro-hydro | Battery + small H2 | Best LCOE if hydrology |
| Coastal | Tidal stream | H2 + FC | Highest TRL risk |

```
[PV / hydro / tidal] -> [DC bus] -> [PEM electrolyser] -> [H2 storage]
                              \                              |
                               -> [battery / inverter]       v
                                              [stationary FC / SOFC] -> [district load]
```

Recommendation: default to inland solar+H2 unless the host site provides hydrology head or tidal resource.

---

## Headline economics

District (CapEx fits $36M cap on all three):

| Scenario | CapEx | LCOE | LCOH |
|---|---|---|---|
| Solar + H2 inland | $27.0M | $214/MWh | $1.90/kg |
| Micro-hydro river | $20.3M | $160/MWh | $4.30/kg |
| Tidal coastal | $24.2M | $198/MWh | $5.22/kg |

Class 8 FCEV TCO sensitivity to H2 price:

| H2 price | TCO | Fuel cost |
|---|---|---|
| $4/kg | $0.907/km | $0.349/km |
| $6/kg | $1.082/km | $0.524/km |
| $9/kg | $1.343/km | $0.786/km |

Diesel ref $0.781/km, BEV ref $0.712/km.

---

## Sensitivity: what moves LCOH

![tornado without subsidy](assets/tornado_lcoh_unsubsidised.png)

![tornado with 45V](assets/tornado_lcoh_45v.png)

- **Top driver: electricity price.** It dominates both subsidised and unsubsidised cases.
- **Second: electrolyser capacity factor.** Below 35% CF, LCOH degrades sharply.
- **Third: stack capex and efficiency.** The 45V Tier 1 credit reorders rank, capex matters less when the production tax credit is secured.

---

## Environmental envelope

- Lifecycle GHG: under 0.45 kgCO2e/kgH2 to qualify as 45V Tier 1 (vs about 10-12 for SMR).
- H2 leakage budget: under 1% across the chain. Sand et al. 2023 indirect GWP100 about 11.6; we design for measurement, not assumption.
- Water draw: under 0.1% of basin renewable yield at all three site variants. About 9 L water per kg H2 stoichiometric, 20-25 L/kg with cooling.
- No PFAS-membrane lock-in: spec hydrocarbon-membrane alternates where qualified.

---

## Roadmap: 36 months, 10 milestones

| ID | Month | Milestone |
|---|---|---|
| M1 | 0-3 | Site MoU + interconnect application |
| M2 | 3-6 | Procurement RFP closed (electrolyser, FC, BoP) |
| M3 | 6-9 | Long-lead orders placed; permits filed |
| M4 | 9-12 | Civils + electrical rough-in |
| M5 | 12-15 | Truck bench integration complete |
| M6 | 15-18 | District mechanical complete |
| M7 | 18-21 | Cold + hot commissioning |
| M8 | 21-24 | Truck 500h endurance signed off |
| M9 | 24-30 | 6-month measurement campaign |
| M10 | 30-36 | Full 12-month dataset + public report |

---

## Team and partners (placeholders)

- **PI**, technical lead, accountable for go/no-go gates.
- **HSE lead**, H2 safety case, ATEX/IECEx, leak-detection plan.
- **Systems integrator**, EPC for the district build.
- **Host community**, landholder, utility, or municipal sign-on.
- **OEM partner**, Class 8 chassis and stack supplier.
- **Insurance / surety broker**, bondability and project insurance from FID.

---

## The ask

**Grant-side (primary):**
- Horizon Europe Cluster 5 (Climate, Energy, Mobility), district + truck.
- US DOE OCED H2Hubs / EERE HFTO, truck bench + district co-funding.
- ARENA Hydrogen Headstart (AU), district production credit eligibility.
- NZ EECA GIDI (Government Investment in Decarbonising Industry), district.
- EU Innovation Fund, district at Small-Scale or Medium-Scale window.

**Equity-side (bridge):**
- $X over Y years, drawn against grant gate completions (M3, M6, M8).
- Investor downside protected by milestone-tied tranches and asset salvage value.

---

## Top 5 risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| R1 | H2 leakage exceeds 1% budget | Continuous leak detection; design for measurement; independent audit |
| R2 | Insurance / bondability gap | Engage broker pre-FID; proven OEM stack only; HSE case to ATEX/IECEx |
| R4 | Interconnect queue delay | File M1; design for islanded operation as fallback |
| R8 | Tidal underperformance | Default to inland; tidal only with 12-mo resource data |
| R6 | RFNBO / 45V compliance drift | Hourly matching from day one; additionality + geographic correlation evidenced |

---

## Why now

- **US:** IRA section 45V production tax credit up to $3/kg for clean H2; 10-year window.
- **EU:** REPowerEU 10 Mt domestic + 10 Mt import target; RFNBO Delegated Acts 2023/1184 and 2023/1185 set the rules; Innovation Fund actively allocating.
- **Australia:** Hydrogen Headstart A$2B production credit program.
- **New Zealand:** Emissions Reduction Plan 2 (ERP2) prioritises industrial decarbonisation and heavy transport.
- Combined: a 5-7 year window where capital, policy, and offtake align for execution-grade demonstrators.

---

## Appendix: due-diligence stance on fringe claims

- Appendix 09 catalogs LENR, hydrinos, "water-as-fuel" and similar claims.
- We rate these **not investable**, consistent with Berlinguette et al., *Nature* 2019 (revisiting cold fusion), and the absence of reproducible, peer-reviewed positive results since.
- We do not pretend otherwise to the reviewer or the investor. The project is grounded in commercially deployable electrolysis and fuel cell technology only.

---

## Disclaimer and forward looking statements

- This deck is a research and modelling artifact, not financial, legal, engineering, or tax advice.
- Nothing here is an offer to sell or a solicitation of an offer to buy any security or interest.
- Cost, performance, and policy figures are model outputs and citations of public sources at a point in time; they will move.
- Forward-looking statements (timelines, milestones, grant outcomes, regulatory windows) involve known and unknown risks and may differ materially from actual results.
- Readers should perform their own due diligence and consult qualified advisors before acting on any information in this document.
