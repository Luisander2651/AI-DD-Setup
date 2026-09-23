# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[SemVer](https://semver.org/lang/es/).

## [1.4.0] - 2026-09-22
### Added
- `shared/agent-security.md`: seguridad del proceso con agentes (contenido de terceros como dato,
  verificación de dependencias nuevas contra slopsquatting, comandos y rutas protegidas, secretos).
- `scripts/aidd.py`: validador determinista (`validate`), índice de estado (`status`), huellas
  (`hash`) y hook de guardia (`hook pre-tool`).
- `hooks/hooks.json`: guardia `PreToolUse` configurable con `workflow.enforcement`.
- Skills `clarify` y `analyze`; `analyze` es la puerta antes de `implement`.
- Plantilla de GitHub Actions (`templates/ci/`) que `init` propone con confirmación.

### Changed
- Todas las skills ejecutan el validador en su autoverificación.
- `init` copia el validador a `.ai/bin/aidd.py` y añade `workflow.enforcement` y
  `security.agent` a `project.yaml`.
- `implement` exige un `analysis.md` vigente con `result: pass`.

## [1.3.1] - 2026-09-22
### Fixed
- `release`: con `deploy.strategy: none` ahora se ejecuta el cierre y la spec pasa a `released`.
- `init`: pide confirmación antes de instalar dependencias y usa modo sin scripts en repos no confiables.
- `review`: regla para cuando no quedan números de tarea libres.
- Contrato: `docs/security.md` es lectura obligatoria para todas las skills.

## [1.3.0] - 2026-09-22
### Added
- Capa de seguridad OWASP en todo el flujo: `shared/security-checklist.md`, plantilla
  `docs/security.md`, subagente de seguridad en `init` y `review`, casos de abuso en `specify`,
  modelo de amenazas en `plan`, cobertura de amenazas en `tasks`, escaneo en `implement` y puerta
  de vulnerabilidades en `release`.
- Skills `tasks` e `implement`.
- Estructura de plugin (`.claude-plugin/`), contrato común en `shared/contract.md`, README.

### Changed
- `init` dividido en `SKILL.md` + `references/` + `templates/`.

## [1.2.0] - 2026-09-22
### Added
- Skills `review` y `release`; plantillas `review.md` y `CHANGELOG.md`.
- Formato de tareas con `cubre`/`depende` y tablas de cobertura.

## [1.1.0] - 2026-09-22
### Added
- Skills `specify` y `plan`; secciones Supuestos, Notas para /plan, Historial y Trazabilidad.
- `docs/deployment.md`, sección Rollout y `skills_version`.

## [1.0.0] - 2026-09-22
### Added
- Skill `init` inicial.
