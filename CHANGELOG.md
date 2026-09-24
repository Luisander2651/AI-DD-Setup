# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[SemVer](https://semver.org/lang/es/).

## [1.5.4] - 2026-09-24
### Fixed
- `init` tomaba `.env.example` y los valores por defecto de `config/` como la configuración real.
  En un proyecto real concluyó "los logs no llegan a Loki" cuando el `.env` del usuario usaba
  `LOG_CHANNEL=stderr`, y lo reportó como brecha confirmada aunque también lo había marcado como
  no determinado.

### Added
- Regla "declarado ≠ real" en `init`, los subagentes de exploración y el contrato.
- La entrevista pregunta en una sola pregunta los valores de configuración no versionados que no
  son secretos (canal y nivel de log, entorno, colas…), sin abrir `.env`.
- `observability.md` separa "Brechas", "Brechas por confirmar" (sin severidad) y "No
  determinado"; la conciliación con el roadmap solo usa brechas confirmadas.

## [1.5.3] - 2026-09-24
### Fixed
- Hook en Windows: `python3` puede ser el acceso directo de Microsoft Store, que existe pero no
  ejecuta Python. El hook elegía ese comando y fallaba en cada acción ("hook error" no
  bloqueante) y la guardia quedaba inactiva. Ahora prueba `python3`, `python` y `py` ejecutando
  Python y usa el primero que funciona; sin ninguno, no hace nada. Detectado en uso real.
- `init` y el contrato indican cómo elegir el intérprete que funciona.

## [1.5.2] - 2026-09-24
### Added
- Specs que extienden otras: campo `extends: [NNN, …]` en el frontmatter de la spec.
  - `specify` recomienda una spec nueva con `extends` cuando el cambio afecta a specs
    `inferred`, `implemented` o `released`, o cruza varias specs.
  - El validador comprueba que las specs referenciadas existan.
  - `analyze` detecta contradicciones no declaradas con las specs extendidas y specs afectadas
    que faltan en `extends`.
  - `release` anota el cambio en el Historial de cada spec extendida y marca como resueltos sus
    criterios **HOY NO SE CUMPLE**, sin cambiar su estado.

## [1.5.1] - 2026-09-24
### Added
- Conciliación de brechas con el roadmap (`references/brownfield.md` §4) en `init` y
  `init --upgrade`: enlaza las brechas ya cubiertas por objetivos del usuario, propone con
  confirmación las parciales y las nuevas, e informa lo que los objetivos mencionan y la
  exploración no detectó. Regla en el contrato: el roadmap es del usuario.

### Fixed
- `init --upgrade` generaba `docs/observability.md` sin reflejar sus brechas en el roadmap.

## [1.5.0] - 2026-09-24
### Added
- Observabilidad y auditoría en todo el flujo (hallazgo de la primera prueba real: el proyecto
  tenía la infraestructura de logs, pero la aplicación no emitía trazas ni eventos de auditoría):
  - Plantilla `docs/observability.md`: logs, correlación por petición, registro de auditoría
    (eventos, campos, solo anexado, retención, lectura restringida), métricas, alertas y brechas.
  - `init`: subagente F de observabilidad, ronda de entrevista, bloque `observability` en
    `project.yaml`, principios propuestos y regla general "presente ≠ configurada ≠ en uso".
  - `specify`: sección "Auditoría" con criterios verificables. `plan`: sección "Observabilidad"
    (Paso 3a). `review`: eventos de auditoría y datos sensibles en logs como bloqueantes.
    `release`: verificación post-deploy por `request_id`.
  - Checklist de seguridad, tema 9 ampliado (auditoría en uso, solo anexado, retención).
  - Validador: avisos si falta "Auditoría" en la spec u "Observabilidad" en el plan cuando hay
    datos sensibles.

## [1.4.2] - 2026-09-24
### Added
- `init --upgrade` (`references/upgrade.md`): actualiza validador, plantillas, claves de
  `project.yaml` y documentos nuevos sin re-explorar; la constitución solo recibe propuestas de
  enmienda.
- `init` Fase 0: detección de metodologías o reglas de agentes en competencia (AI-DLC, Spec Kit,
  Cursor, Kiro, Windsurf, Copilot, Cline) con opciones pausar, migrar o convivir
  (`references/brownfield.md` §1).
- Migración de specs previas en otros formatos a `docs/specs/NNN/referencias/` (§3).
- Bloque "Código previo" en la plantilla de constitución para brownfield.

### Changed
- Convenciones de specs inferidas formalizadas en el contrato: `[x]` = cubierto por un test,
  detalles técnicos permitidos, marca **HOY NO SE CUMPLE** (el validador da error si va con `[x]`).
- Plantilla de CI en modo baseline: seguridad solo sobre los cambios del PR y revisión completa
  semanal informativa, para que la deuda previa no bloquee todos los PRs.
- Formato Markdown normalizado en skills y plantillas.

## [1.4.1] - 2026-09-22
### Fixed
- `aidd.py`: salida en UTF-8 en Windows (antes requería `PYTHONIOENCODING=utf-8`) y lectura del
  evento del hook como UTF-8, para rutas con acentos. Detectado en la primera prueba real.

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
