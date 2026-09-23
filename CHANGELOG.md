# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[SemVer](https://semver.org/lang/es/).

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
