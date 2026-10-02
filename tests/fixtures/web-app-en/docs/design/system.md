---
status: approved
source: extracted
version: 1.0.0
html: docs/design/system.html
---
# Design system of Plantshop
## Color
| Token | Value | Use | Contrast on its background |
|---|---|---|---|
| `--color-bg` | `#fbfaf6` | Base | — |
| `--color-text` | `#1f2a1c` | Main text | 14.9:1 on --color-bg |
| `--color-text-muted` | `#4f5b4b` | Secondary text | 6.8:1 on --color-bg |
| `--color-on-primary` | `#ffffff` | Text on primary | 5.2:1 on --color-primary |
| `--color-danger` | `#a4262c` | Errors | 6.9:1 on --color-bg |
## Design debt
| ID | Problem | Where | Fix | Status |
|---|---|---|---|---|
| DS1 | Hardcoded hex colors in 12 files | src/components | Replace with tokens | pending |
