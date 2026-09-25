---
spec: 001-parse-dates
status: approved
---
# Tasks
- [ ] T001 Write failing tests — `tests/test_core.py` — done when: they fail for the right reason (TM1) — covers: AC1, AC2, AC3
- [ ] T002 Implement parser — `tinyparse/core.py` — done when: tests pass — covers: AC1, AC2 — depends on: T001
- [ ] T003 Length limit — `tinyparse/core.py` — done when: test_huge_input passes (TM1) — covers: AC3 — depends on: T002

- [ ] T090 Update `docs/architecture.md` — done when: it reflects the change
- [ ] T091 Update `docs/deployment.md` — done when: it reflects the change
- [ ] T092 Mark the spec implemented — done when: status implemented
- [ ] T095 Publish to TestPyPI
- [ ] T096 Human approval for production
- [ ] T097 Publish to PyPI
- [ ] T098 Mark spec as `released`
