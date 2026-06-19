# 07 - Risk Register

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See `DISCLAIMER.md` at the repository root.

## Risk acceptance criteria

The register classifies each top-quartile risk against four standard treatments: accepted, mitigated, transferred, or avoided. The criteria below set the boundary.

A risk is **accepted** when its residual exposure after low-cost controls is within the project's tolerance and further treatment costs more than the expected loss. R10 (lithium price reversal) and R12 (fuel-cell price stays at low-volume multiples) sit in this class. They are monitored, not engineered around.

A risk is **mitigated** when active engineering, procurement, or process controls reduce its likelihood or impact below the action threshold. Most of the register sits here: R1 (leakage), R3 (iridium), R4 (interconnect queue), R7 (durability), R11 (cyber), R13 (community), R14 (price volatility). The mitigation owner is named for each.

A risk is **transferred** when a third party is paid to absorb the residual. R2 (bondability) and R15 (insurance step-up after a sector incident) are transfer items. The premium is the cost of transfer, and the limit is the cap on transferred exposure.

A risk is **avoided** when the project changes scope rather than carry the risk. R8 (tidal cost overrun on the coastal variant) is avoided in the headline plan: tidal is variant-only and is not pre-committed.

The register is reviewed quarterly. A risk that crosses the threshold for re-classification triggers a written change order, not a quiet update.

## Top-quartile register

Top-quartile risks only. Each carries a likelihood (L), impact (I), and a named mitigation owner. The full register lives in the project's risk-management system once deployment is funded.

| ID | Risk | L | I | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | H2 leakage exceeds 1 percent budget, breaching 45V/RFNBO and inflating indirect GHG | M | H | Continuous leak detection at all stages; annual integrity audit; OEM warranty includes a leakage clause | HSE lead |
| R2 | Insurance market unwilling to bond a 36 M USD H2 project at acceptable premium | M | H | Engage Marsh McLennan energy practice plus one reinsurance partner pre-bid; carry NFPA 2 and ATEX compliance docs into procurement | CFO |
| R3 | Iridium price spike (PEM electrolyzer) | M | M | Dual-source procurement; AEM/alkaline alternative pre-qualified for substitution; recovery clause with stack OEM | Procurement |
| R4 | Solar interconnect queue delay greater than 24 months from FERC Order 2023 backlog (US scenario) | M | H | File interconnect study at Month 0 of the grant; carry alternative behind-the-meter sizing as plan B | Project mgmt |
| R5 | IRA section 45V regulatory change (administration turnover) | L | H | Project economics tested with and without 45V; non-US scenarios retain a commercial case independently | CFO |
| R6 | EU RFNBO three-pillar compliance failure (additionality) | L | H | Sign new-build PPA at financial close; do not retrofit existing renewable | Legal |
| R7 | Stack durability less than 80,000 hr in field operation | M | M | Accelerated stress test on the car-track bench; field replacement reserve in opex; OEM warranty | Engineering |
| R8 | Tidal cost overrun (coastal variant) | H | H | Carry coastal as variant only; do not pre-commit until host site is selected and tidal cost is de-risked | Project mgmt |
| R9 | Water-rights challenge at host site | L | H | WRI Aqueduct screening at site short-list; community engagement starts before site select | Community lead |
| R10 | Lithium battery cell price reversal of 2020-2024 declines | M | M | Battery component is a small share (about 0.5 M USD); easily resized | Procurement |
| R11 | Cybersecurity / OT attack on inverters or control system | M | M | IEC 62443 compliance; air-gapped safety PLC; SBOM tracked for all firmware | OT security |
| R12 | Fuel-cell stack price stays at 2 to 3 times automotive volume cost | M | M | A 1 M USD car-track validates the spec but does not commit procurement before the volume curve is confirmed | Engineering |
| R13 | Public opposition to district H2 siting (NIMBY) | M | M | Pre-application community engagement is budgeted; community ownership share offered (project-internal) | Community lead |
| R14 | Grid-import price volatility breaks LCOE band | M | M | Long-duration storage sized to ride 7-day grid outages; PPA hedge | CFO |
| R15 | Insurance step-up after first H2 industry incident in deployment region | M | M | Proactive disclosure of safety case; benchmark premium against natural-gas-equivalent class | CFO |

## Insurance and bondability

H2 project insurability is the single most underestimated risk in deployments above 30 M USD. The project commits to:

1. Engaging an energy-specialist broker in the first 90 days post grant award.
2. Producing an NFPA 2 and ATEX compliant safety case as a *funded deliverable*, not an afterthought.
3. Sharing operational H2 leakage data with the broker quarterly to reduce premium drift.

If the insurance premium at financial close exceeds 1.5 percent of deployed capex per year, the project pivots to an alkaline electrolyzer (less PGM exposure, better-understood industrial class) and reduces H2 storage tonnage by 30 percent. This pivot is pre-engineered, not invented at crisis time.

### Broker classes engaged

The bondability strategy needs more than a single broker relationship. Five classes of intermediary are engaged in parallel.

**Lead energy broker (large-cap).** Marsh McLennan energy and power practice or Aon natural resources practice. They place the primary property, builder's risk, and operational liability layers. They have the relationships with London-market and Bermuda-market underwriters that write hydrogen risk today.

**Specialist hydrogen and clean-energy broker.** GCube, Tokio Marine HCC clean-energy team, or Howden specialty for renewable and emerging-energy lines. These brokers carry the technical underwriters who can read an NFPA 2 safety case and price it correctly. The lead broker frames the deal; the specialist broker prevents over-pricing through ignorance.

**Surety broker for performance and decommissioning bonds.** Liberty Mutual surety, Zurich surety, or Travelers bond department. Performance bonds for EPC contractors, decommissioning bonds where required by the host jurisdiction, and parent-company guarantees are placed here.

**Marine and cargo broker (coastal variant only).** Lockton marine or WTW marine. Tidal and barge-delivered components, if the coastal variant proceeds, need separate marine cargo and installation cover.

**Reinsurance contact, direct.** Munich Re green-tech, Swiss Re corporate solutions, or Hannover Re facultative. Direct dialogue with a reinsurer at the design stage shapes the primary terms and often unlocks capacity that the primary market will not write alone.

The CFO maintains a contact log for each class. The log is reviewed at every quarterly risk meeting.
