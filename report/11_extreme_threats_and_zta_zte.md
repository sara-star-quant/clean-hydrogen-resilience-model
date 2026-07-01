# 11 - Extreme-Threat Architectures and Zero-Trust Engineering

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

## 11.1 Background

Earlier chapters scope the water-medium energy system around expected operating envelopes: nominal solar and wind resource, intact grid interconnection, supplier-supported firmware, a stable policy regime. The 2026 threat landscape contains classes of constraint that those envelopes do not cover, and that nonetheless determine whether a 2 MW district microgrid plus a Class 8 FCEV truck fleet can be relied upon over a 25-year asset life. This chapter scopes three such classes and sets the architectural response.

**Class A: weather-immune baseload demand.** Multi-month-to-multi-year suppression of variable renewable output. The reference cases are: a VEI 6+ stratospheric volcanic injection causing global insolation depression on the order of 5-10% for 2-3 years (Pinatubo 1991 produced roughly 0.4 K cooling and ~3% direct-beam reduction at mid-latitudes; a Tambora-class event is plausibly an order of magnitude larger); persistent regional dust-storm regimes; sustained heat-dome events that simultaneously suppress wind and reduce PV efficiency by 8-12% (each 10 K above STC reduces output by ~4%); and cyber-physical compromise of inverter fleets disabling otherwise-available solar/wind capacity.

**Class B: adversarial cyber-physical conditions.** Coordinated grid attacks on the OT layer, GPS/UTC time-source spoofing affecting protection coordination and synchrophasor logic, supply-chain firmware injection in PLCs/inverters/BMS, AI-orchestrated lateral attacks that out-pace human defender cycles, and a "Q-day" event in which a cryptanalytically-relevant quantum computer breaks RSA/ECC and invalidates legacy firmware-signing and TLS chains. NIST has standardised the post-quantum primitives (FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA, August 2024); industrial OT migration is the slow path. The relevant standards baseline for the OT side is IEC 62443-3-3 (system security requirements and security levels) and IEC 62443-4-1/4-2 (secure product development and component requirements).

**Class C: auto-recovery under continuous damage.** War-zone, disaster-zone, sabotage, and prolonged-outage operating regimes where components fail at sustained rates incompatible with vendor SLAs. The system must continue to serve critical load while individual elements are damaged, replaced, or worked around. This is the operating regime against which Defence Production Act (DPA) and Critical Raw Materials Act (CRMA) funders evaluate "resilience" deliverables.

The hydrogen-leakage GWP penalty quantified in chapter 06 (GWP100 ~11.6, [Sand-2023]) is relevant here because cyber-physical compromise of leakage-detection sensors would silently invalidate the project's <1% leakage commitment ([IEA-GHR-2024]). Supply-chain framing follows [IEA-CMO-2025].

## 11.2 Probabilistic framing disclaimer

Probabilities for the tail events catalogued in this chapter are not calibrated. The threat register (Table 11.1), the "blast radius" estimate in section 11.4.2, and the auto-recovery sketch in section 11.4.3 are architectural readiness instruments, not a probabilistic risk model. We do not claim to know the annual probability of a Carrington-class GMD, a Q-day event, or a VEI 6+ eruption. The chapter argues that the system either has a defined response to each class or it does not, and that defined response is the deliverable. Quantitative risk weighting is out of scope for this document.

## 11.3 Hypothesis

- **H1 (weather-immune mix).** A baseload mix of geothermal-EGS + SMR + biomass-CHP can serve the 2 MW district at a levelised cost within 1.5x of the solar-H2 hybrid baseline, at the cost of 30-40% higher upfront capex.
- **H2 (zero-trust blast radius).** A Zero-Trust Architecture with hardware root-of-trust, signed firmware, microsegmentation, and air-gapped safety PLC reduces the most-exposed-vulnerability blast radius by >= 1 order of magnitude relative to a default ICS deployment.
- **H3 (auto-recovery availability).** An N+2 redundancy design with hot-swap modular components and mechanical override on every safety-critical loop maintains >= 95% critical-load availability under a continuous-damage scenario simulated at one component failure per week.

## 11.4 Methods

### 11.4.1 Threat register

