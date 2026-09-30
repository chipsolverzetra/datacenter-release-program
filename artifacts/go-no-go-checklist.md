# Go / No-Go Checklist — Production Release

> **Fictional / illustrative.** Every box must be checked (or formally waived with VP sign-off) before the Gate 5 go decision.


## G1 — Gate 1 — Code Freeze (2026-10-26)

**Entry criteria**
- [ ] All P0/P1 bugs closed or formally waived
- [ ] Feature branches merged; regression suite green on latest nightly
- [ ] Feature flag inventory reviewed with QA

**Exit criteria**
- [ ] Freeze declared in writing to all workstreams
- [ ] Hotfix-branch policy activated (cherry-pick only, 2 reviewers)
- [ ] RC1 build kicked off

## G2 — Gate 2 — RC1 Ready (2026-11-06)

**Entry criteria**
- [ ] RC1 build passes 24h smoke
- [ ] No new P0 in the preceding 48h

**Exit criteria**
- [ ] RC1 formally handed to QA/Validation
- [ ] Known-issue list published to OEM/CSP partners

## G3 — Gate 3 — RC2 Ready (2026-11-27)

**Entry criteria**
- [ ] All RC1 P0/P1 fixed and verified
- [ ] Regression suite green on RC2

**Exit criteria**
- [ ] RC2 handed to QA and OEM staging
- [ ] Delta release notes published

## G4 — Gate 4 — Release Candidate Sign-off (2026-12-18)

**Entry criteria**
- [ ] PCIe link-training stress sign-off (QA-02)
- [ ] Thermal corner validation pass (HW-03)
- [ ] Security review sign-off memo (FW-05)
- [ ] Telemetry schema v2 live (SW-03)

**Exit criteria**
- [ ] RC declared golden by QA + FW leads
- [ ] OEM qualification (ring 1) and CSP staging (ring 2) unblocked

## G5 — Gate 5 — Production Release (go / no-go) (2027-01-15)

**Entry criteria**
- [ ] OEM sign-off letters received (OEM-03)
- [ ] 14-day CSP burn-in green, zero P0 (CSP-02)
- [ ] Support runbook published; support team trained
- [ ] Rollback plan tested in lab
- [ ] Release notes and errata finalized

**Exit criteria**
- [ ] Go decision recorded with sign-offs (VP Eng, VP Ops)
- [ ] Production rollout (ring 3) begins per rollout plan
- [ ] Customer comms sent to OEM/CSP partners

## Release readiness (Gate 5 addendum)
- [ ] Support runbook published; support team trained (owner: SW lead)
- [ ] Rollback plan tested in lab (owner: FW lead)
- [ ] Release notes and errata finalized (owner: Program TPM)
- [ ] Customer comms sent to OEM/CSP partners (owner: Program TPM)
- [ ] 30-day stability review scheduled (owner: Program TPM)

## Sign-off
- [ ] VP Engineering — go / no-go
- [ ] VP Operations — go / no-go
- [ ] Program TPM — recommendation recorded
