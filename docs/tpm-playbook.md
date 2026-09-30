# TPM Playbook: Running a Datacenter Firmware/Software Release End to End

> **Fictional / illustrative.** This playbook distills generally-known release
> management practices into one place. It describes no real company's process.

## 1. Release lifecycle

A datacenter FW/SW release moves through five phases. Each phase has entry and
exit criteria — a phase is not "done" because the calendar says so, but because
its exit criteria are met and recorded.

| Phase | Goal | Entry | Exit |
|---|---|---|---|
| **Planning** | Agree what ships and when | Business ask approved; draft scope | Plan of record signed; RACI published |
| **Development** | Build the features | Plan signed; branches cut | Feature complete; code freeze (Gate 1) |
| **Hardening** | Make it shippable | Frozen code; RC1 built | Golden RC declared (Gate 4) |
| **Qualification** | Prove it with customers | Golden RC; qual slots booked | OEM sign-off; CSP pilot green |
| **Deployment** | Roll it out safely | Go decision (Gate 5) | Rollout complete; 30-day review done |

The plan of record (`program/release.yaml` in this repo) is the single source
of truth. Any schedule change greater than one week needs a written proposal
48 hours ahead and VP Engineering approval (see RACI D-09) — never a hallway
agreement.

## 2. Meeting cadence

| Meeting | Cadence | Purpose | Attendees |
|---|---|---|---|
| Weekly program status | Weekly (Thu) | Schedule, risks, gate readiness | All workstream leads, TPM runs it |
| Bug triage | Daily during hardening; weekly otherwise | Prioritize new bugs, assign owners | FW/QA leads, TPM |
| Executive review | Biweekly | Decisions needing VP sign-off, escalations | VP Eng, VP Ops, TPM |
| Go / no-go | Per gate | Formal gate decision | Per RACI (D-08 for production) |
| Post-mortem | Within 2 weeks of release | Blameless review, action items | All leads |

Templates live in `meetings/`. Rules that keep these useful:

- Every meeting has a written agenda beforehand and notes afterward. No agenda,
  no meeting.
- Status meetings are for **decisions and risks**, not round-robin reading of
  slides. Green items get one line; the time goes to red and yellow.
- The TPM publishes notes within 24 hours with owners and due dates. If it
  isn't written down, it didn't happen.

## 3. Status communication

The weekly executive status report (`artifacts/status-report.md`) follows a
fixed shape so executives can skim it in two minutes:

1. **Executive summary** — 3 sentences: are we on track, what changed, what I need.
2. **Accomplishments** — what actually finished (past tense, with dates).
3. **Next 2 weeks** — what's starting, who owns it.
4. **Risks needing executive attention** — top exposures only, with the ask.
5. **Schedule delta** — planned vs forecast, in days. Never hide slip; show it
   with the mitigation.
6. **Gate outlook** — upcoming gates and readiness.

Translate customer requirements into achievable goals internally, then keep
customers updated on issue status in their language: impact, workaround, ETA —
not internal bug IDs.

## 4. Bug triage and SLAs

Severity is defined by **customer impact**, not by who found it:

| Sev | Definition | Response SLA | Fix/plan SLA |
|---|---|---|---|
| P0 | Blocks release or customer deployment | 4 hours | Fix in 24h or same-day plan |
| P1 | Major function broken, workaround exists | 1 business day | Fix within 1 week |
| P2 | Minor / cosmetic, or rare configuration | 3 business days | Fix within 1 month |
| P3 | Nice to have | Best effort | Backlog |

Triage rules:

- Every new P0/P1 gets an owner and a next-update time before the triage ends.
- A bug's severity can only be **lowered** with QA lead agreement; anyone can
  raise it.
- After code freeze, every fix needs a risk note: what could this break, and
  what test proves it doesn't.
- The TPM tracks the burn-down; if P1s aren't closing, that's a program risk,
  not just a bug list.

## 5. Customer release management

Releases go out in rings; each ring gates the next (see "Customer release
rings" in `artifacts/release-plan.md`):

- **Ring 0 — Internal:** lab and dogfood fleets. This is where you find the
  embarrassing bugs. Minimum 72h soak, no P0 for 7 days before promoting.
- **Ring 1 — OEM qualification:** OEM partners run their own qual suites in
  their labs. Give them a single point of contact, a shared issue log, and a
  daily sync during active qual. Their sign-off letter is a formal deliverable.
- **Ring 2 — CSP pilot:** a bounded production fleet (here: 500 nodes).
  Instrument everything first — you cannot debug what you cannot see. Daily
  health reviews with the CSP partner during burn-in.
- **Ring 3 — Production:** only after the Gate 5 go decision, with a tested
  rollback plan. Roll out in waves, never all at once.

Working with customer PMs (OEM/ODM/CSP):

- Acknowledge every customer-reported issue within one business day, even if
  the answer is "investigating, update tomorrow."
- Separate **technical feedback** (goes to engineering, may become a P1) from
  **release-blocking issues** (goes to the TPM immediately).
- Never promise a fix date you haven't confirmed with the owning engineer.

## 6. Risk management

- The risk register is reviewed **weekly**, not filed away. Each risk has one
  owner, a trigger (the observable event that says "this is happening"), a
  mitigation (what we do now), and a contingency (what we do if it happens).
- Score exposure as probability × impact (1–5 each). Anything ≥ 12 gets
  executive visibility.
- Retire risks explicitly when the trigger window passes — a register full of
  stale risks teaches everyone to ignore it.

## 7. Timezone collaboration

With leads in Santa Clara (PT), Taipei (CST), and Hyderabad (IST):

- One standing meeting time that is humane for all three: Thu 18:00 PT /
  Fri 10:00 Taipei / Fri 07:30 IST.
- Async-first for everything else: written proposals 48h ahead, 24h minimum
  sign-off windows so every region gets a business day.
- Record meetings that fall outside someone's daytime; accept async comments
  for 5 business days.
- The emergency lane (hotfix branch decision): page leads directly, decide
  within 4 hours regardless of zone — and write it up immediately after.

## 8. Post-mortem

Within two weeks of production release, run a blameless post-mortem:

1. Timeline of what happened (from the plan of record and status reports).
2. What went well — protect it.
3. What hurt — for each, one owner and one dated action item.
4. Publish the action items; review them at the v2.5.0 kickoff. A post-mortem
   whose actions die in a doc is theater.

---

*Companion files: `meetings/` (agenda templates), `docs/reproduce.md`
(how to run and extend this repo), `artifacts/` (the generated example pack).*
