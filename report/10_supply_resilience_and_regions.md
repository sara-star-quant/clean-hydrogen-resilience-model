# 10 - Supply Resilience and Regional Prioritisation

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

## 10.1 Background

Heavy-duty fuel-cell electric trucks and proton-exchange-membrane (PEM) electrolysers depend on a small set of platinum-group metals (PGMs) and lithium-ion battery materials whose primary production is concentrated in a handful of jurisdictions. The IEA *Critical Minerals Outlook 2025* reports that, for several materials core to this project, the top three producing countries account for more than 80% of mined output and a still higher share of refined output [IEA-CMO-2025]. The USGS *Mineral Commodity Summaries 2026* gives the corresponding 2024 production figures by country and confirms that those concentrations persist year on year [USGS-MCS-2026].

The Class 8 FCEV under $1M and the 2 MW district hybrid microgrid under $36M are quoted as of 2026-05-05 against business-as-usual (BAU) mineral prices. That envelope is conditional. Since 2024 the policy environment has shifted materially. Export controls on gallium and germanium remain in force. The EU Critical Raw Materials Act has entered application. The US Defense Production Act (DPA) Title III has been invoked for several battery and electrolyser inputs. The Inflation Reduction Act 45V Clean Hydrogen Production Credit final rule has been in force since January 2025 [IRA-45V][EC-REPowerEU]. The chapter therefore models supply shocks explicitly rather than carrying a single BAU LCOE forward.

The second axis of this chapter is geographic. Both project tracks can be sited in many places. The choice of site changes interconnection lead time, water availability, regulatory eligibility (in particular for 45V and for the EU Renewable Fuels of Non-Biological Origin rules), supply-chain proximity, and social-licence cost. This chapter sets out a transparent scoring rubric across six axes for the candidate regions encoded in `model/src/electicity_model/regions.py`. It separates "deployment-reliability" from "autonomy" weightings, and pairs the regional choice with a survival-stack architecture intended to remain operable under a maritime chokepoint thought experiment.

## 10.2 Methodology and limitations of region scoring

The 0-5 rubric used throughout this chapter is illustrative. Named experts have not validated the per-axis weights. The composite scores are intended to expose tradeoffs and to be auditable, not to be cited as authoritative. Readers should treat ranks within ~0.25 composite points as indistinguishable. The weights and per-axis sources in `regions.py` are the correct objects of critique; a single composite number is not. We re-state these limitations in section 10.7.

## 10.3 Hypothesis

Three falsifiable claims are tested in this chapter.

- **H1.** Substituting alkaline or anion-exchange-membrane (AEM) electrolysis for PEM keeps the 2 MW district capex within the $36M envelope under an iridium-shortage shock (`ir_shortage`, Ir loading x 5, PEM stack capex x 1.6).
- **H2.** At least one autonomy-candidate region per jurisdiction (EU, US, AU, NZ) scores >= 4.0/5 on the deploy composite and >= 4.0/5 on the autonomy composite.
- **H3.** A `maritime_blockade` shock breaks the inland-default architecture (`district_solar_h2_inland`) but the autonomy-maximised architecture survives within 1.5 x the BAU LCOE of $214/MWh ([generated tables](_generated_tables.md)).

## 10.4 Methods

### 10.4.1 Critical-minerals exposure matrix

For each material with a non-trivial role in the project, the analysis records (i) the in-project use case, (ii) the 2024 supply concentration reported by [USGS-MCS-2026] (top-1 / top-3 share of mined or refined output, whichever is more concentrated), (iii) a substitution path with TRL, and (iv) the in-project consequence if no substitution is taken.

### 10.4.2 Shock profiles

Nine declarative profiles are encoded in `model/src/electicity_model/supply.py`. Each profile is a list of `(yaml-path, multiplier)` tuples. The math contract, enforced by the test suite, is that each multiplier acts on a specific YAML line item (e.g. `pem_electrolyzer.capex_per_kw`) and never on a derived aggregate. `triple_squeeze` is therefore not the product of `ir_shortage` x `pt_shortage` x `li_shortage` rolled up onto a common base; it is the union of their line-item multipliers, each acting on its own line.

