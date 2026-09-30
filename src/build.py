#!/usr/bin/env python3
"""build.py — validate program/release.yaml and generate the TPM artifact pack.

Usage:
    python3 src/build.py            # run from the repo root

What it does:
    1. Loads program/release.yaml (the plan of record).
    2. Validates it — duplicate ids, date sanity, dependency existence,
       dependency cycles, dependency ordering, gate criteria, risk scoring,
       RACI completeness. Prints EVERY problem found and exits non-zero
       if any exist (fail loudly; never generate from a broken plan).
    3. Generates artifacts/release-plan.md, status-report.md, risk-register.md,
       go-no-go-checklist.md, raci.md and artifacts/gantt.svg.

Only the standard library + PyYAML are used.
"""

import datetime
import os
import sys

import yaml

# Import the sibling chart module regardless of how this script is invoked.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gantt import render_gantt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM_FILE = os.path.join(ROOT, "program", "release.yaml")
ARTIFACTS = os.path.join(ROOT, "artifacts")

VALID_STATUSES = {"done", "on-track", "at-risk"}


# ------------------------------------------------------------------ loading
def load_program():
    """Load the YAML plan of record."""
    with open(PROGRAM_FILE) as f:
        data = yaml.safe_load(f)
    return data


def parse_date(value, where):
    """Parse an ISO date string; raise a helpful error on failure."""
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        raise ValueError(f"{where}: bad date {value!r} (expected YYYY-MM-DD)")


# --------------------------------------------------------------- validation
class ValidationError(Exception):
    """Collects every problem so the author can fix them in one pass."""


def validate(data):
    """Return (milestones, errors). milestones have parsed date objects."""
    errors = []
    milestones = data.get("milestones", [])
    seen = {}
    for m in milestones:
        mid = m.get("id")
        if not mid:
            errors.append("milestone missing 'id': %r" % (m.get("name"),))
            continue
        if mid in seen:
            errors.append(f"duplicate milestone id: {mid}")
        seen[mid] = m

    # Required fields + date sanity.
    for m in milestones:
        mid = m.get("id", "?")
        for field in ("name", "owner", "workstream", "start", "end"):
            if field not in m:
                errors.append(f"{mid}: missing required field '{field}'")
        if m.get("status") not in VALID_STATUSES:
            errors.append(f"{mid}: bad status {m.get('status')!r} "
                          f"(expected one of {sorted(VALID_STATUSES)})")
        if m.get("workstream") not in {w["id"] for w in data.get("workstreams", [])}:
            errors.append(f"{mid}: unknown workstream {m.get('workstream')!r}")
        if m.get("owner") not in data.get("people", {}):
            errors.append(f"{mid}: unknown owner {m.get('owner')!r}")
        try:
            m["_start"] = parse_date(m["start"], mid)
            m["_end"] = parse_date(m["end"], mid)
            if m["_start"] > m["_end"]:
                errors.append(f"{mid}: start {m['start']} is after end {m['end']}")
        except (ValueError, KeyError) as e:
            errors.append(str(e))
        m.setdefault("deps", [])
        m.setdefault("type", "milestone")
        m.setdefault("slip_days", 0)

    # Dependencies: existence + no cycles + ordering.
    for m in milestones:
        for dep in m["deps"]:
            if dep not in seen:
                errors.append(f"{m['id']}: depends on unknown id {dep!r}")

    # Cycle detection via DFS.
    visiting, visited, cycle = set(), set(), []

    def dfs(node, path):
        if node in visiting:
            cycle.append(path[path.index(node):] + [node])
            return
        if node in visited or node not in seen:
            return
        visiting.add(node)
        for dep in seen[node]["deps"]:
            dfs(dep, path + [dep])
        visiting.discard(node)
        visited.add(node)

    for m in milestones:
        dfs(m["id"], [m["id"]])
    for c in cycle:
        errors.append("dependency cycle: " + " -> ".join(c))

    # A dependency must finish on or before the dependent starts.
    for m in milestones:
        for dep in m["deps"]:
            if dep in seen and "_end" in seen[dep] and "_start" in m:
                if seen[dep]["_end"] > m["_start"]:
                    errors.append(
                        f"{m['id']}: starts {m['start']} before dependency "
                        f"{dep} ends {seen[dep]['end']}")

    # Gates need entry and exit criteria.
    for m in milestones:
        if m["type"] == "gate":
            for crit in ("entry_criteria", "exit_criteria"):
                if not m.get(crit):
                    errors.append(f"gate {m['id']}: missing '{crit}'")

    # Risks: 1-5 scoring + required fields.
    for r in data.get("risks", []):
        rid = r.get("id", "?")
        for field in ("title", "owner", "mitigation", "contingency", "trigger"):
            if not r.get(field):
                errors.append(f"risk {rid}: missing '{field}'")
        for field in ("probability", "impact"):
            v = r.get(field)
            if not isinstance(v, int) or not 1 <= v <= 5:
                errors.append(f"risk {rid}: {field} must be an int 1-5, got {v!r}")

    # RACI: exactly one Accountable, one Responsible, unique decision ids.
    raci_ids = set()
    for rc in data.get("raci", []):
        rid = rc.get("id", "?")
        if rid in raci_ids:
            errors.append(f"duplicate RACI id: {rid}")
        raci_ids.add(rid)
        if not rc.get("R"):
            errors.append(f"RACI {rid}: no one Responsible")
        if not rc.get("A"):
            errors.append(f"RACI {rid}: no one Accountable")
        for role_key in ("R", "A"):
            if rc.get(role_key) not in data.get("people", {}):
                errors.append(f"RACI {rid}: unknown person {rc.get(role_key)!r}")

    return milestones, errors


