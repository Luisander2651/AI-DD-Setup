---
spec: 001-unique-titles
status: approved
---
# Plan
## Discoverability
| Route | Title | Description | Canonical | Sitemap | Indexable |
|---|---|---|---|---|---|
| `/` | Lumen Studio — Product photography | Studio photography for small brands | `/` | yes | yes |
| `/services/` | Services — Lumen Studio | Packages and prices | `/services/` | yes | yes |
## Traceability
| Item | Test |
|---|---|
| AC1 | test_titles_unique |
| AC2 | test_descriptions_unique |
## Rollout
Static deploy; rollback by redeploying the previous build.