| Profile | Multipliers (selected) | Intent |
|---|---|---|
| `bau` | identity | Baseline. Bit-for-bit identity. |
| `ir_shortage` | PEM Ir loading x 5; PEM stack capex x 1.6 | Single-material PGM shock. |
| `pt_shortage` | Stationary FC Pt loading x 3; FC stack capex x 1.25; vehicle FC capex x 1.25 | Single-material PGM shock. |
| `li_shortage` | Grid Li-ion capex x 2.5 | Single-material battery shock. |
| `china_decoupling` | PV capex x 1.30; Li-ion capex x 1.20; LFP capex x 1.20; electrolyser opex x 1.10 | Multi-line moderate shock. |
| `triple_squeeze` | Union of `ir_shortage`, `pt_shortage`, `li_shortage` | Compound shock, line-by-line. |
| `western_only` | PV / electrolyser / FC / Li / LFP capex x 1.25 | Strict friend-shoring. |
| `maritime_blockade` | PV x 1.50; PEM x 2.20; FC x 2.00; Li-ion x 3.50; LFP x 1.80; Na-ion x 1.30 (and others) | Tail-risk thought experiment. |
| `regional_autarky` | PEM x 1.50; FC x 1.40; Li-ion x 1.30; PV x 1.15 | Forced regional self-sufficiency. |

### 10.4.3 Region scoring rubric

Six axes are scored 0-5 per region, with sources cited per axis per region in `regions.py`.

| Axis | Definition |
|---|---|
| RES | Renewable-resource quality (irradiance, hydro CF, tidal stream, geothermal). |
| INT | Interconnection lead time and queue depth. |
| WAT | Water availability per [WRI-Aqueduct-4]. |
| REG | Regulatory eligibility (45V, RFNBO 2023/1184, ARENA, MBIE) and clarity. |
| SUP | In-jurisdiction or jurisdiction-aligned supply-chain depth. |
| SOC | Social-licence framework maturity (e.g. tribal, iwi, Sami, Native Title). |

Two composite scores are formed.

| Composite | RES | INT | WAT | REG | SUP | SOC |
|---|---|---|---|---|---|---|
| `deploy` (deployment reliability) | 0.25 | 0.20 | 0.15 | 0.15 | 0.10 | 0.15 |
| `autonomy` (autarky-resilient)    | 0.20 | 0.05 | 0.15 | 0.20 | 0.30 | 0.10 |

The `autonomy` weighting penalises sites that depend on long interconnection queues to deliver value, and rewards supply-chain depth and regulatory clarity.

## 10.5 Results

### 10.5.1 Critical-minerals exposure matrix

| Material | In-project use | Concentration (2024) | Substitution path | TRL of substitute |
|---|---|---|---|---|
| Iridium (Ir) | PEM electrolyser anode | South Africa ~85% of mined PGM-Ir [USGS-MCS-2026] | Alkaline electrolyser (no PGM); AEM (low-PGM) | Alkaline 9; AEM 6-7 [IEA-GHR-2025] |
| Platinum (Pt) | PEM fuel cell (vehicle + stationary) | South Africa ~70% mined; refining concentrated [USGS-MCS-2026] | Pt-loading reduction; recycled-Pt loop; SOFC (no Pt) for stationary | Pt-reduction 8; SOFC stationary 8 [IEA-GHR-2025] |
| Lithium (Li) | Li-ion grid battery; Li-ion in BEV reference | Australia + Chile + China ~90% mined; China dominates refining [IEA-CMO-2025] | LFP (still Li but no Ni/Co); Na-ion | LFP 9; Na-ion grid 7 [NREL-ATB-2025] |
| Nickel (Ni) | NMC cells (excluded from base case); some FC BoP | Indonesia + Philippines + Russia ~65% [USGS-MCS-2026] | LFP / Na-ion route avoids Ni entirely | LFP 9; Na-ion 7 |
| Cobalt (Co) | NMC cells (excluded from base case) | DRC ~70%; refining China-dominant [IEA-CMO-2025] | LFP / Na-ion | 9 / 7 |
| Copper (Cu) | Conductors, transformers, BoS | Chile + Peru + DRC ~50% [USGS-MCS-2026] | Aluminium for some BoS; recycling | Al-conductor 9 (well established) |
| Silicon / polysilicon (Si) | Crystalline-Si PV | China ~80% polysilicon refining [IEA-CMO-2025] | EU/US polysilicon expansion; thin-film CdTe | c-Si 9; CdTe 9 (limited supply) |
| Gallium (Ga) | Power electronics (GaN inverters) | China ~95% low-purity Ga [USGS-MCS-2026] | SiC / Si IGBT power electronics | SiC 9; Si IGBT 9 |
| Nd / Pr / Dy (REE) | PMSM in some BEV refs and wind | China ~60% mined, ~90% refined [IEA-CMO-2025] | Externally excited synchronous (no PM); induction motors | Non-PM 9 |

