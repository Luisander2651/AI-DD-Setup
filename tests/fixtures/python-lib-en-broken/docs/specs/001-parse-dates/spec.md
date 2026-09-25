---
status: approved
---
# Parse ISO dates
## Problem
Users need to parse ISO-8601 dates without extra dependencies.
## Acceptance criteria
- [ ] AC1 `parse("2026-09-25")` returns a `date`
- [ ] AC2 Timezone offsets are preserved
- [ ] AC3 (abuse) A 10 MB string is rejected in under 10 ms [NEEDS CLARIFICATION]
## Out of scope
Non-ISO formats.
## Security and privacy
Untrusted input strings (see AC3).
## Audit
Not applicable: a library does not log.
