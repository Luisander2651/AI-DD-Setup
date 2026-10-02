---
status: approved
---
# Parse ISO dates
## Problem
Users need to parse ISO-8601 dates without extra dependencies. Addresses RS1 partially.
## Acceptance criteria
- [ ] AC1 `parse("2026-09-25")` returns a `date`
- [ ] AC2 Timezone offsets are preserved
- [ ] AC3 (abuse) A 10 MB string is rejected in under 10 ms 
## Out of scope
Non-ISO formats.
## Security and privacy
Untrusted input strings (see AC3).
## Risk coverage
| Correction | Scope | Criteria / reason and destination |
|---|---|---|
| RS1.a — length limit | in | AC3 |
| RS1.b — linear-time parser | out | needs a new engine → roadmap objective 2 |

## Audit
Not applicable: a library does not log.

## Decisions
| Date | Type | Question / conflict | Decision | Source |
|---|---|---|---|---|
| 2026-10-02 | implicit | Runtime dependencies | None | docs/constitution.md P2 |
| 2026-10-02 | contradiction | "Accept any format" vs. AC1 (ISO only) | ISO only | user |
| 2026-10-02 | gap | Maximum input length | 10 MB | user (/clarify) |
| 2026-10-02 | assumption | Error type | `ValueError` | /clarify (recommended) |