### 10.5.2 Shock x scenario LCOE delta

The baseline `district_solar_h2_inland` is $26.9M capex and $214/MWh LCOE ([generated tables](_generated_tables.md)). Shock-specific re-runs are produced by the model when the shock profile is supplied to `render-all`. The table below should be regenerated when shocks land in the published table set.

| Shock | Inland scenario LCOE | Inland scenario capex | Comment |
|---|---|---|---|
| `bau` | $214/MWh | $26.9M | Reference. |
| `ir_shortage` | <!-- regenerate via electicity render-all --> | <!-- regenerate via electicity render-all --> | Substitute alkaline to retain envelope (H1). |
| `pt_shortage` | <!-- regenerate via electicity render-all --> | <!-- regenerate via electicity render-all --> | District has no FCEV; minimal direct effect on inland LCOE. |
| `triple_squeeze` | <!-- regenerate via electicity render-all --> | <!-- regenerate via electicity render-all --> | Stresses both PEM and Li-ion lines. |
| `regional_autarky` | <!-- regenerate via electicity render-all --> | <!-- regenerate via electicity render-all --> | +30% PGM, +30% Li-ion, +15% PV. |
| `maritime_blockade` | <!-- regenerate via electicity render-all --> | <!-- regenerate via electicity render-all --> | Tail risk; expect > 1.5 x BAU on inland default; H3 to be checked vs survival-stack. |

### 10.5.3 Top regions per jurisdiction (deploy composite)

Scores are computed by composite weighting from `regions.py` and rounded to two decimals.

#### European Union / EEA

| Rank | Region | Variants | Deploy | Autonomy |
|---|---|---|---|---|
| 1 | Norwegian fjords (Finnmark / Trondelag) | river-adjacent | 4.35 | 4.50 |
| 2 | Iceland (geothermal + hydro) | river-adjacent, inland | 4.20 | 3.75 |
| 3 | Brittany / French Atlantic coast | tidal | 4.05 | 4.20 |

Axis breakdowns (RES / INT / WAT / REG / SUP / SOC):

| Region | RES | INT | WAT | REG | SUP | SOC |
|---|---|---|---|---|---|---|
| Norwegian fjords | 5 | 3 | 5 | 5 | 4 | 4 |
| Iceland | 5 | 4 | 5 | 4 | 2 | 4 |
| Brittany | 5 | 3 | 5 | 4 | 4 | 3 |

Notes. Andalucia/Aragon is the EU inland default for grid-connected deployment (deploy 3.65, autonomy 3.55) but ranks below the autonomy-leaning top-3 above on water and supply. RFNBO eligibility under [EU-REPowerEU][EC-REPowerEU] is satisfied across all four candidates.

#### United States

| Rank | Region | Variants | Deploy | Autonomy |
|---|---|---|---|---|
| 1 | Pacific Northwest (Columbia Basin WA/OR) | river-adjacent, inland | 3.95 | 3.90 |
| 2 | Iowa / South Dakota | inland | 3.90 | 3.65 |
| 3 | Texas ERCOT (West Texas / Permian) | inland | 3.70 | 3.50 |

| Region | RES | INT | WAT | REG | SUP | SOC |
|---|---|---|---|---|---|---|
| Pacific Northwest | 5 | 3 | 5 | 4 | 3 | 3 |
| Iowa / South Dakota | 4 | 4 | 5 | 3 | 3 | 4 |
| Texas ERCOT | 5 | 5 | 1 | 3 | 4 | 3 |

Notes. The Pacific Northwest is the strongest US river-adjacent pick and has a direct DPA Title III pathway. ERCOT provides the fastest interconnect [FERC-Order-2023] but at WAT = 1, requiring closed-loop or dry cooling. New Mexico (deploy 3.10) is excluded from the top-3.

#### Australia

The three encoded AU candidates are all retained.

