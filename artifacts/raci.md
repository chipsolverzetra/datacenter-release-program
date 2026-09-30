# RACI — Key Program Decisions

> **Fictional / illustrative.** R = Responsible (does the work), A = Accountable (exactly one — makes the call), C = Consulted, I = Informed.

| ID | Decision | Due | R | A | C | I | Timezone note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-01 | Approve code-freeze scope | 2026-10-23 | A. Sharma | R. Okafor | L. Gomez, Wei Chen | J. Park, S. Iyer | Decided at weekly program review Thu 18:00 PT / Fri 10:00 Taipei / Fri 07:30 IST |
| D-02 | Accept RC1 into validation | 2026-11-06 | L. Gomez | R. Okafor | A. Sharma | Arjun Rao, J. Park | Async sign-off in release tracker; 24h window covers all zones |
| D-03 | Grant security-review exception or deferral | 2026-12-04 | D. Kim | M. Alvarez | A. Sharma | R. Okafor, L. Gomez | Escalation review Tue 09:00 PT / 17:00 Taipei / 22:30 IST (recorded for Hyderabad) |
| D-04 | Approve thermal spec waiver | 2026-11-20 | Wei Chen | M. Alvarez | L. Gomez | J. Park, R. Okafor | HW review Wed 17:00 PT / Thu 09:00 Taipei / Thu 06:30 IST |
| D-05 | Enter OEM qualification (ring 1) | 2026-12-18 | J. Park | R. Okafor | L. Gomez | S. Iyer, Arjun Rao | Part of Gate 4 sign-off meeting; OEM partners join async via written sign-off |
| D-06 | Expand CSP pilot fleet | 2026-12-29 | S. Iyer | R. Okafor | Arjun Rao | A. Sharma, L. Gomez | Daily pilot standup 18:30 PT / 10:30 Taipei / 08:00 IST during burn-in |
| D-07 | Cut hotfix branch from golden RC | as needed | A. Sharma | R. Okafor | L. Gomez | J. Park, S. Iyer, Arjun Rao, Wei Chen | Emergency lane: TPM pages leads; decision within 4h regardless of zone |
| D-08 | Production go / no-go | 2027-01-15 | R. Okafor | M. Alvarez | A. Sharma, Wei Chen, Arjun Rao, L. Gomez, J. Park, S. Iyer | T. Nguyen | Go/no-go review Thu 17:00 PT / Fri 09:00 Taipei / Fri 06:30 IST; VP Ops co-signs |
| D-09 | Approve schedule change greater than 1 week | as needed | R. Okafor | M. Alvarez | A. Sharma, Wei Chen, Arjun Rao, L. Gomez, J. Park, S. Iyer | T. Nguyen | Exec review slot; written proposal 48h ahead so Taipei/Hyderabad can comment async |
| D-10 | Publish post-mortem action items | 2027-02-12 | R. Okafor | M. Alvarez | A. Sharma, Wei Chen, Arjun Rao, L. Gomez, J. Park, S. Iyer | T. Nguyen | Post-mortem Fri 09:00 PT / Sat 01:00 Taipei — recorded; async comments accepted 5 days |

## Timezone norms
- Santa Clara PT (UTC-8) · Taipei CST (UTC+8) · Hyderabad IST (UTC+5:30).
- The standing program review is Thu 18:00 PT / Fri 10:00 Taipei / Fri 07:30 IST — US evening, Asia morning, so nobody is routinely on call past midnight.
- Async sign-off windows are 24h minimum so every region gets a business day.
- Emergency lane (D-07 hotfix branch): the TPM pages leads directly; decision within 4 hours regardless of time zone.
