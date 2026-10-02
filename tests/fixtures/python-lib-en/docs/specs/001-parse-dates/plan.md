---
spec: 001-parse-dates
status: approved
---
# Plan
## Constitution Check
| Principle | Result | Justification | How it is verified |
|---|---|---|---|
| P1 | ✅ | Pure functions | test: test_basic |
| P2 | ✅ | No runtime dependencies | lint: deptry |
## Threat model
| ID | Threat | Control | Test |
|---|---|---|---|
| TM1 | Huge input (DoS) | Length limit | test_huge_input |
## Traceability
| Item | Test |
|---|---|
| AC1 | test_basic |
| AC2 | test_offset |
| AC3, TM1 | test_huge_input |
## Rollout
Minor release (SemVer), published from CI on tag.
## Risks and mitigations
- RS1.a covered by TM1. RS1 is not mitigated by this release: RS1.b stays open (→ roadmap objective 2).
