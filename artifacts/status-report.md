# Weekly Executive Status Report — Meridian MBX-8 BMC Firmware v2.4.0 Release Program

> **Fictional / illustrative.**

**Week of November 16, 2026** (as of 2026-11-20)  |  **Production target:** 2027-01-15  |  **Prepared by:** Program TPM

## Executive summary
The program remains on track for the January 15 production target. Three workstreams carry at-risk items (firmware security review, retimer supply, PCIe stress) with mitigations active and no change to the production date at this time.

## Accomplishments (last 2 weeks)
- **FW-03** RC1 build + smoke test pass — completed 2026-11-06
- **G2** Gate 2 — RC1 Ready — completed 2026-11-06
- **SW-02** In-band update tooling ready — completed 2026-11-13
- **QA-01** Regression suite green on RC1 — completed 2026-11-13
- **HW-03** Thermal corner validation (40C ambient) — completed 2026-11-20

## Next 2 weeks
- **G3** Gate 3 — RC2 Ready — starts 2026-11-27 (owner: R. Okafor)

## Risks needing executive attention
- **R-02** Retimer part supply delay — exposure 16 (P4×I4), owner Wei Chen.
  Mitigation: Dual-source qualification in parallel; expedite fees approved; weekly supplier check-ins
- **R-01** PCIe Gen6 link-training regression on retimer path — exposure 15 (P3×I5), owner L. Gomez.
  Mitigation: Early stress on DVT boards; retimer FW A/B versions in test matrix; weekly link-margin reviews with HW
- **R-03** Security review backlog delays sign-off — exposure 12 (P3×I4), owner D. Kim.
  Mitigation: Pre-review engagement in October; phased submission (threat model first, code second)

## Schedule delta
| ID | Milestone | Planned end | Slip (days) | Forecast end | Impact |
| --- | --- | --- | --- | --- | --- |
| FW-05 | Security review sign-off | 2026-12-04 | 5 | 2026-12-09 | Absorbed by buffer; production date unchanged |
| HW-02 | Retimer parts allocation confirmed | 2026-10-30 | 7 | 2026-11-06 | Absorbed by buffer; production date unchanged |
| QA-02 | PCIe link-training stress sign-off | 2026-12-04 | 4 | 2026-12-08 | Absorbed by buffer; production date unchanged |

## Gate outlook
- **G3** Gate 3 — RC2 Ready — 2026-11-27 (status: on-track; entry criteria: 2, exit criteria: 2)
- **G4** Gate 4 — Release Candidate Sign-off — 2026-12-18 (status: on-track; entry criteria: 4, exit criteria: 2)
- **G5** Gate 5 — Production Release (go / no-go) — 2027-01-15 (status: on-track; entry criteria: 5, exit criteria: 3)

## Asks of leadership
- None this week. FYI: security-review escalation path (R-03) is armed if the review has not started by Nov 16.
