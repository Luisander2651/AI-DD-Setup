---
lane: fix
status: done
base: aa11bb2
relates: [001]
covers: [AC9]
---

# Fix: offsets with seconds are rejected

## Problem
`+05:30:15` raises instead of parsing.

## Root cause
The offset regex stops at minutes.

## Change
Accept an optional seconds group.

## Escalation
lane-check: no.

## Verification
Suite passes.