| Rank | Region | Variants | Deploy | Autonomy |
|---|---|---|---|---|
| 1 | Tasmania (hydro + tidal) | river-adjacent, tidal, inland | 4.70 | 4.65 |
| 2 | Pilbara WA (solar + hydrogen) | inland | 3.95 | 4.00 |
| 3 | Snowy Hydro region NSW | river-adjacent | 3.80 | 3.95 |

| Region | RES | INT | WAT | REG | SUP | SOC |
|---|---|---|---|---|---|---|
| Tasmania | 5 | 4 | 5 | 5 | 4 | 5 |
| Pilbara WA | 5 | 4 | 2 | 5 | 4 | 3 |
| Snowy NSW | 4 | 3 | 4 | 4 | 4 | 4 |

Notes. Tasmania is the strongest single region in the global database on both composites and aligns with [ARENA-H2] and [AEMO-ISP-2024] priorities. Pilbara is water-stressed.

#### New Zealand

The two encoded NZ candidates are both retained.

| Rank | Region | Variants | Deploy | Autonomy |
|---|---|---|---|---|
| 1 | Otago / Canterbury South Island | river-adjacent, inland | 4.00 | 3.70 |
| 2 | Taupo / Bay of Plenty (geothermal) | inland | 3.85 | 3.55 |

| Region | RES | INT | WAT | REG | SUP | SOC |
|---|---|---|---|---|---|---|
| Otago / Canterbury | 5 | 3 | 5 | 4 | 2 | 4 |
| Taupo / BoP | 5 | 3 | 4 | 4 | 2 | 4 |

Notes. SUP = 2 reflects the limited domestic OEM presence noted in [MBIE-NZ-H2-2023]. Trans-Tasman partnership is the practical mitigation.

### 10.5.4 Architecture x jurisdiction recommendation matrix

| Architecture | EU | US | AU | NZ |
|---|---|---|---|---|
| Inland (`district_solar_h2_inland`) | Andalucia / Aragon | Iowa / SD | Pilbara (with closed-loop) | Otago / Canterbury |
| River-adjacent (`district_microhydro_river`) | Norwegian fjords | Pacific Northwest | Snowy Hydro NSW | Otago / Canterbury |
| Tidal (`district_tidal_coastal`) | Brittany | (not recommended) | Tasmania (Bass Strait) | (not recommended) |

### 10.5.5 Hypotheses re-stated against results

- **H2.** Norway (autonomy 4.50), Tasmania (4.65), and Pilbara (4.00) meet the >= 4.0 / >= 4.0 dual threshold. Pacific Northwest (3.95) and Otago / Canterbury (3.70) miss the autonomy-side threshold; the US and NZ jurisdictions therefore fail H2 on the strict formulation. EU and AU pass.
- **H1** and **H3** require shock-aware LCOE re-runs. The results panel carries placeholders to be replaced when the model emits them.

## 10.6 Autonomy-Maximised Survival Stack

### 10.6.1 Background

The commercial architecture is optimised against BAU LCOE. A separate "survival stack" architecture is specified for sites where the operator's risk tolerance assigns non-trivial probability to multi-month loss of imported critical components. In that regime the design objective shifts from least-cost-of-energy to time-to-recover-from-shock. This is not the base-case architecture; it is a documented alternative that the remainder of this section sizes and prices.

### 10.6.2 Architecture choices

| # | Choice | Rationale | Cost penalty vs commercial |
|---|---|---|---|
| 1 | Alkaline electrolyser (no PGM) instead of PEM | Removes Ir / Pt exposure; mature TRL 9 [IEA-GHR-2025] | +0-10% stack capex; lower dynamic response |
| 2 | Solid-oxide fuel cell (SOFC) for stationary backup | No PGM; high-temperature CHP; tolerant of impure H2 [NREL-ATB-2025] | +20-40% vs PEM stationary FC capex |
| 3 | LFP grid battery (no Ni / Co) | Drops Co exposure entirely; Li-only chemistry [USGS-MCS-2026] | Negligible vs 2026 NMC; better cycle life |
| 4 | Oversize PV by ~30% | Buffers against polysilicon-import disruption and degradation | +15% PV capex |
| 5 | Biomass black-start unit (<= 200 kW) | Locally fuelled cold-start path independent of imports | +3-5% aggregate capex |
| 6 | Analog PLC / hardwired safety logic for top-level interlocks | Reduces dependence on imported semiconductors for core safety [IEA-CMO-2025] | +1-2% BoS capex |
| 7 | 30-day on-site water reserve (closed-loop polishing) | Decouples from external water deliveries / chemistries | +0.5-1% aggregate capex |
| 8 | One-year strategic spares (membranes, gaskets, valves, seals) | Bridges import disruption to next ship-window | +2-3% aggregate capex |