# ----------------------------------------------------------------- markdown
def person(data, key):
    p = data["people"][key]
    return f"{p['name']} ({p['role']}, {p['location']})"


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def write(path, text):
    with open(path, "w") as f:
        f.write(text)
    print(f"  wrote {os.path.relpath(path, ROOT)}")


# ------------------------------------------------------------- artifact: plan
def gen_release_plan(data, milestones):
    p = data["program"]
    L = [f"# Release Plan — {p['name']}",
         "",
         "> **Fictional / illustrative.** All vendors, products, people, dates, and "
         "events are invented for demonstration. Not affiliated with any real company.",
         "",
         f"**Release:** {p['release']}  |  **Production target:** {p['production_target']}  "
         f"|  **Plan version:** {p['plan_of_record_version']}  |  **Status as of:** {p['status_as_of']}",
         "",
         "## Objectives"]
    L += [f"- {o}" for o in data["objectives"]]
    L += ["", "## Scope", "", "### In scope"]
    L += [f"- {s}" for s in data["scope_in"]]
    L += ["", "### Out of scope"]
    L += [f"- {s}" for s in data["scope_out"]]
    L += ["", "## Phases and milestones"]
    for w in data["workstreams"]:
        rows = []
        for m in milestones:
            if m["workstream"] != w["id"]:
                continue
            kind = "🔶 gate" if m["type"] == "gate" else "milestone"
            deps = ", ".join(m["deps"]) if m["deps"] else "—"
            rows.append([m["id"], m["name"], kind, m["start"], m["end"],
                         person(data, m["owner"]).split(" (")[0], m["status"], deps])
        L += ["", f"### {w['name']}",
              "",
              md_table(["ID", "Milestone", "Type", "Start", "End", "Owner",
                        "Status", "Depends on"], rows)]
    L += ["", "## Phase gates"]
    rows = []
    for m in milestones:
        if m["type"] == "gate":
            rows.append([m["id"], m["name"], m["end"], m["status"],
                         "; ".join(m["entry_criteria"][:2]) + "…"])
    L += ["", md_table(["Gate", "Name", "Date", "Status", "Entry criteria (summary)"], rows),
          "",
          "## Customer release rings"]
    for r in data["release_rings"]:
        L += ["", f"### Ring {r['ring']} — {r['name']}",
              f"Scope: {r['scope']}",
              "", "**Entry:** " + "; ".join(r["entry"]),
              "", "**Exit:** " + "; ".join(r["exit"])]
    L += ["", "## Key contacts",
          "",
          md_table(["Role", "Name", "Location"],
                   [[data["people"][k]["role"], data["people"][k]["name"],
                     data["people"][k]["location"]] for k in data["people"]])]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------- artifact: status
