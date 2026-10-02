---
status: approved
---
# Security
## Known risks
### RS1 · High — Catastrophic backtracking on hostile input (A05:2025)
Corrections:
- RS1.a Reject inputs longer than 64 characters before parsing — status: pending
- RS1.b Replace the regex engine with a linear-time parser — status: pending
