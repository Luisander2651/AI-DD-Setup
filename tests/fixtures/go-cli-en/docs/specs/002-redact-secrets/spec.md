---
status: draft
---
# Redact secrets in followed logs
## Problem
Followed logs may contain API tokens.
## Acceptance criteria
- [ ] AC1 Tokens matching known patterns are printed as `***`
- [ ] AC2 (abuse) A line crafted to bypass the pattern is still redacted
## Out of scope
Custom patterns.
## Security and privacy
Credentials of third parties pass through the tool (AC2).