Fifteen extreme threats are scoped (Table 11.1). Each row carries a regional/global classification, a prevent strategy (reduce probability of impact), and a tackle strategy (reduce consequence given the event). Probability calibration is not attempted. The register is an architectural readiness instrument, not a quantitative risk model.

**Table 11.1: Extreme-threat register.**

| # | Threat | Scope | Prevent | Tackle |
|---|---|---|---|---|
| 1 | Carrington-class CME / GMD | Global | Faraday-shielded comms cabinet; fibre-only WAN | Manual islanding; spare power transformers in depot; mechanical pony-motor cold start |
| 2 | Q-day (CRQC breaks RSA/ECC) | Global | Crypto-agile firmware update; PQC migration on FIPS 203/204/205 timeline | Pre-installed PQC trust anchors; signed-revocation channel |
| 3 | HEMP (high-altitude EMP) | Regional | Shielded enclosures; surge arrestors at every penetration | Sacrificial I/O; mechanical safety chain unaffected |
| 4 | VEI 6+ volcanic veil | Global | Site selection avoiding ash-fall corridors | Geothermal-EGS + SMR + biomass-CHP baseload; 12-month fuel buffer |
| 5 | Megathrust earthquake | Regional | Seismic design class IV; underground H2 storage avoided in fault zones | Modular skids on isolators; rapid-replacement inventory |
| 6 | Pandemic II (workforce) | Global | Cross-trained staff; remote-operations capability | Hand-startable rig; 1-yr spares depot; on-site dormitory option |
| 7 | GPS / UTC spoofing | Regional | Disciplined OCXO + Rb backup; eLoran where available | Holdover budget >= 72 h; protection logic uses local sequence-of-events |
| 8 | AI-orchestrated grid attack | Global | Default-deny microsegmentation; behaviour-based anomaly detection | Air-gapped safety PLC; manual island mode |
| 9 | Hyperinflation / sovereign default | Regional | Multi-currency contracts; physical commodity hedges | Local-fuel (biomass) self-sufficiency; spares pre-bought |
| 10 | Substation / pipeline sabotage | Regional | Multi-feed interconnect; site fencing IEC 62443 zone-3 perimeter | Black-start from biomass-CHP; H2 storage at low-pressure buffer |
| 11 | Insurance-market collapse | Global | Self-insured reserve fund; mutual-pool agreements | Reduced-coverage operating mode pre-engineered |
| 12 | Regulatory whiplash (e.g. 45V repeal) | Regional | Project NPV stress-tested without 45V; non-US deployment optionality | Off-grid mode does not depend on subsidy |
| 13 | AMOC / climate tipping cascade | Global | Site selection robust to +/-5 K shift in design ambient | Closed-cycle cooling; fuel-flexible biomass intake |
| 14 | Mega-firmware-CVE in deployed fleet | Global | SBOM tracking; multi-vendor diversity on critical paths | Crypto-agile rollback; air-gapped safety PLC unaffected |
| 15 | Late-life H2 embrittlement consensus shift | Global | Material selection to ASME B31.12 + 50% margin; coupon programme | Pipework replaceable at flange boundaries; H2-to-NH3 conversion option |

### 11.4.2 Zero-Trust Architecture (ZTA) layer

ZTA is the policy and identity stratum. Every component mutually authenticates via mTLS using device-resident hardware keys (TPM 2.0 or HSM-backed). Every firmware image is signed and verified at boot via a measured-boot/secure-boot chain rooted in the hardware. East-west traffic is default-deny across microsegments, with one segment per subsystem: PV-DC, electrolyzer, fuel-cell, battery, H2-storage, EMS/SCADA, safety PLC. The safety PLC is air-gapped from the routable network and exchanges only hardwired analogue or discrete signals through optical isolators. Target compliance: IEC 62443-3-3 SL3+ for the EMS/SCADA zone, IEC 62443-4-1 for the secure-development lifecycle of all custom firmware, IEC 62443-4-2 component requirements for procured devices.

### 11.4.3 Zero-Trust Environment (ZTE) layer

ZTE is the physical-trust stratum that complements ZTA. Each control loop receives at least two independent sensor inputs that are cross-validated (e.g. for H2 leakage: catalytic-bead, electrochemical, and ultrasonic, voted 2-of-3). Failsafe defaults are explicit per loop: fail-closed for safety isolation valves and fuel-cell shutdown; fail-static for non-safety dispatch (last-known-good). Time is sourced from a local disciplined OCXO with rubidium backup and an external radio-clock receiver (DCF77/MSF/WWVB depending on region). GPS is used only as a sanity input, never as the authoritative source. Anomaly detection runs per loop with thresholds derived from the loop's own physics envelope, not from generic IT-IDS signatures.