The aggregate cost penalty is bounded above by approximately 25% versus the commercial $26.9M / $214/MWh inland baseline. The 1.5 x LCOE survival threshold in H3 therefore has headroom in BAU. H3 is meaningful only when the survival stack is itself priced under `maritime_blockade`, to be populated by `render-all`.

### 10.6.3 Failure-mode analysis (6-month grid-off)

| Subsystem | Time to first failure | Failure mode | Mitigation in stack |
|---|---|---|---|
| Water-treatment chemicals (membrane antiscalants, chlorine) | ~120 days | Fouling of polishing loop | 30-day reserve + on-site electrochlorination |
| Fuel-cell stack hours | 8000-20000 h | Degradation; replacement parts | 1-year membrane spares; SOFC redundancy |
| Biomass feedstock | Seasonal | Wet feedstock; storage moulding | Covered storage; rotating buffer >= 90 days |
| PV degradation under sustained dust / volcanic ash | Months | Soiling > 20% loss | Manual / dry-clean SOPs; oversize margin |
| Battery cells | Years | Capacity fade | LFP cycle life; cell-level redundancy |
| Power electronics | Years | Random IGBT failure | SiC / Si only; spares and modular replacement |

### 10.6.4 Cold-start sequence: black grid to 1 MW operational in < 6 h

1. **t = 0 min.** Trigger biomass black-start unit (manual). Closed manual disconnects isolate the site from the dead grid.
2. **t = 0-30 min.** Biomass unit reaches ~150 kW; energises the analog PLC bus, the SOFC pre-heater, and battery management.
3. **t = 30-90 min.** SOFC reaches operating temperature on stored H2. Battery is brought online; 250 kW available on the DC bus.
4. **t = 90-180 min.** PV array is re-synchronised at first daylight; dust is cleared per SOP; ramp to ~600 kW PV-AC if irradiance >= 600 W/m^2.
5. **t = 180-300 min.** Alkaline electrolyser warm-starts at 30% load on surplus PV; the H2 buffer begins re-fill.
6. **t = 300-360 min.** Site at 1 MW dispatchable through PV+battery+SOFC triad with electrolyser following PV.

The sequence assumes a daylight start and a pre-loaded H2 buffer >= 200 kg. Night or empty-buffer cold-starts extend to ~12 h on biomass and battery alone.

### 10.6.5 Funding alignment

| Jurisdiction | Programme | Element of stack supported |
|---|---|---|
| US | DPA Title III invocations on PGMs / batteries | Alkaline electrolyser; LFP; SOFC |
| US | 45V Clean Hydrogen Production Credit [IRA-45V] | Alkaline electrolyser; PV oversize |
| EU | CRMA Strategic Projects | Spares pool; supply-chain qualification |
| EU | REPowerEU [EC-REPowerEU] | PV oversize; alkaline electrolyser |
| AU | Hydrogen Headstart [ARENA-H2]; ISP 2024 [AEMO-ISP-2024] | Tasmania / Pilbara stack co-funding |
| NZ | South Island grid-resilience funding under [NZ-ERP2]; [MBIE-NZ-H2-2023] | Otago / Canterbury stack co-funding |

## 10.7 Discussion

The exposure matrix and shock profiles together imply that the dominant single-material risks for this project are iridium (PEM) and lithium (grid battery). Both have mature substitutions: alkaline electrolysis at TRL 9 and LFP / Na-ion at TRL 9 / 7 respectively [IEA-GHR-2025][NREL-ATB-2025]. The architecture-level conclusion is that PEM-and-Li-ion is a defensible default but not a defensible only design. The survival stack in section 10.6 is the explicit alternative.

The regional results show an asymmetric outcome on H2. EU (Norway) and AU (Tasmania) have candidates that simultaneously clear >= 4.0 on both composites; the best US and NZ candidates clear deploy but not autonomy. Operationally this is consistent with the SUP-axis scores. US autonomy is hurt by the WAT-or-supply trade-off across Pacific Northwest, ERCOT, and Iowa rather than by absolute resource quality. NZ autonomy is hurt by SUP = 2 in both candidates [MBIE-NZ-H2-2023]. The recommendation matrix in section 10.5.4 reflects the deploy weighting, which is the correct weighting for a commercial first deployment.

