# 00. Executive summary

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

<!-- model v0.1.0 @ no-git | params 214a7b5cb0b0 -->

## The problem

Heavy transport and dispatchable district energy remain undecarbonized at cost. Diesel still wins on $/km for long-haul Class 8 trucks. Renewable electricity alone cannot firm a 2 MW district load without storage or a fuel [IEA-WEO-2024]. The gap is a carrier and conversion problem, not a primary-energy problem.

## The two-track ask

The proposal funds two grounded tracks.

1. **Class 8 FCEV bench-validation.** Under **$1M** over 24 months. Fuel-cell stack characterization, drive-cycle dynamometer testing, and TCO validation against BEV and diesel baselines.
2. **2 MW district hybrid microgrid.** Under **$36M** over 36 months. Renewable primary (solar, micro-hydro, tidal), PEM electrolysis, H2 storage, and fuel-cell firming, instrumented for open-data publication.

## Why "from water"

The pathway is renewable electricity -> PEM electrolysis -> H2 storage -> fuel-cell reconversion (or direct use in the FCEV). Water is the carrier, not the source. The chemistry is industrially mature [IRENA-H2-2022]. LENR claims are surveyed in chapter 09 and rated not investable per [Berlinguette-2019]. They are excluded from the budget.

## Headline numbers

From [report/_generated_tables.md](_generated_tables.md) (model v0.1.0, params hash `214a7b5cb0b0`).

| Metric | Value | Source |
|---|---|---|
| Inland district capex | $27.0M (fits $36M envelope) | see model output, `district_solar_h2_inland` |
| Inland district LCOE | $214/MWh | see model output |
| Inland district LCOH | $1.90/kg (with 45V PTC) | see model output |
| Class 8 FCEV TCO @ $4/kg H2 | $0.907/km | see model output, `car_fcev_class8` |
| Class 8 FCEV TCO @ $6/kg H2 | $1.082/km | see model output |
| Class 8 FCEV TCO @ $9/kg H2 | $1.343/km | see model output |
| Class 8 BEV TCO (reference) | $0.712/km | see model output, `car_bev_class8_ref` |
| Class 8 diesel TCO (reference) | $0.781/km | see model output, `car_diesel_class8_ref` |

## Honest positioning

BEV beats FCEV on $/km for Class 8 at our reference parameters, and decisively so for passenger vehicles [IEA-GlobalEV-2024]. The defensible niche for FCEV is heavy-duty long-haul and back-to-base fleets where battery mass, charge time, and depot peak-power constraints invert the comparison [ICCT-HDV-2023]. The proposal does not pitch a general "hydrogen economy". It pitches the specific corridor where the chemistry pays. LENR is reported as a literature survey and is rated not investable per the calorimetry-and-reproducibility critique in [Berlinguette-2019].

## Risk and mitigation (summary)

- **H2 price volatility.** Sensitivity reported across $4/$6/$9/kg bands. Offtake structured against the 45V PTC floor [IRA-45V-2023].
- **Electrolyzer capex slippage.** Capex is benchmarked against IRENA tracking. The model exposes the parameter for live re-pricing [IRENA-H2-2022].
- **Niche-bound demand.** Bench-validation is scoped to the heavy-duty niche. Deployment is staged behind validation gates, not committed up front.

## Ask split

- **Grant-first.** Target instruments: Horizon Europe Cluster 5, DOE OCED, ARENA, EECA, EU Innovation Fund. See `grants/` for instrument-specific narratives.
- **Equity.** Placeholder, post-grant matching. Private climate-tech investors, sized to fill the residual after grant award and structured to preserve open-data commitments.

## Pointers

- Full technical detail: [report/01_problem_and_scope.md](01_problem_and_scope.md) through `report/08_*.md`.
- Not-investable survey: [report/09_appendix_fringe_tech.md](09_appendix_fringe_tech.md).
- VC pitch: [deck/pitch.md](../deck/pitch.md).
- Grant-specific narratives: `grants/*.md`.
- Bibliography: [report/references.md](references.md).

## Limitations and uncertainties

The largest unknown is the delivered price of green H2 over the 2027-2032 window. Modeled values track 45V eligibility under current US Treasury guidance, and a regulatory reversal would shift the inland LCOH band by $2-4/kg. Tidal stream remains pre-commercial at TRL 6-7, so the coastal variant carries a cost-overrun risk that the model cannot bound from public data. Stack durability projections rely on accelerated stress tests that have not yet been correlated against 20,000-hour HD road operation at scale. Site selection is unresolved, which leaves water-stress and interconnection assumptions parametric rather than committed.
