# Bug Triage — Agenda

> Fictional / illustrative template.

**When:** Daily during hardening (15–30 min), weekly otherwise
**Owner:** Program TPM · **Required:** FW lead, QA lead · **Pre-read:** new-bug list since last triage

## Agenda

| Time | Item |
|---|---|
| 0:00–0:05 | P0 check: any new P0? Owner + next-update time assigned immediately |
| 0:05–0:15 | New P1/P2: severity correct? (anyone may raise; lowering needs QA lead) |
| 0:15–0:25 | Stale bugs: P1s open > 1 week — why? Escalate or re-plan |
| 0:25–0:30 | Post-freeze fixes: risk note + verifying test for each cherry-pick |

## Severity SLAs

| Sev | Response | Fix or plan |
|---|---|---|
| P0 | 4 hours | 24h |
| P1 | 1 business day | 1 week |
| P2 | 3 business days | 1 month |
| P3 | Best effort | Backlog |

## Ground rules

- Every bug leaves triage with an **owner** and a **next-update time**.
- After code freeze, each fix needs a written risk note: what could it break,
  and what test proves it doesn't.
- The TPM owns the burn-down chart; a flat P1 curve is a program risk, not
  just a bug list.

## Outputs

- Prioritized bug list with owners, updated burn-down, escalation notes.