The `maritime_blockade` profile is included as a tail-risk thought experiment, not a base-case planning scenario. Its multipliers, 2.20x for PEM capex and 3.50x for Li-ion capex, are illustrative ceilings rather than market-derived elasticities. They are useful for stress-testing the design margin under H3; they are not useful for valuation.

Region scores are necessarily judgement-laden. Publishing the rubric (section 10.4.3), the per-axis sources in `regions.py`, and the composite weights allows critique on the correct object: the inputs and weights, not a single composite number.

AEM electrolysis is at TRL 6-7 in 2026 [IEA-GHR-2025]. Reliance on AEM at the 2 MW scale carries first-of-a-kind risk that PEM and alkaline do not. The survival stack therefore selects alkaline (TRL 9) rather than AEM. AEM remains a watch-list item.

45V is in force as of 2026-05 with the January 2025 final rule [IRA-45V]. The political risk of repeal or material amendment is flagged in the risk register (chapter 07) and is the single largest US-side non-technical risk to the LCOH numbers in section 10.5.

Finally, fringe technologies (low-energy nuclear reactions and similar) are not part of any architecture in this chapter. The [Berlinguette-2019] multi-laboratory null result remains the controlling evidence for exclusion.

### Geopolitical neutrality statement

This chapter names supply concentrations from public USGS and IEA data. It does not advocate any particular foreign policy stance. The shock profiles in `supply.py`, including `china_decoupling`, `western_only`, and `maritime_blockade`, are stress-test settings used to size the survival stack. They are not endorsements of decoupling, friend-shoring, or any other policy posture.

## 10.8 Limitations

- **Region-scoring weights are illustrative, not optimised.** No objective function (minimise LCOE-at-risk, maximise expected deliverability, etc.) has been used to fit the deploy and autonomy weights. They are a defensible default; alternative weightings will change the ranking, in particular within the US block where the top three are within 0.25 deploy points.
- **Region-scoring rubric is not expert-validated.** The 0-5 scores have not been reviewed by named domain experts. Numbers should not be cited as authoritative; they are auditable inputs to a transparent rubric.
- **Shock multipliers are illustrative, not market-derived.** The multipliers in `supply.py` are not estimates from price-elasticity studies of mineral markets. They are stress-test settings calibrated against historical PGM and Li price excursions and should not be read as forecasts.
- **First-of-a-kind risk for the survival stack at 2 MW.** No 2 MW alkaline + SOFC + LFP + biomass-black-start integrated stack has been demonstrated to the author's knowledge. Sub-system TRLs are 8-9 individually; the integrated TRL is lower.
- **USGS MCS 2026 figures are 2024 production data.** Concentration shares shift annually [USGS-MCS-2026]. The matrix in section 10.5.1 should be refreshed against MCS 2027 when it is released (January 2027).
- **Only 14 regions are encoded.** The geographic coverage is representative, not exhaustive. In particular Canada, Chile, Morocco, South Africa, India, and Japan are absent and would change cross-jurisdiction comparison.
- **Fringe-technology pathways excluded.** Per [Berlinguette-2019], low-energy nuclear reactions are not investable as of the report date and are excluded from all architectures, including the survival stack.

## 10.9 Forward work

- Empirical validation of region scores via a formal Multi-Criteria Decision Analysis (MCDA) against a stated objective function (e.g. minimise expected LCOE under a probability-weighted shock ensemble).
- Bottom-up critical-minerals pricing model linked to commodity-futures data, replacing the illustrative multipliers in `supply.py` with empirically calibrated distributions.
- Hardware-in-the-loop test of the cold-start sequence on a sub-scale rig (~50 kW), to validate the < 6 h target and the biomass + SOFC sequencing.
- Integration with [AEMO-ISP-2026] (when released) and ENTSO-E TYNDP 2026 for INT-axis updates, and with the next USGS MCS for the exposure matrix.
- Extension of the regional database to Canada (BC/Quebec hydro), Chile (Atacama solar), Morocco (solar + REPowerEU partnership), South Africa (PGM-adjacent), Japan, and India, with full per-axis source traceability matching the existing entries.