### 11.4.4 Auto-recovery specification

Critical paths carry N+2 redundancy: two electrolyzer skids, two fuel-cell stacks, two BMS-isolated battery strings, two independent inverter blocks per bus. Each skid is ISO-container-mountable and hot-swappable on a quick-disconnect manifold; the mean time to replace is targeted at < 8 h once the spare reaches site. Control authority is distributed: each major subsystem has a local PLC capable of autonomous operation in degraded-comms mode; the central EMS issues set-points but never closes the inner safety loops. A 1-year spares depot is held at a separate site. Consumables (deionised water, biomass fuel, lubricants) are stocked for 6 months at minimum. Cold-start does not require an external grid: a mechanical pony motor (compressed-air or hand-cranked diesel) initiates the biomass gasifier, which energises the auxiliary bus, which in turn brings the fuel-cell or SMR auxiliaries online.

### 11.4.5 Post-Quantum Cryptography migration

Cryptographic boundaries are inventoried (Table 11.4 below). Each is mapped to (current algorithm, target algorithm, migration year, validation method). The target algorithms are drawn exclusively from the NIST PQC standards: FIPS 203 (ML-KEM, key encapsulation), FIPS 204 (ML-DSA, primary signatures), and FIPS 205 (SLH-DSA, hash-based signatures for long-lived firmware roots-of-trust). Crypto-agility is built into the firmware update protocol so that algorithm rotation does not require a hardware refresh.

## 11.5 Results

### 11.5.1 Architecture variants

Three variants are compared at 2 MW district scale. Capex is from `tech_params.yaml` central values. LCOE is order-of-magnitude derived from those capex/opex/CF values at a 5% discount rate over each technology's lifetime. Chapter 04 carries the calibrated dispatch-based LCOE; the figures here are presented for cross-architecture ranking, not for finance-grade quotation.

**Table 11.2: Architecture variants for 2 MW district load.**

| Property | A: Solar-H2 baseline (`district_solar_h2_inland`) | B: Weather-immune (`district_no_solar_no_wind` + SMR enabled) | C: Hybrid resilient (`district_autonomy_max` + EGS) |
|---|---|---|---|
| Primary generation | 8 MWp PV | 1.5 MW EGS + 2 MW SMR + 0.5 MW biomass | 8.5 MWp PV + 0.5 MW biomass + 1 MW EGS |
| Storage | 12 t H2 + 1.5 MWh Li-ion | 4 t H2 + 2 MWh LFP | 14 t H2 + 2 MWh LFP |
| Firm-power capability | Low (weather-bound) | High (three independent firm sources) | Medium (one firm source + large storage) |
| Indicative capex (USD M) | ~18 | ~35 | ~26 |
| Indicative LCOE ratio vs A | 1.0x | 1.35-1.50x | 1.15-1.25x |
| Availability under 2-yr veil | 40-60% | 95%+ | 85-90% |
| Weather dependence | High | Negligible | Moderate |
| Political-acceptability risk | Low | High (nuclear) | Medium |
| Supply-chain concentration | High (PGM, Li) | Medium (nuclear fuel, drilling) | Medium |

Reading: B clears H1 in capex (~+95% over A, above the hypothesised 30-40% band, driven by SMR first-of-a-kind premium [NREL-ATB-2025]); LCOE lands at 1.35-1.5x as hypothesised. C is the policy-realistic compromise. H1 holds for LCOE; the capex band must be widened to 50-100% to be honest about FOAK SMR cost.

### 11.5.2 ZTA / ZTE control coverage matrix

Rows are subsystems; columns are the principal ZTA/ZTE controls. F = full coverage, P = partial, N = not applicable, X = explicit gap accepted with mitigation.

**Table 11.3: Control coverage matrix.**