def gen_status_report(data, milestones):
    p = data["program"]
    as_of = datetime.date.fromisoformat(p["status_as_of"])
    L = [f"# Weekly Executive Status Report — {p['name']}",
         "",
         "> **Fictional / illustrative.**",
         "",
         f"**{p['report_week']}** (as of {p['status_as_of']})  |  "
         f"**Production target:** {p['production_target']}  |  **Prepared by:** Program TPM",
         "",
         "## Executive summary",
         "The program remains on track for the January 15 production target. "
         "Three workstreams carry at-risk items (firmware security review, retimer "
         "supply, PCIe stress) with mitigations active and no change to the "
         "production date at this time.",
         "",
         "## Accomplishments (last 2 weeks)"]
    for m in sorted(milestones, key=lambda m: m["_end"]):
        if m["status"] == "done" and as_of - datetime.timedelta(days=14) <= m["_end"] <= as_of:
            L.append(f"- **{m['id']}** {m['name']} — completed {m['end']}")
    L += ["", "## Next 2 weeks"]
    for m in sorted(milestones, key=lambda m: m["_start"]):
        if as_of < m["_start"] <= as_of + datetime.timedelta(days=14):
            L.append(f"- **{m['id']}** {m['name']} — starts {m['start']} "
                     f"(owner: {data['people'][m['owner']]['name']})")
    L += ["", "## Risks needing executive attention"]
    top = sorted(data["risks"], key=lambda r: r["probability"] * r["impact"], reverse=True)[:3]
    for r in top:
        exp = r["probability"] * r["impact"]
        L += [f"- **{r['id']}** {r['title']} — exposure {exp} "
              f"(P{r['probability']}×I{r['impact']}), owner {data['people'][r['owner']]['name']}.",
              f"  Mitigation: {r['mitigation']}"]
    L += ["", "## Schedule delta"]
    slipped = [m for m in milestones if m["slip_days"] > 0]
    if slipped:
        L.append(md_table(
            ["ID", "Milestone", "Planned end", "Slip (days)", "Forecast end", "Impact"],
            [[m["id"], m["name"], m["end"], m["slip_days"],
              (m["_end"] + datetime.timedelta(days=m["slip_days"])).isoformat(),
              "Absorbed by buffer; production date unchanged"] for m in slipped]))
    else:
        L.append("No forecast slips this week.")
    L += ["", "## Gate outlook"]
    for m in sorted(milestones, key=lambda m: m["_start"]):
        if m["type"] == "gate" and m["_start"] > as_of:
            L.append(f"- **{m['id']}** {m['name']} — {m['start']} "
                     f"(status: {m['status']}; entry criteria: {len(m['entry_criteria'])}, "
                     f"exit criteria: {len(m['exit_criteria'])})")
    L += ["", "## Asks of leadership",
          "- None this week. FYI: security-review escalation path (R-03) is armed "
          "if the review has not started by Nov 16."]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------- artifact: risk
def gen_risk_register(data):
    L = ["# Risk Register",
         "",
         "> **Fictional / illustrative.** Exposure = probability × impact (1–5 each).",
         "",
         md_table(["ID", "Risk", "WS", "P", "I", "Exposure", "Owner", "Trigger"],
                  [[r["id"], r["title"], r["workstream"], r["probability"],
                    r["impact"], r["probability"] * r["impact"],
                    data["people"][r["owner"]]["name"], r["trigger"]]
                   for r in sorted(data["risks"],
                                   key=lambda r: r["probability"] * r["impact"],
                                   reverse=True)]),
         ""]
    for r in sorted(data["risks"], key=lambda r: r["probability"] * r["impact"], reverse=True):
        L += ["", f"## {r['id']} — {r['title']}",
              f"**Exposure:** {r['probability'] * r['impact']} "
              f"(P{r['probability']} × I{r['impact']}) · "
              f"**Owner:** {person(data, r['owner'])} · **Status:** {r['status']}",
              f"- **Trigger:** {r['trigger']}",
              f"- **Mitigation:** {r['mitigation']}",
              f"- **Contingency:** {r['contingency']}"]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------- artifact: go-no-go
