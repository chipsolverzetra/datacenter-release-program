# Reproduce This Project

> Everything here is fictional / illustrative. No real company data is used.

## Prerequisites

- **Python 3.10+** (developed on 3.12)
- **PyYAML** — check with `python3 -c "import yaml"`.
  Install if missing: `pip install pyyaml` (or `apt install python3-yaml`).
- No network access, no other dependencies. The Gantt chart is hand-rolled SVG
  (stdlib only) precisely so the build works offline.

## Build

From the repo root:

```bash
python3 src/build.py
```

Expected output:

```
Loading program/release.yaml ...
Validation passed (12 check groups, 22 milestones, 8 risks, 10 RACI decisions).
Generating artifacts/ ...
  wrote artifacts/release-plan.md
  wrote artifacts/status-report.md
  wrote artifacts/risk-register.md
  wrote artifacts/go-no-go-checklist.md
  wrote artifacts/raci.md
  wrote artifacts/gantt.svg

Done. 6 artifacts generated.
```

The six files in `artifacts/` are regenerated from scratch on every run.

## What the validation checks (12 groups)

| # | Check | Fails the build when… |
|---|---|---|
| 1 | Milestone ids | missing or duplicated |
| 2 | Required fields | `name`, `owner`, `workstream`, `start`, `end` absent |
| 3 | Status values | not one of `done` / `on-track` / `at-risk` |
| 4 | Workstream refs | milestone names a workstream not in `workstreams:` |
| 5 | Owner refs | milestone names a person not in `people:` |
| 6 | Date sanity | unparsable date, or `start` after `end` |
| 7 | Dependency existence | a `dep` id doesn't match any milestone |
| 8 | Dependency cycles | A→B→A (or longer loops) detected by DFS |
| 9 | Dependency ordering | a milestone starts before its dependency ends |
| 10 | Gate criteria | a gate lacks `entry_criteria` or `exit_criteria` |
| 11 | Risk scoring | `probability`/`impact` not ints 1–5, or missing mitigation/contingency/trigger/owner |
| 12 | RACI completeness | missing Responsible or Accountable, or unknown person |

All errors are printed at once (not one-at-a-time), and **no artifacts are
generated** when validation fails — a broken plan must never produce a
pretty-looking pack.

Try it: change a dependency in `program/release.yaml` to a nonsense id, run
`python3 src/build.py`, watch it fail loudly, then revert.

## Verify a clean checkout reproduces identically

```bash
# copy the repo somewhere fresh (or git clone it)
cp -r datacenter-release-program /tmp/repro-check
cd /tmp/repro-check
rm -rf artifacts && mkdir artifacts
python3 src/build.py
# compare against the committed artifacts
diff -r artifacts <original>/artifacts && echo IDENTICAL
```

(The only expected difference: none. Generation is deterministic — no
timestamps or random ids are embedded.)

## Authoring a NEW release program (mini-tutorial)

The whole point of this repo is that the YAML **is** the program. To model
your own release:

1. **Copy** `program/release.yaml` to a backup, then edit the `program:` block:
   name, release, production target, `status_as_of`.
2. **Edit `people:`** — replace the fictional names with roles that match your
   org. Keep the `location` field honest; the RACI timezone notes are generated
   from what you write.
3. **Define `workstreams:`** — 4 to 8 is the sweet spot. Each milestone points
   at exactly one.
4. **Write `milestones:`** — one entry per deliverable or gate:
   - `id`: short, unique, prefixed by workstream (`FW-`, `QA-`…).
   - `type: gate` for phase gates, with `entry_criteria` / `exit_criteria`.
   - `deps`: ids that must finish first. `build.py` enforces finish-to-start.
   - `status`: be honest — `at-risk` items are what make the status report useful.
   - `slip_days`: forecast slip; drives the "Schedule delta" table.
5. **Fill `risks:`** — aim for 6–10. Every risk needs a trigger (observable),
   a mitigation (now), and a contingency (if it happens). Score 1–5.
6. **Fill `raci:`** — one row per real decision, exactly one Accountable each.
7. **Run `python3 src/build.py`** and iterate on validation errors until it
   passes. The errors are the tutorial — read them.
8. **Read the artifacts** with fresh eyes: if the Gantt looks wrong, the plan
   is wrong. Fix the YAML, not the chart.

## Repo map

```
program/release.yaml      the plan of record (edit this)
src/build.py              validate + generate (one command)
src/gantt.py              SVG Gantt renderer (library)
artifacts/                generated pack (committed, view without running)
docs/tpm-playbook.md      how to run a FW/SW release end to end
docs/reproduce.md         this file
meetings/                 agenda templates (status, triage, go/no-go)
README.md                 overview + JD mapping
```