| Subsystem | mTLS east-west | Signed firmware | HW root-of-trust | Microsegment | Air-gap from safety | Sensor 2-of-3 | Failsafe default | GPS-independent time |
|---|---|---|---|---|---|---|---|---|
| Solar PV inverter | F | F | P (TPM retrofit) | F | F | N | fail-static | F |
| Electrolyzer (PEM/alkaline) | F | F | F | F | F | F (H2/O2 sensors) | fail-closed | F |
| Fuel cell (stationary) | F | F | F | F | F | F | fail-closed | F |
| Battery (LFP/Na-ion) | F | F | F | F | F | F (BMS triple-vote) | fail-static | F |
| H2 storage (700 bar / buffer) | F | F | F | F | F | F (leak detection) | fail-closed | F |
| EMS / SCADA | F | F | F | F | F (one-way diode out) | N | fail-static | F |
| Safety PLC | N (hardwired only) | F | F | N (air-gapped) | - | F | fail-closed | F |
| Truck FCEV onboard | P (cellular link only) | F | F | F | F | F | fail-closed | F |

Blast-radius estimate: under a default ICS deployment, a successful firmware-CVE exploit on the EMS propagates laterally to all OT subsystems within minutes (single trust domain). Under the matrix above, the same exploit is bounded to the EMS microsegment, cannot cross the air-gap to the safety PLC, and cannot issue commands accepted by component PLCs that require mTLS-authenticated signed dispatch. Quantitatively, "subsystems reachable from a single foothold" drops from 7-of-7 to 1-of-7 (EMS only). H2 holds.

### 11.5.3 Auto-recovery simulation

A discrete-event sketch with one component-failure event per 7 days, exponential-distributed repair time with mean 8 h (on-site spare available) or 14 d (depot dispatch required, 10% of failures), 1-year horizon. Critical-load cutoff is 1.0 MW (50% of nominal); below this the district sheds non-essential load.

**Table 11.4: Auto-recovery scenario outcomes.**

| Failure pattern | Coincident component count | Critical load served | Notes |
|---|---|---|---|
| Steady-state, 1 fail / week | 1 | 100% | N+2 absorbs |
| Burst, 2 simultaneous | 2 | 100% | N+2 absorbs |
| Burst, 3 simultaneous | 3 | 70-85% | one redundancy path exhausted |
| Depot-dispatch event, 14 d | 1 | 95% | bridged by H2 buffer + biomass |
| Annualised, 52 events at 1/wk | rolling | 96.4% mean | meets H3 (>= 95%) |

H3 holds at the simulated rate. Sensitivity to mean-time-to-repair is high. At 24 h on-site MTTR the annualised number drops to 92%, and N+2 must be widened on the most-failure-prone subsystem (in fleet field data this is consistently the inverter and power-electronics layer).

### 11.5.4 PQC migration plan

**Table 11.5: Cryptographic boundary migration.**

| Boundary | Current algorithm | Target algorithm (NIST FIPS) | Migration year | Validation method |
|---|---|---|---|---|
| Firmware signing root | RSA-3072 / ECDSA-P256 | SLH-DSA (FIPS 205) | 2027 | Hash-based signature verification on cold-stored test vectors; cross-vendor witness |
| mTLS device identity (OT east-west) | ECDSA-P256 + ECDHE | ML-DSA + ML-KEM (FIPS 204/203) | 2028 | Interop test against NIST CAVP-validated implementations |
| PPA / contract digital signing | RSA-2048 / ECDSA-P256 | ML-DSA (FIPS 204) | 2027 | Counterparty co-validation; legal admissibility opinion |
| Time-stamp authority | RSA-2048 | ML-DSA (FIPS 204) | 2028 | RFC 3161 profile update; long-term archival re-signing pipeline |
| Truck-to-station session keys | ECDHE-P256 | ML-KEM (FIPS 203) | 2029 | Field interop trial with at least two refuelling-station vendors |

Crypto-agility requirement: every boundary above must support algorithm negotiation and key-rollover without firmware reflash, so that a future migration (for example should ML-DSA be deprecated) does not require a fleet recall.

## 11.6 Discussion

A project credible only under nominal weather and nominal cyber conditions is not a credible candidate for DPA, CRMA, or energy-security funding lines. Resilience is therefore not an add-on; it is itself a deliverable, evaluated by funders as such. The three-class framing in section 11.1 maps cleanly onto three funder questions: what if the resource fails for two years; what if the adversary is competent; what if components fail faster than vendors can ship. The architectural responses (variants A/B/C, the ZTA/ZTE matrix, N+2 with mechanical override) answer those questions architecturally, even where the underlying probabilities cannot be calibrated.

