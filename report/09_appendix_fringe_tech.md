# 09 - Appendix A: Fringe-Tech Evidence Review

> **Disclaimer.** Research document. Not financial, legal, engineering, or tax advice. Not a fundraising solicitation. See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

## A.1 Why this appendix exists

Reviewers of energy-transition proposals routinely encounter pitches built on cold fusion, hydrinos, water-as-fuel cells, and overunity machines. A grant or investment review that ignores these claims can read as either naive or evasive. This appendix documents that the project team has examined the most prominent fringe-energy claims, applied a uniform evidence rubric, and reached a defensible exclusion decision for each. The main report (Chapters 02 to 08) commits to grounded technologies only: alkaline and PEM electrolysis, hydrogen storage and fuel-cell powertrains, and established balance-of-plant. Those are the technologies with the replication record, supply chain, and bankability the FCEV truck and 2 MW microgrid tracks require. The purpose of this appendix is not to debate. It is to demonstrate due diligence and to specify, for each candidate, the empirical conditions under which we would reopen the question.

## A.2 Evidence rubric

Each technology is scored against five criteria. Scores are conservative; absence of evidence yields a low score, not a neutral one. The rubric reflects the published peer-reviewed record as of the project cutoff.

| # | Criterion | Scale | What "High" looks like |
|---|-----------|-------|------------------------|
| R1 | TRL of any peer-reviewed replication | 1-9 (NASA scale) | TRL >= 6 (system demonstration in relevant environment) reproduced by independent group |
| R2 | Number of independent peer-reviewed replications | None / 1 / 2-4 / >= 5 | >= 5 independent groups, journal of record |
| R3 | Energy-balance plausibility | High / Medium / Low / None | Mechanism consistent with conservation of energy and known cross-sections |
| R4 | Fraud / retraction history | None / Isolated / Recurrent | No retractions, no documented prosecutions, no pattern of unverifiable demos |
| R5 | Commercial viability today | High / Medium / Low / None | A unit can be purchased, metered, and audited by a third party with reproducible kWh-in / kWh-out figures |

A "High" overall verdict requires High or near-High across all five rows. Any "None" on R3 (energy-balance plausibility) is treated as disqualifying for investable scope, regardless of the other rows. A project funded by public grant agencies cannot stake deliverables on the falsification of conservation laws.

## A.3 Catalogue

### A.3.1 Cold fusion / Low-Energy Nuclear Reactions (LENR)

The history runs from the 1989 Pons-Fleischmann electrolytic-palladium "excess heat" announcement, through Mizuno's nickel-hydrogen variants, to Andrea Rossi's E-Cat demonstrations, which never produced an independently metered, isolated commercial unit. The most rigorous modern attempt is the Google-funded multi-laboratory program led from UBC and reported by Berlinguette and colleagues [Berlinguette-2019]. That program was explicitly designed to give LENR its fairest hearing in three decades. It deployed calorimetry, materials science, and nuclear-product diagnostics across multiple institutions. It found no reproducible excess heat and no nuclear signatures above background, while substantially advancing the metrology for any future attempt.

Rubric: R1 TRL 2-3 at best (bench experiments, contested calorimetry); R2 None at peer-reviewed standard since 1989; R3 Low (would require a screening mechanism for Coulomb repulsion in condensed matter for which no theoretical framework has survived peer review); R4 Recurrent (Rossi litigation, repeated failure of public demonstrations under independent metering); R5 None (no auditable commercial unit exists).

Verdict: Excluded. LENR remains a research curiosity. It is not an engineering basis for a 2 MW microgrid or a Class 8 truck.

### A.3.2 Hydrinos / Brilliant Light Power / Randell Mills

