# 05 - Economics: LCOE, LCOH, TCO

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

All numbers in this chapter are produced by `electicity_model` and regenerated end-to-end by `python -m electicity_model.cli render-all`. See `report/_generated_tables.md` for the live tables tied to the current `tech_params.yaml` hash.

## Modelling assumptions and limitations

*Scenario output, not a forecast. Indicative numbers; replace at submission. See DISCLAIMER.md.*

- The model is deterministic and produces scenario outputs from disclosed inputs in tech_params.yaml.
- Numbers are not forecasts. They reflect public-source parameters as of 2026-05-05 and assumptions documented in this report.
- Real deployments require site-specific engineering, permitting, financial advisory, legal advisory, and insurance review.
- Reuse of these numbers in any document that solicits investment must be paired with appropriate disclaimers and review.

## Method

LCOE, LCOH, and LCOS use the standard IEA / IRENA discounted cash-flow form:

```
LCOE = sum_t [(CapEx_t + OpEx_t + Fuel_t) / (1+r)^t]
       /  sum_t [E_t / (1+r)^t]
```

Project headline numbers use a private-equity discount of 9 percent. That keeps comparisons fair against commercial benchmarks. Grant-only counter-factuals use a 5 percent public-money discount and are flagged when shown.

## District LCOE / LCOH

See the generated table in `_generated_tables.md`. Validation gate V5 (chapter intro Validation table) requires the inland scenario LCOE in the 180 to 300 USD/MWh band. The model returns 214 USD/MWh, which passes.

## Truck TCO

Validation gate V4 checks the FCEV fuel-cost-per-mile band against the H2 price. Headline TCO numbers include capex, fuel, maintenance, insurance, and residual value. Discount rate is 8 percent. Lifetime is 10 years.

## Sensitivity: what kills the case, what saves it

The tornado chart `deck/assets/tornado_lcoh_unsubsidised.png` ranks LCOH drivers without subsidies. The top three are:

1. **Capacity factor of the electrolyzer.** Below 30 percent, LCOH exceeds 7 USD/kg. Above 60 percent, it drops to 3.50 USD/kg. The implication is structural: dedicated PV plus a grid PPA for low-price hours matters more than cheap stack capex.
2. **Electricity price.** Each 10 USD/MWh swing moves LCOH by about 0.50 USD/kg.
3. **Electrolyzer capex.** A move from 2400 USD/kW to 800 USD/kW shifts LCOH by 1.60 USD/kg over project life.

Adding the IRA section 45V Tier 1 credit at 3 USD/kg flips the ranking. Capacity factor still dominates. Electricity price moves to position three because the credit dilutes its share of LCOH. See `deck/assets/tornado_lcoh_45v.png`.

## Monte Carlo NPV (district inland, US)

The model uses triangular and Gaussian sampling over annual revenue (PV plus delivered electricity) and opex, with 5,000 runs at the central case. Reproduced by:

```python
from electicity_model.sensitivity import monte_carlo_npv
monte_carlo_npv(
    capex=27_000_000,
    annual_revenue_mean=5_500_000,
    annual_revenue_std=600_000,
    annual_opex_mean=1_300_000,
    annual_opex_std=200_000,
    discount_rate=0.09,
    lifetime_years=25,
)
```

Outputs cover P5, P50, and P95 NPV and the probability of negative NPV. The headline target is **P(NPV < 0) <= 15 percent** at the chosen risk-adjusted discount rate. If the distribution exceeds that, the architecture is rejected pending a tariff or scale revision.

## Investor vs grant discount comparison

The choice of discount rate changes the headline number more than any single capex line item. At 9 percent (private equity), the inland district returns 214 USD/MWh. At 5 percent (grant-only public money), the same configuration returns roughly 160 USD/MWh, about 25 percent lower. Neither figure is wrong. They answer different questions.

A grant reviewer cares whether the project delivers public benefit per public dollar at a sovereign cost of capital. A private investor cares whether the project beats a hurdle rate that includes equity premium and project-finance risk. We quote both because mixing them is the single most common error in hydrogen project pitches. The same plant that looks marginal at 9 percent can look attractive at 5 percent, and vice versa once tax-credit timing is layered in.

## Comparison vs grant-only LCOE

For audiences that want public-money LCOE (5 percent discount, no equity premium), the same tables run with `--discount-rate 0.05` produce LCOE about 25 percent lower across all scenarios. The report quotes both figures to keep both audiences honest. Grant reviewers see public-money LCOE. Investors see private-equity LCOE.

## Limitations

The economic model is deliberately compact. Three simplifications matter and should be named.

First, there is no stochastic dispatch. The model uses annual energy balances and average capacity factors. It does not optimize hour-by-hour scheduling against price curves or simulate ancillary-service revenue. A production-grade dispatch model would refine LCOH by a few percent and could shift the rank of electricity-price sensitivity.

Second, there is no detailed grid simulation. Interconnection costs are taken as a single line item from the engineering estimate. Curtailment is approximated by capacity factor. A nodal power-flow study at the chosen host site is required before financial close.

Third, there is no explicit construction profile. Capex flows in as a single Year 0 outlay rather than an S-curve over months 6 to 24. This understates interest during construction by an amount that depends on financing structure, on the order of 2 to 4 percent of capex for a 24-month build. The financial-close model will replace this with a calendarized draw schedule.

These simplifications are appropriate at the feasibility stage. They are not appropriate for bankability documents.
