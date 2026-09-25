---
spec: 001-parse-dates
status: approved
---
# Plan
## Constitution Check
| Principle | Result |
|---|---|
| P1 | ✅ |

## Threat model
| ID | Threat | Control | Test |
|---|---|---|---|
| TM1 | Huge input (DoS) | Length limit | test_huge_input |
## Traceability
| Item | Test |
|---|---|
| AC1 | test_basic |

| AC3, TM1 | test_huge_input |
## Rollout
Minor release (SemVer), published from CI on tag.
