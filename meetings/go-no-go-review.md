# Go / No-Go Review — Agenda

> Fictional / illustrative template. Used at every phase gate; Gate 5
> (production) additionally requires VP Eng + VP Ops sign-off.

**When:** On the gate date (90 min for Gate 5, 45 min otherwise)
**Owner:** Program TPM · **Pre-read:** go/no-go checklist (`artifacts/go-no-go-checklist.md`) with evidence links

## Agenda

| Time | Item |
|---|---|
| 0:00–0:10 | Gate criteria walk-through: entry criteria — met, with evidence? |
| 0:10–0:25 | Exit criteria: can we honestly check each box? |
| 0:25–0:40 | Open risks and known issues: what's shipping *with* the release, and who signed the waiver? |
| 0:40–0:55 | Customer impact review (Gates 4–5): OEM/CSP status, comms ready? |
| 0:55–1:10 | Rollback / contingency: if this goes wrong, what's the first hour look like? |
| 1:10–1:30 | Decision: **GO** / **NO-GO** / **GO with conditions** — recorded with names |

## Ground rules

- The checklist is filled **before** the meeting; the meeting is for judgment,
  not discovery.
- "Go with conditions" must name the conditions, owners, and dates — otherwise
  it's a no-go with better PR.
- A no-go is a successful review if it prevents a bad release. No blame.

## Outputs

- Signed decision (names + date), condition list if any, updated plan of record.
