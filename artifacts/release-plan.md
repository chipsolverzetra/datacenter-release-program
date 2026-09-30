# Release Plan — Meridian MBX-8 BMC Firmware v2.4.0 Release Program

> **Fictional / illustrative.** All vendors, products, people, dates, and events are invented for demonstration. Not affiliated with any real company.

**Release:** BMC firmware v2.4.0  |  **Production target:** 2027-01-15  |  **Plan version:** 1.3  |  **Status as of:** 2026-11-20

## Objectives
- Ship BMC firmware v2.4.0 to production on 2027-01-15 with zero P0 defects
- Complete OEM qualification with two OEM partners and a 500-node CSP pilot burn-in
- Close all security review findings before Gate 4
- Demonstrate a repeatable release process reusable for v2.5.0

## Scope

### In scope
- BMC firmware v2.4.0 for the MBX-8 baseboard
- In-band update tooling and telemetry schema v2
- OEM qualification support and CSP pilot deployment
- Release documentation, runbooks, and rollback plan

### Out of scope
- Next-gen baseboard hardware (out of scope for this release)
- Host driver feature development beyond the frozen interface spec
- Data-center network / fabric firmware

## Phases and milestones

### Firmware

| ID | Milestone | Type | Start | End | Owner | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FW-01 | Feature complete — all v2.4.0 commits landed | milestone | 2026-10-05 | 2026-10-23 | A. Sharma | done | — |
| G1 | Gate 1 — Code Freeze | 🔶 gate | 2026-10-26 | 2026-10-26 | R. Okafor | done | FW-01 |
| FW-03 | RC1 build + smoke test pass | milestone | 2026-10-27 | 2026-11-06 | A. Sharma | done | G1 |
| G2 | Gate 2 — RC1 Ready | 🔶 gate | 2026-11-06 | 2026-11-06 | R. Okafor | done | FW-03 |
| FW-04 | RC2 build with regression fixes | milestone | 2026-11-16 | 2026-11-27 | A. Sharma | on-track | FW-03, QA-01 |
| G3 | Gate 3 — RC2 Ready | 🔶 gate | 2026-11-27 | 2026-11-27 | R. Okafor | on-track | FW-04 |
| FW-05 | Security review sign-off | milestone | 2026-11-09 | 2026-12-04 | D. Kim | at-risk | G1 |

### Hardware

| ID | Milestone | Type | Start | End | Owner | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HW-01 | DVT board bring-up complete | milestone | 2026-09-14 | 2026-10-09 | Wei Chen | done | — |
| HW-02 | Retimer parts allocation confirmed | milestone | 2026-10-12 | 2026-10-30 | Wei Chen | at-risk | — |
| HW-03 | Thermal corner validation (40C ambient) | milestone | 2026-11-02 | 2026-11-20 | Wei Chen | done | HW-02 |

### System Software

| ID | Milestone | Type | Start | End | Owner | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SW-01 | Driver/FW interface spec frozen | milestone | 2026-10-05 | 2026-10-16 | Arjun Rao | done | — |
| SW-02 | In-band update tooling ready | milestone | 2026-10-19 | 2026-11-13 | Arjun Rao | done | SW-01 |
| SW-03 | Telemetry schema v2 rollout | milestone | 2026-11-16 | 2026-12-11 | Arjun Rao | on-track | FW-03 |

### QA / Validation

| ID | Milestone | Type | Start | End | Owner | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QA-01 | Regression suite green on RC1 | milestone | 2026-11-09 | 2026-11-13 | L. Gomez | done | FW-03 |
| QA-02 | PCIe link-training stress sign-off | milestone | 2026-11-16 | 2026-12-04 | L. Gomez | at-risk | QA-01 |
| G4 | Gate 4 — Release Candidate Sign-off | 🔶 gate | 2026-12-18 | 2026-12-18 | R. Okafor | on-track | FW-04, FW-05, QA-02, HW-03 |

### OEM Enablement

