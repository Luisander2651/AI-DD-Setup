---
status: approved
---
# SEO
## Site rules
- Canonical URL: https://lumen.example.com (https, no `www`, trailing slash).
- Language: English only. Rendering: static (generated at build time).
- Not indexed: internal search results, 404, staging and preview deployments.

## Route inventory
| Route | Indexable | Title | Description | Canonical | Evidence |
|---|---|---|---|---|---|
| `/` | yes | ✅ | ✅ | ✅ | dist/index.html |
| `/services/` | yes | ❌ same as `/` | ❌ missing | ✅ | dist/services/index.html |
| `/search/` | no (internal search results) | ➖ | ➖ | ➖ | dist/search/index.html |

## Gaps
### SE1 · Medium — Every route shares the home page title and has no description
Evidence: dist/services/index.html, dist/about/index.html.
Corrections:
- SE1.a Unique title per route — status: pending
- SE1.b Unique meta description per route — status: pending

### SE2 · Medium — No sitemap.xml
Corrections:
- SE2.a Sitemap generated at build time with every indexable route — status: pending

## Gaps to confirm
- Whether staging sends `X-Robots-Tag: noindex` (not determined: no staging URL).
