# Datacenter Release Program — in a Box

> **Fictional / illustrative.** This repo models a complete firmware release
> program for an invented vendor ("Meridian Compute"), an invented product
> ("MBX-8 baseboard"), and invented people, dates, and events. It demonstrates
> technical program management artifacts and is not affiliated with any real
> company, product, or employer.

A single YAML file is the **plan of record** for a fictional BMC firmware
v2.4.0 release (Oct 2026 → Jan 2027, production target 2027-01-15). One command
validates the plan and generates the full TPM artifact pack: release plan,
executive status report, risk register, go/no-go checklist, RACI, and a Gantt
chart.

## Quickstart

```bash
python3 src/build.py
```

Requires Python 3.10+ and PyYAML (`pip install pyyaml`). No network, no other
dependencies. Generated files land in `artifacts/`:

| Artifact | What it is |
|---|---|
| `artifacts/release-plan.md` | Plan of record in prose: objectives, scope, milestones, gates, rings |
| `artifacts/status-report.md` | Weekly executive status report generated from the data |
| `artifacts/risk-register.md` | Risks scored by exposure (P×I), with mitigations |
| `artifacts/go-no-go-checklist.md` | Release readiness checklist with sign-off owners |
| `artifacts/raci.md` | RACI table with explicit timezone handling |
| `artifacts/gantt.svg` | Gantt: swimlanes, dependencies, gates, today-line, at-risk highlights |

Validation runs first and **fails loudly** — 12 check groups covering duplicate
ids, date sanity, dependency existence/cycles/ordering, gate criteria, risk
scoring, and RACI completeness. No artifacts are generated from a broken plan.

## Repo map

```
program/release.yaml      the plan of record — edit this to model a new release
src/build.py              one-command validate + generate
src/gantt.py              stdlib-only SVG Gantt renderer
artifacts/                generated pack (committed — viewable without running)
docs/tpm-playbook.md      how to run a datacenter FW/SW release end to end
docs/reproduce.md         reproduction steps + mini-tutorial for new programs
meetings/                 agenda templates: status, bug triage, go/no-go
```

## How this maps to a TPM job description

For a Technical Program Manager role leading datacenter SW/firmware execution
(release schedules, executive updates, cross-functional coordination, customer
releases, process documentation):

| JD ask | Where it's demonstrated |
|---|---|
| Drive release schedules and plans | `program/release.yaml` + `artifacts/gantt.svg` + `release-plan.md` |
| Executive status updates | `artifacts/status-report.md` (generated weekly format) |
| Schedule and lead status meetings | `meetings/weekly-program-status.md`, `meetings/go-no-go-review.md` |
| Coordinate HW / FW / SW across time zones | 6 workstreams, RACI with PT/CST/IST handling (`artifacts/raci.md`) |
| Manage customer releases (OEM/CSP) | Release rings 0–3, OEM qual + CSP pilot milestones, go/no-go gates |
| Drive process documentation | `docs/tpm-playbook.md` (lifecycle, SLAs, risk, post-mortem) |
| Bug triage and issue management | `meetings/bug-triage.md`, P0–P3 SLAs in the playbook |
| Translate customer requirements into goals | Rings' entry/exit criteria; customer comms norms in the playbook |
| Risk management | `artifacts/risk-register.md` — 8 risks, exposure scoring, triggers |

## Reproduce / extend

See [`docs/reproduce.md`](docs/reproduce.md) for exact steps, the validation
checklist, a clean-checkout determinism test, and a mini-tutorial for authoring
a new release program from the YAML.