| ID | Milestone | Type | Start | End | Owner | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OEM-01 | OEM qual slots booked (2 OEMs) | milestone | 2026-10-19 | 2026-10-30 | J. Park | done | — |
| OEM-02 | OEM qualification testing (ring 1) | milestone | 2026-12-21 | 2027-01-08 | J. Park | on-track | G4 |
| OEM-03 | OEM sign-off received | milestone | 2027-01-11 | 2027-01-11 | J. Park | on-track | OEM-02 |

### CSP Deployment

| ID | Milestone | Type | Start | End | Owner | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CSP-01 | CSP pilot fleet staged (ring 2) | milestone | 2026-12-21 | 2026-12-29 | S. Iyer | on-track | G4 |
| CSP-02 | CSP pilot burn-in, 14 days (ring 2) | milestone | 2026-12-30 | 2027-01-12 | S. Iyer | on-track | CSP-01 |
| G5 | Gate 5 — Production Release (go / no-go) | 🔶 gate | 2027-01-15 | 2027-01-15 | R. Okafor | on-track | OEM-03, CSP-02 |

## Phase gates

| Gate | Name | Date | Status | Entry criteria (summary) |
| --- | --- | --- | --- | --- |
| G1 | Gate 1 — Code Freeze | 2026-10-26 | done | All P0/P1 bugs closed or formally waived; Feature branches merged; regression suite green on latest nightly… |
| G2 | Gate 2 — RC1 Ready | 2026-11-06 | done | RC1 build passes 24h smoke; No new P0 in the preceding 48h… |
| G3 | Gate 3 — RC2 Ready | 2026-11-27 | on-track | All RC1 P0/P1 fixed and verified; Regression suite green on RC2… |
| G4 | Gate 4 — Release Candidate Sign-off | 2026-12-18 | on-track | PCIe link-training stress sign-off (QA-02); Thermal corner validation pass (HW-03)… |
| G5 | Gate 5 — Production Release (go / no-go) | 2027-01-15 | on-track | OEM sign-off letters received (OEM-03); 14-day CSP burn-in green, zero P0 (CSP-02)… |

## Customer release rings

### Ring 0 — Internal
Scope: Lab fleets + internal dogfood (~2,000 nodes)

**Entry:** RC1 smoke pass complete; 24h soak green

**Exit:** 72h soak green; No P0 for 7 days

### Ring 1 — OEM Qualification
Scope: Two OEM partners' qual labs

**Entry:** Gate 4 sign-off; OEM test plan exchanged

**Exit:** OEM qual reports clean; Written OEM sign-off

### Ring 2 — CSP Pilot
Scope: 500-node pilot fleet at CSP partner

**Entry:** Gate 4 sign-off; Fleet staged and healthy

**Exit:** 14-day burn-in green; Zero P0, telemetry baseline captured

### Ring 3 — Production
Scope: Full fleet rollout per rollout plan

**Entry:** Gate 5 go decision; Rollback plan tested

**Exit:** Rollout complete; 30-day stability review scheduled

## Key contacts

| Role | Name | Location |
| --- | --- | --- |
| Program TPM | R. Okafor | Santa Clara (PT, UTC-8) |
| Firmware Lead | A. Sharma | Santa Clara (PT, UTC-8) |
| Hardware Lead | Wei Chen | Taipei (CST, UTC+8) |
| System Software Lead | Arjun Rao | Hyderabad (IST, UTC+5:30) |
| QA / Validation Lead | L. Gomez | Santa Clara (PT, UTC-8) |
| OEM Enablement Lead | J. Park | Taipei (CST, UTC+8) |
| CSP Deployment Lead | S. Iyer | Hyderabad (IST, UTC+5:30) |
| Security Architect | D. Kim | Santa Clara (PT, UTC-8) |
| VP Engineering | M. Alvarez | Santa Clara (PT, UTC-8) |
| VP Operations | T. Nguyen | Santa Clara (PT, UTC-8) |