def gen_go_no_go(data, milestones):
    L = ["# Go / No-Go Checklist — Production Release",
         "",
         "> **Fictional / illustrative.** Every box must be checked (or formally "
         "waived with VP sign-off) before the Gate 5 go decision.",
         ""]
    for m in sorted([m for m in milestones if m["type"] == "gate"],
                    key=lambda m: m["_start"]):
        L += ["", f"## {m['id']} — {m['name']} ({m['end']})",
              "", "**Entry criteria**"]
        L += [f"- [ ] {c}" for c in m["entry_criteria"]]
        L += ["", "**Exit criteria**"]
        L += [f"- [ ] {c}" for c in m["exit_criteria"]]
    L += ["", "## Release readiness (Gate 5 addendum)",
          "- [ ] Support runbook published; support team trained (owner: SW lead)",
          "- [ ] Rollback plan tested in lab (owner: FW lead)",
          "- [ ] Release notes and errata finalized (owner: Program TPM)",
          "- [ ] Customer comms sent to OEM/CSP partners (owner: Program TPM)",
          "- [ ] 30-day stability review scheduled (owner: Program TPM)",
          "",
          "## Sign-off",
          "- [ ] VP Engineering — go / no-go",
          "- [ ] VP Operations — go / no-go",
          "- [ ] Program TPM — recommendation recorded"]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------- artifact: raci
def gen_raci(data):
    L = ["# RACI — Key Program Decisions",
         "",
         "> **Fictional / illustrative.** R = Responsible (does the work), "
         "A = Accountable (exactly one — makes the call), C = Consulted, I = Informed.",
         "",
         md_table(["ID", "Decision", "Due", "R", "A", "C", "I", "Timezone note"],
                  [[rc["id"], rc["decision"], rc["due"],
                    data["people"][rc["R"]]["name"], data["people"][rc["A"]]["name"],
                    ", ".join(data["people"][c]["name"] for c in rc.get("C", [])),
                    ", ".join(data["people"][i]["name"] for i in rc.get("I", [])),
                    rc["timezone_note"]] for rc in data["raci"]]),
         "",
         "## Timezone norms",
         "- Santa Clara PT (UTC-8) · Taipei CST (UTC+8) · Hyderabad IST (UTC+5:30).",
         "- The standing program review is Thu 18:00 PT / Fri 10:00 Taipei / Fri 07:30 IST — "
         "US evening, Asia morning, so nobody is routinely on call past midnight.",
         "- Async sign-off windows are 24h minimum so every region gets a business day.",
         "- Emergency lane (D-07 hotfix branch): the TPM pages leads directly; "
         "decision within 4 hours regardless of time zone."]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------- main
def main():
    print(f"Loading {os.path.relpath(PROGRAM_FILE, ROOT)} ...")
    try:
        data = load_program()
    except FileNotFoundError:
        print(f"ERROR: plan of record not found: {PROGRAM_FILE}")
        return 1
    except yaml.YAMLError as e:
        print(f"ERROR: invalid YAML: {e}")
        return 1

    milestones, errors = validate(data)
    n_checks = 12  # validation rule groups implemented above
    if errors:
        print(f"\nVALIDATION FAILED — {len(errors)} problem(s) "
              f"({n_checks} check groups run):")
        for e in errors:
            print(f"  ✗ {e}")
        print("\nFix program/release.yaml and re-run. No artifacts were generated.")
        return 1
    print(f"Validation passed ({n_checks} check groups, "
          f"{len(milestones)} milestones, {len(data.get('risks', []))} risks, "
          f"{len(data.get('raci', []))} RACI decisions).")

    os.makedirs(ARTIFACTS, exist_ok=True)
    print("Generating artifacts/ ...")
    write(os.path.join(ARTIFACTS, "release-plan.md"), gen_release_plan(data, milestones))
    write(os.path.join(ARTIFACTS, "status-report.md"), gen_status_report(data, milestones))
    write(os.path.join(ARTIFACTS, "risk-register.md"), gen_risk_register(data))
    write(os.path.join(ARTIFACTS, "go-no-go-checklist.md"), gen_go_no_go(data, milestones))
    write(os.path.join(ARTIFACTS, "raci.md"), gen_raci(data))

    as_of = datetime.date.fromisoformat(data["program"]["status_as_of"])
    svg_path = os.path.join(ARTIFACTS, "gantt.svg")
    render_gantt(milestones, data["workstreams"], as_of,
                 data["program"]["name"], svg_path)
    print(f"  wrote {os.path.relpath(svg_path, ROOT)}")
    print("\nDone. 6 artifacts generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