The hydrino hypothesis posits hydrogen states below the quantum-mechanical ground state, releasing energy via "fractional Rydberg" transitions. The theory (Mills' "Grand Unified Theory of Classical Physics") is rejected by mainstream physics because it contradicts the standard solution of the Schrodinger equation for hydrogen, which has been verified to extremely high precision by atomic spectroscopy. Brilliant Light Power (formerly BlackLight Power) has, over more than two decades, repeatedly announced imminent commercial demonstrations (SunCell variants) that have not produced an independently metered net-energy unit purchasable by a customer.

Rubric: R1 TRL 2 (prototype demos, not independently replicated); R2 None (no peer-reviewed independent replications of net energy gain); R3 None (requires revising the hydrogen ground state, which is among the best-tested results in physics); R4 Isolated (no fraud findings, but a long pattern of unfulfilled commercialization timelines); R5 None.

Verdict: Excluded. The energy-balance disqualifier (R3 = None) is decisive on its own.

### A.3.3 Water-as-fuel devices: Stanley Meyer cell, HHO / Brown's gas, oxyhydrogen fuel-saver supplements

This family covers (a) Meyer's "water fuel cell" patents, the underlying claims of which were ruled "fraud" by an Ohio court in 1996; (b) HHO / Brown's gas generators sold as fuel-economy add-ons for internal-combustion vehicles; and (c) related "structured water" or "plasma water" fuel claims. The physics is simple. Dissociating water into H2 and O2 by electrolysis, then recombining them, cannot yield more energy than was input. That is the definition of a thermodynamic cycle bounded by the enthalpy of formation of water. Independently instrumented dynamometer studies of HHO add-ons have consistently found no statistically significant fuel savings, with apparent gains traceable to ECU-feedback artefacts.

Rubric: R1 TRL 1 for net-energy claim; R2 None; R3 None (closed-cycle water -> H2/O2 -> water net-positive output violates the first law of thermodynamics); R4 Recurrent (Meyer fraud ruling; ongoing FTC-style consumer-protection actions against HHO vendors); R5 None for net energy. The devices exist and run, but at net loss.

Verdict: Excluded. Note that on-board electrolysis from grid or solar electricity to feed a fuel cell or H2 ICE is grounded technology and is the subject of Chapters 03 to 04. The exclusion here is specifically of the closed-loop water-as-fuel net-energy claim.

### A.3.4 Magnet motors, overunity, free-energy devices

This category encompasses permanent-magnet motors that allegedly deliver continuous shaft power without input, Bedini-style "battery rejuvenators" claimed to gain net energy, and various solid-state "zero-point" devices. All such claims violate the second law of thermodynamics, a constraint also embedded in IPCC AR6 working-group analyses of energy-system pathways. Any decarbonization scenario in AR6 budgets energy by conservation, not by hypothetical free sources. No independently audited overunity device has ever passed metering by a national-laboratory or accredited test house.

Rubric: R1 TRL 1; R2 None; R3 None (second-law violation); R4 Recurrent (long history of investor losses and consumer-protection actions); R5 None.

Verdict: Excluded with no further analysis warranted.

### A.3.5 Briefly noted: real physics, not engineering-viable

- **Muon-catalysed fusion.** A genuine, peer-reviewed nuclear process. A muon temporarily replaces an electron in a D-T molecule, allowing fusion at low temperatures. The blocker is muon production cost and the alpha-sticking limit, which together push break-even out of reach with current technology. R3 is High (real physics), but R1 and R5 remain Low. Not investable on grant timescales; we monitor it as a long-horizon basic-science item.
- **Pyroelectric fusion.** Demonstrated (Naranjo et al., 2005, peer-reviewed) and reproduced as a tabletop deuteron source. Produces real neutrons but at fluxes orders of magnitude below energy break-even. Viable as a portable neutron generator, not as a power source. R3 High, R1 ~4 for neutron-source application, R5 Low for net energy.

Both are catalogued here so reviewers see we distinguish "fringe physics" from "fringe engineering against real physics."

## A.4 Summary verdict table

| Technology | R1 TRL | R2 Replications | R3 Plausibility | R4 Integrity | R5 Commercial | Investable? |
|---|---|---|---|---|---|---|
| Cold fusion / LENR | 2-3 | None | Low | Recurrent | None | No |
| Hydrinos | 2 | None | None | Isolated | None | No |
| Water-as-fuel (closed-loop) | 1 | None | None | Recurrent | None | No |
| Magnet / overunity | 1 | None | None | Recurrent | None | No |
| Muon-catalysed fusion | 3-4 | >= 5 (physics, not power) | High | None | None | No (basic science only) |
| Pyroelectric fusion | ~4 (as neutron source) | 2-4 | High | None | Low (non-power use) | No (not a power source) |

One-line verdicts:

- **LENR:** The best-resourced modern replication attempt returned a null result [Berlinguette-2019]; no engineering basis.
- **Hydrinos:** Requires overturning the hydrogen ground state; no independently metered commercial unit in 25+ years.
- **Water-as-fuel:** Violates the first law in the closed loop. On-board electrolysis from external electricity is a different and grounded matter, covered in the main report.
- **Overunity:** Violates the second law. Energy-system analyses, including IPCC AR6 mitigation pathways, are bounded by conservation rather than by hypothetical free sources.
- **Muon-catalysed and pyroelectric fusion:** Real physics, but neither yields net power on present engineering.

## A.5 Falsification conditions: what would change our position

We commit, in writing, to the following reopening criteria. Each is operational, third-party-auditable, and tied to the literatures of record.

- **LENR.** Independently replicated continuous excess heat at a signal-to-noise ratio of at least 10x the calorimetry noise floor, observed by at least five geographically and institutionally independent laboratories, with results published in *Nature*, *Science*, or *Physical Review Letters* within a rolling three-year window, accompanied by a nuclear-product signature (helium-4, neutron, or gamma) consistent with the claimed reaction rate. Absent the nuclear signature, we treat continued heat-only claims as chemical or calorimetric artefacts, consistent with the [Berlinguette-2019] framework.

- **Hydrinos.** Independent measurement, by a national metrology institute (e.g., NIST, NPL, PTB), of a hydrogen spectroscopic line corresponding to a sub-ground-state transition, plus a metered, sealed, third-party-audited net-energy unit operated for >= 1000 hours with input/output electrical accounting.

- **Water-as-fuel (closed-loop).** A sealed device with only water as input and water as output, producing net positive electrical or shaft work, audited by an accredited test house (e.g., TUV, UL, DEKRA) over >= 100 hours. We assess the prior probability of this as effectively zero, but the falsification path is well-defined.

- **Overunity / magnet motors.** Same protocol: sealed device, accredited test house, no concealed input, >= 100-hour run, full energy accounting. Same near-zero prior.

- **Muon-catalysed fusion.** A demonstrated muon-production pathway (e.g., advanced accelerator or muon-collider spinoff) reducing muon cost per fusion below the energy released per muon, with the alpha-sticking fraction reduced below ~0.5%, in peer-reviewed work.

- **Pyroelectric / inertial-electrostatic fusion.** Demonstrated Q (fusion power out / electrical power in) > 1 in a peer-reviewed, independently replicated experiment. Until then, useful as a neutron source only.

Until these conditions are met, the project will continue to allocate capital and grant-matched resources only to electrolytic green hydrogen and its directly downstream applications, as scoped in Chapters 03 and 04.

## A.6 References used in this appendix

- [Berlinguette-2019] Berlinguette, C. P. et al. "Revisiting the cold case of cold fusion." *Nature* 570, 45-51 (2019). doi:10.1038/s41586-019-1256-6.
- IPCC AR6 Working Group III, *Climate Change 2022: Mitigation of Climate Change*. Used here for the framing that decarbonization pathways are bounded by energy conservation; cited in report/references.md.
- Additional citations (Pons and Fleischmann 1989; Naranjo et al. 2005 on pyroelectric fusion; Ohio v. Meyer 1996 ruling; standard thermodynamics texts) are listed in the project references file and are not duplicated here to avoid mis-cited DOIs.
