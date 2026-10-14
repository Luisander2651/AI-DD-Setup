---
lane: fix
status: done
base: 3f2a91c
relates: [001]
covers: [AC1]
escalated_to: null
---

# Fix: `--follow` drops the last line when the file has no trailing newline

## Problem
With `--follow`, a line written without a trailing newline never appears until the next write.

## Reproduction
`internal/follow/follow_test.go: TestFollowPrintsLineWithoutNewline` — failed before the fix:
`expected "c", got ""`.

## Root cause
The reader only flushed on `\n`; a partial line at EOF stayed in the buffer.

## Change
Flush the pending partial line when the poll finds the file unchanged for one interval.

## Escalation
`aidd.py lane-check`: no (1 code file, no contract, data, security or dependency changes).

## Verification
- The new test passes; `go test ./...` passes.
- Light review: the test fails with the change reverted; no findings.

## Decisions
| Date | Type | Question / conflict | Decision | Source |
|---|---|---|---|---|
| 2026-10-14 | implicit | Is a line without newline a line? | Yes | docs/specs/001-follow-mode/spec.md |
