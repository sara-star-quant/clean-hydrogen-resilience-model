# Grant Call Tracker

> **Disclaimer.** Planning aid, not legal or financial advice. Call IDs, dates, and
> envelopes must be confirmed against the official portal before any submission.
> See [DISCLAIMER.md](../DISCLAIMER.md) at the repository root.

Scope: **EU-based applicant for now.** EU schemes are primary. US / AU / NZ rows are
parked (kept for the record, not actionable until a resident entity exists in that
jurisdiction).

Status legend:
- **READY** - submittable by a single EU entity with the assets already in this repo.
- **NEAR** - one or two concrete items away from ready.
- **BLOCKED** - needs cost-share, a site, or a multi-party consortium that does not exist yet.

Confirm every `TODO` against the portal URL in the row before drafting.

---

## Primary (EU, in scope)

| Scheme | Track | Current call | Open | Close | Funding rate | Cost-share needed | Entity / consortium | TRL fit | Status | Next action |
|---|---|---|---|---|---|---|---|---|---|---|
| **Horizon Europe Cluster 5 (RIA)** | Car bench + methodology | `TODO: call ID` from https://ec.europa.eu/info/funding-tenders/opportunities/ | `TODO` | `TODO` | **100% direct + 25% flat indirect** | **None** | Min 3 independent legal entities from 3 EU/associated states (collaborative RIA); single-entity only for ERC/EIC-type, not this topic | 4-6 (matches bench) | **NEAR** | Confirm an open Destination 2/3 topic; line up 2 partner entities (university metrology + 1 more); register PIC |
| **Horizon Europe Cluster 5 (IA)** | District 2 MW | `TODO: call ID` (same portal) | `TODO` | `TODO` | 70% (100% non-profit) + 25% flat indirect | 30% if for-profit | Collaborative consortium, plus host/offtaker | 6-7 | **BLOCKED** | Needs site + host + EPC partner + 30% match; defer until bench data exists |
| **EU Innovation Fund (CINEA)** | District 2 MW | `TODO: call ID` from same portal | `TODO` | `TODO` | up to 60% of incremental cost | Yes (40%+ of relevant cost) | Single or multi, but needs near-commercial build | >=7 | **BLOCKED** | Project is pre-deployment; revisit only with a real build + co-investment |

## Parked (non-EU, out of scope until resident entity exists)

| Scheme | Track | Funding rate | Cost-share | Why parked | Status |
|---|---|---|---|---|---|
| US DOE OCED | District | ~50% | $18M match on $36M | US entity + 50% matched capital + site | BLOCKED |
| US ARPA-E OPEN | Car bench | $1-10M | varies | US entity; also TRL/transformational reframing needed | BLOCKED |
| AU ARENA | District | 30-50% capex | Yes | AU proponent + co-investor | BLOCKED |
| NZ Callaghan R&D | Car bench | partial | small | NZ entity | BLOCKED |
| NZ EECA GIDI / MBIE Endeavour | District / research | ~50% | Yes | NZ entity | BLOCKED |

---

## Focus: Horizon Europe Cluster 5 RIA (the one to move on)

Why this is the lead target:
- **100% of eligible direct cost**, plus a 25% flat-rate indirect allowance. No proponent
  cash match. Every other district-scale scheme demands 30-60% co-investment that does not
  exist yet.
- TRL band 4-6 matches the **car bench validation** track as-is. No site, no EPC, no
  offtaker required for the RIA-shaped bench work.
- The open cost model, report chapters, and [_shared_narrative.md](_shared_narrative.md) blocks already cover the
  Part B narrative skeleton. The technical case is largely written.

What still gates a Horizon RIA submission (the NEAR items):
1. **Consortium.** Collaborative RIA needs at least 3 independent legal entities from 3
   different EU member or associated states. Today: 0 named. Minimum viable set = coordinator
   + university metrology lead + one industry partner (FCEV platform or electrolyser).
2. **PIC registration.** Each entity needs a Participant Identification Code on the Funding &
   Tenders portal. Coordinator first.
3. **An actually-open topic.** Confirm a current Destination 2 or Destination 3 topic whose
   scope admits HD-FCEV bench validation or renewable-H2 integration. Calls rotate; the topic
   text must be matched, not assumed.
4. **PI with track record.** Reviewers score the team. Name a PI and 1-2 key staff with
   relevant delivery history.
5. **Open Science / DMP + ethics.** Horizon expects a Data Management Plan and an ethics
   self-assessment; H2 safety touches the ethics appendix.

Sequence:
```
1. Confirm open Cluster 5 topic (Destination 2/3)   -> verify: topic ID + close date in this table
2. Register coordinator PIC                          -> verify: PIC issued
3. Secure 2 partner entities (3 states total) + LOIs -> verify: signed letters in grants/letters/
4. Draft Part B from eu_horizon_europe_cluster5.md   -> verify: placeholders replaced, page cap met
5. Submit before close                               -> verify: portal submission receipt
```

Reference draft: [eu_horizon_europe_cluster5.md](eu_horizon_europe_cluster5.md) in this directory.
Narrative blocks: [_shared_narrative.md](_shared_narrative.md).
Live numbers: [../report/_generated_tables.md](../report/_generated_tables.md).
