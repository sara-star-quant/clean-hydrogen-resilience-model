# References

**Last reviewed:** 2026-05-05. Vintages bumped from Phase-1 (2023/2024) to latest available
(2025/2026) where a newer publication exists. Older keys retained for traceability where
quantitative claims still resolve to those editions.

Citation keys are referenced from the report chapters as `[Citation-Key]` and from
`model/data/tech_params.yaml` via the `source:` field. Every quantitative claim in this
project must resolve to one of these or an equivalent peer-reviewed / government source
added below.

## Hydrogen - global benchmarks

- **[IEA-GHR-2025]** International Energy Agency. *Global Hydrogen Review 2025*. Paris,
  September 2025. Primary annual benchmark for the post-2026 build phase.
- **[IEA-GHR-2024]** International Energy Agency. *Global Hydrogen Review 2024*. Paris.
  Retained for time-series comparisons.
- **[IEA-GHR-2023]** International Energy Agency. *Global Hydrogen Review 2023*. Paris.
- **[IRENA-GH2-2020]** International Renewable Energy Agency. *Green Hydrogen Cost
  Reduction: Scaling Up Electrolysers to Meet the 1.5  degC Climate Goal*. Abu Dhabi, 2020.
- **[IRENA-Geopolitics-2022]** International Renewable Energy Agency. *Geopolitics of the
  Energy Transformation: The Hydrogen Factor*. Abu Dhabi, 2022. Supply-chain context.
- **[BNEF-H2-Outlook]** BloombergNEF. *Hydrogen Economy Outlook* (annual). Public
  executive summaries.

## Renewables and storage - cost benchmarks

- **[IRENA-RPGC-2024]** International Renewable Energy Agency. *Renewable Power Generation
  Costs in 2024*. Abu Dhabi, 2025. Current LCOE anchor.
- **[IRENA-RPGC-2023]** Retained for older comparisons.
- **[NREL-ATB-2025]** National Renewable Energy Laboratory. *Annual Technology Baseline
  2025*. Golden, CO. Current capex/opex anchor (incl. SMR, EGS, LFP/Na-ion, biomass-CHP).
- **[NREL-ATB-2024]** Retained for time-series.
- **[IEA-NZE-2023]** International Energy Agency. *Net Zero Roadmap: A Global Pathway to
  Keep the 1.5  degC Goal in Reach (2023 update)*. Paris.
- **[IEA-Storage-2024]** International Energy Agency. *Batteries and Secure Energy
  Transitions* / energy storage outlook chapters.

## US policy and programmes

- **[DOE-H2Shot]** US Department of Energy. *Hydrogen Shot* targets and roadmap (DOE EERE
  HFTO).
- **[DOE-H2atScale]** US Department of Energy. *H2@Scale* technical reports.
- **[DOE-HD-FCEV]** US DOE EERE. Heavy-duty FCEV TCO and demonstration reports; NACFE *Run
  on Less* heavy-duty datasets.
- **[IRA-45V]** US Internal Revenue Code section 45V (Inflation Reduction Act 2022) and Treasury
  / IRS final rule on the Clean Hydrogen Production Credit (January 2025), including the
  three-pillar requirements (additionality, hourly temporal matching phase-in, geographic
  deliverability).
- **[FERC-Order-2023]** Federal Energy Regulatory Commission Order No. 2023 (2023) on
  generator interconnection reform. Used for US interconnection-queue assumptions.

## EU policy and programmes

- **[EC-H2-Strategy]** European Commission. *A Hydrogen Strategy for a Climate-Neutral
  Europe*, COM(2020) 301 final.
- **[EC-REPowerEU]** European Commission. *REPowerEU Plan*, COM(2022) 230 final.
- **[EU-RFNBO-1184]** Commission Delegated Regulation (EU) 2023/1184 of 10 February 2023
  (additionality, temporal correlation, geographic correlation for RFNBO hydrogen).
- **[EU-RFNBO-1185]** Commission Delegated Regulation (EU) 2023/1185 of 10 February 2023
  (GHG methodology for RFNBO and recycled-carbon fuels).
- **[ENTSO-E-TYNDP]** ENTSO-E *Ten-Year Network Development Plan* (most recent). Used for
  EU interconnection assumptions.

## Australia / New Zealand

- **[ARENA-H2]** Australian Renewable Energy Agency. *Australia's Pathway to $2/kg* and
  the *Hydrogen Headstart* program documents. ARENA, Canberra.
- **[AEMO-ISP-2024]** Australian Energy Market Operator. *Integrated System Plan 2024*.
- **[MBIE-NZ-H2-2023]** New Zealand Ministry of Business, Innovation and Employment. *New
  Zealand Hydrogen Roadmap*, 2023.
- **[NZ-ERP2]** New Zealand Government. *Emissions Reduction Plan 2*.

## Climate-science basis (used for LCA chapter 06)

- **[IPCC-AR6-WG1]** IPCC, 2021. *Climate Change 2021: The Physical Science Basis*.
  Cambridge University Press. Used for radiative-forcing baselines.
- **[Sand-2023]** Sand, M. et al. "A multi-model assessment of the Global Warming
  Potential of hydrogen." *Communications Earth & Environment* 4, 203 (2023).
  doi:10.1038/s43247-023-00857-8. Hydrogen GWP100 approx  11.6 +/- 2.8.

## Materials and water

- **[USGS-MCS-2026]** US Geological Survey. *Mineral Commodity Summaries 2026*. Reston, VA,
  January 2026. Current source for platinum, iridium, lithium, nickel, cobalt, copper,
  silicon, gallium, rare-earth supply concentrations.
- **[USGS-MCS-2025]** Retained for time-series.
- **[IEA-CMO-2025]** International Energy Agency. *Critical Minerals Outlook 2025*. Paris.
  Concentration, refining, and demand-projection figures used in chapter 10.
- **[WRI-Aqueduct-4]** World Resources Institute. *Aqueduct 4.0 Water Risk Atlas*.
  Site-screening water-stress baselines.

## Codes and standards (referenced in safety section)

- **[NFPA-2]** National Fire Protection Association. *NFPA 2: Hydrogen Technologies Code*
  (most recent edition).
- **[ATEX-2014-34]** Directive 2014/34/EU on equipment for use in potentially explosive
  atmospheres.
- **[AS-4564]** AS 4564:2020 *General purpose natural gas* (Australia/NZ - referenced for
  comparable gaseous-fuel safety baseline).
- **[AS-NZS-1596]** AS/NZS 1596 *The storage and handling of LP Gas* - comparable storage-
  and-handling code referenced for gaseous-fuel siting analogues.

## Fringe-technology appendix anchor

- **[Berlinguette-2019]** Berlinguette, C. P. et al. "Revisiting the cold case of cold
  fusion." *Nature* 570, 45-51 (2019). doi:10.1038/s41586-019-1256-6. Multi-laboratory,
  multi-year, well-funded null result. Anchor citation for the position that LENR is not
  an investable pathway as of the date of this report.

---

**Maintenance rule.** When adding a parameter to `tech_params.yaml`, add the citation here
*first* and use the same key. CI fails if a `source:` value in the YAML does not match a
key defined above.
