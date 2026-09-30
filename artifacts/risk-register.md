# Risk Register

> **Fictional / illustrative.** Exposure = probability × impact (1–5 each).

| ID | Risk | WS | P | I | Exposure | Owner | Trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-02 | Retimer part supply delay | HW | 4 | 4 | 16 | Wei Chen | Supplier misses Oct 30 allocation commit |
| R-01 | PCIe Gen6 link-training regression on retimer path | QA | 3 | 5 | 15 | L. Gomez | >2% link-down events in 10k-cycle stress run |
| R-03 | Security review backlog delays sign-off | FW | 3 | 4 | 12 | D. Kim | Review not started by Nov 16 |
| R-04 | OEM qual slot slip | OEM | 3 | 4 | 12 | J. Park | Slot not confirmed by Oct 30 |
| R-05 | Thermal corner failure at 40C ambient | HW | 2 | 5 | 10 | Wei Chen | Any hotspot exceeds spec in DVT thermal runs |
| R-06 | In-band update tooling failure at fleet scale | SW | 2 | 5 | 10 | Arjun Rao | Update failure rate >0.5% on 2k-node dogfood fleet |
| R-07 | CSP pilot surfaces scale-dependent bug | CSP | 3 | 3 | 9 | S. Iyer | Crash signature repeats on >5 pilot nodes |
| R-08 | Holiday coverage gap (Dec 24 - Jan 2) | FW | 2 | 3 | 6 | R. Okafor | Coverage roster shows single point of failure in any workstream |


## R-02 — Retimer part supply delay
**Exposure:** 16 (P4 × I4) · **Owner:** Wei Chen (Hardware Lead, Taipei (CST, UTC+8)) · **Status:** open
- **Trigger:** Supplier misses Oct 30 allocation commit
- **Mitigation:** Dual-source qualification in parallel; expedite fees approved; weekly supplier check-ins
- **Contingency:** Descope to validated alternate retimer; accept 2-week DVT slip

## R-01 — PCIe Gen6 link-training regression on retimer path
**Exposure:** 15 (P3 × I5) · **Owner:** L. Gomez (QA / Validation Lead, Santa Clara (PT, UTC-8)) · **Status:** open
- **Trigger:** >2% link-down events in 10k-cycle stress run
- **Mitigation:** Early stress on DVT boards; retimer FW A/B versions in test matrix; weekly link-margin reviews with HW
- **Contingency:** Cap link speed to Gen5 for affected configs; respin schedule +2 weeks

## R-03 — Security review backlog delays sign-off
**Exposure:** 12 (P3 × I4) · **Owner:** D. Kim (Security Architect, Santa Clara (PT, UTC-8)) · **Status:** open
- **Trigger:** Review not started by Nov 16
- **Mitigation:** Pre-review engagement in October; phased submission (threat model first, code second)
- **Contingency:** Executive escalation to CISO; time-boxed conditional sign-off with follow-ups

## R-04 — OEM qual slot slip
**Exposure:** 12 (P3 × I4) · **Owner:** J. Park (OEM Enablement Lead, Taipei (CST, UTC+8)) · **Status:** open
- **Trigger:** Slot not confirmed by Oct 30
- **Mitigation:** Slots booked early with backup dates; shared test plan reduces on-site time
- **Contingency:** Compress pilot by 1 week; run OEM-B qual in parallel with CSP staging

## R-05 — Thermal corner failure at 40C ambient
**Exposure:** 10 (P2 × I5) · **Owner:** Wei Chen (Hardware Lead, Taipei (CST, UTC+8)) · **Status:** open
- **Trigger:** Any hotspot exceeds spec in DVT thermal runs
- **Mitigation:** Early CFD modeling; fan curve v3 validated ahead of DVT; margin added to heatsink spec
- **Contingency:** Revised fan curve + targeted airflow shrouds; schedule thermal re-test sprint

## R-06 — In-band update tooling failure at fleet scale
**Exposure:** 10 (P2 × I5) · **Owner:** Arjun Rao (System Software Lead, Hyderabad (IST, UTC+5:30)) · **Status:** open
- **Trigger:** Update failure rate >0.5% on 2k-node dogfood fleet
- **Mitigation:** Canary rollout (50 -> 500 -> 2000 nodes); idempotent update design; dry-run mode
- **Contingency:** Fall back to out-of-band update path; hotfix tooling in 1-week sprint

## R-07 — CSP pilot surfaces scale-dependent bug
**Exposure:** 9 (P3 × I3) · **Owner:** S. Iyer (CSP Deployment Lead, Hyderabad (IST, UTC+5:30)) · **Status:** open
- **Trigger:** Crash signature repeats on >5 pilot nodes
- **Mitigation:** 14-day burn-in with full telemetry; daily pilot health reviews with CSP partner
- **Contingency:** Hotfix branch from golden RC; targeted patch release to pilot only

## R-08 — Holiday coverage gap (Dec 24 - Jan 2)
**Exposure:** 6 (P2 × I3) · **Owner:** R. Okafor (Program TPM, Santa Clara (PT, UTC-8)) · **Status:** open
- **Trigger:** Coverage roster shows single point of failure in any workstream
- **Mitigation:** Coverage roster published Dec 1; on-call pairs across time zones; freeze non-urgent changes
- **Contingency:** Contractor backfill for critical roles; defer non-blocking work to January