Trade-offs are real and not symmetric. SMR brings firm-power and fuel density at the price of nuclear-political acceptability, which in many jurisdictions is binding regardless of LCOE. Geothermal-EGS removes the political question but adds drilling-cost risk and sub-surface uncertainty; the [NREL-ATB-2025] capex range of $5,000-12,000/kW reflects exactly this. Biomass-CHP is the most politically straightforward but adds feedstock-supply risk that is itself sensitive to the same climate-tipping pathways the system is meant to be insulated from. Variant C diversifies these, at the cost of operating three different firm-source supply chains.

We are deliberate about the tail-risk framing. Many threats in Table 11.1 are events for which we do not claim probability calibration. The deliverable is architectural readiness: the system either has a defined response or it does not. "Defined response" means a procedure, a piece of installed hardware, or a documented operating mode, not a hope that the threat will not materialise.

### Cyber security disclosure policy

Any vulnerability discovered in deployed systems will be disclosed to the broker, the OEM, and the user community per coordinated-disclosure norms. Standard practice will include a fixed remediation window before public disclosure, expedited handling for actively exploited issues, and a CVE record where the boundary affects multiple deployments. The intent is to align with established industrial-control-system disclosure conventions (CISA ICS-CERT, vendor PSIRT processes) rather than to publish without coordination.

## 11.7 Limitations

- ZTA in microgrid OT environments is at TRL 7 in 2026 for the integrated stack described here. Individual elements (TPM-backed mTLS, signed firmware, microsegmentation) are mature in IT and partially deployed in OT, but the air-gapped-safety-PLC plus crypto-agile-firmware combination at MW scale is first-of-a-kind for several subsystems. A pen-test campaign on a sub-scale rig is required before any deployment claim.
- The PQC migration plan assumes FIPS 203/204/205 stability through the 2027-2029 deployment window. NIST or sector-specific recommendations (NSA CNSA 2.0, BSI TR-02102, NCSC) may diverge; the plan must be revisited annually.
- N+2 redundancy carries a 25-35% capex premium on the affected subsystems and is only justified for resilience-priority deployments (DPA, military, island/remote, disaster-relief). Commercial deployments will rationally choose N+1.
- AI-orchestrated grid attack is a moving target. Static defences (rule-based IDS, signature-based AV) will lag. The architectural response in this chapter is structural (microsegmentation, air-gap, fail-closed) rather than detection-based, which is the only honest posture against an attacker whose tooling iterates faster than ours.
- Insider threats are out of scope. The implicit assumption is that personnel-security regimes (background checks, dual-control on critical commands, audit-log integrity) are handled at the organisational layer. A dedicated insider-threat chapter would be required for a defence-customer deployment.
- The auto-recovery simulation in section 11.5.3 is a discrete-event sketch, not a calibrated reliability model. Field data for hot-swap MTTR on the specific skid designs is not yet available; the 8 h on-site and 14 d depot figures are plausible but unverified.
- Tail-event probabilities are not calibrated. The threat register is for architectural readiness, not for quantitative risk weighting.
- The indicative LCOE and capex ratios in Table 11.2 are for cross-architecture ranking only; finance-grade numbers are produced by the chapter 04 dispatch model.

## 11.8 Forward work

- Pen-test campaign against a sub-scale ZTA/ZTE rig before first deployment, scoped per IEC 62443-3-2 risk-assessment methodology. Target milestone: Month 18.
- Tabletop exercise on a coincident scenario: Carrington-class GMD plus pandemic-II workforce attrition. Output: a documented degraded-operations procedure, tested against the hand-startable cold-start chain.
- Continuous-monitoring SIEM/SOC integration with a named MSSP partner at deployment, with OT-specific detections (Modbus/IEC 61850/DNP3 traffic baselines, not just IT logs).
- Public-trust deliverable: a hand-startable rig demonstration filmed and published, showing cold-start from grid-off, network-off, and GPS-off conditions through to critical-load energisation, on biomass alone.
- Annual review of the PQC migration plan against NIST and sector publications, with explicit re-validation of the Table 11.5 timeline.
