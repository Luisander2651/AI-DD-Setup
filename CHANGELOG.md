# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[SemVer](https://semver.org/lang/es/).

## [1.8.1] - 2026-09-25
### Fixed
- El validador fallaba con `UnicodeDecodeError` si un `.md` estaba guardado en ANSI (cp1252,
  habitual en editores de Windows). Ahora lee UTF-8 (con o sin BOM) y, si no lo es, cp1252.
- `tests/run.py` escribía archivos con la codificación por defecto del sistema: en Windows (CI)
  rompía el escenario de `review-pack`. Todas las escrituras son UTF-8 explícito, la salida se
  fuerza a UTF-8 y hay un escenario nuevo con specs en cp1252 y en UTF-8 con BOM.

## [1.8.0] - 2026-09-25
Contra el sobreajuste: hasta aquí todo se había probado en un solo proyecto (Laravel, brownfield,
en español). Probado contra proyectos de otro tipo, el validador no aceptaba documentos en inglés y
no había soporte para apps móviles.

### Added
- **Idioma:** `project.yaml → language` y `shared/vocabulary.md` con la forma española e inglesa de
  cada título, ID y marcador que lee el validador (`Acceptance criteria`, `AC1`, `done when:`,
  `covers:`, `(abuse)`, `NOT MET TODAY`…). El validador acepta ambas; `/init` traduce las
  plantillas con ese vocabulario.
- **Tipo `mobile`** (Ionic/Capacitor, React Native, Flutter): detección en `/init`, sección de
  arquitectura, principios propuestos (MASVS, almacenamiento seguro, permisos mínimos,
  compatibilidad con versiones instaladas), preguntas de despliegue (tiendas, canal de pruebas,
  firma, publicación escalonada, actualizaciones en vivo), contratos y Rollout en `/plan`, y
  `/release` para tiendas con su rollback real (detener el escalonado, flag remoto, hotfix).
  Checklist MASVS ampliado. El hook protege claves de firma (`*.keystore`, `*.jks`, `*.p12`,
  `*.p8`, `*.mobileprovision`, `key.properties`).
- `tests/run.py` y `tests/fixtures/`: proyectos de prueba de otro tipo e idioma (librería Python en
  inglés, app Ionic en español, CLI en Go, monorepo), válidos e inválidos, más escenarios de
  `review-pack`, `history`/`rotate` y el hook. CI en Linux y Windows con Python 3.8 y 3.12.

### Changed
- El aviso de "Observabilidad" en el plan no aplica a `library`.
- La columna Alcance de "Cobertura de riesgos" se lee en su celda, no en toda la fila (un motivo
  que decía "fuera" marcaba como fuera una corrección "dentro").

### Removed
- `scripts/__pycache__/` del repositorio.

## [1.7.1] - 2026-09-25
### Fixed
- `review-pack`: la coincidencia por nombre de archivo (para rutas abreviadas con alias en las
  tareas) daba por cubiertos archivos distintos con el mismo nombre (`app/admin/page.tsx` por
  `app/login/page.tsx`). Ahora solo se usa si la ruta citada no existe y el nombre no se repite.

## [1.7.0] - 2026-09-25
Lecciones de la primera spec recorrida de punta a punta (7 rondas de `/analyze`, 3 de `/review`,
~200k tokens por revisor en la primera review).

### Added
- `aidd.py review-pack`: paquete compartido de `/review` en `.ai/cache/review/` con el diff de
  código filtrado (sin `docs/`, `.ai/`, Markdown ni lockfiles), `scope.md` (archivos sin tarea y
  tareas sin diff), `context.md` (criterios, amenazas, trazabilidad) y tamaño estimado en tokens.
- `impl_base` en `tasks.md`: lo registra `/implement`; `/review` revisa desde ahí y no desde el
  merge con la rama principal.
- Historial de la spec en `docs/specs/NNN/history/` (nunca se borra): `aidd.py rotate` archiva la
  ronda o versión vigente; `aidd.py history [--write] [--migrate]` indexa las rondas y mueve las
  sueltas corrigiendo enlaces. `/release` escribe `history/README.md`.
- `aidd.py changes --since REF` y aviso cuando la copia en caché no coincide con el último análisis.
- `aidd.py status` muestra las rondas de `/analyze` y `/review` (`a7 r3`).
- Validador: aceptados `- **ID** → nota de T0xx` sin su nota en una tarea hecha (error); rondas o
  versiones sueltas; aceptados sin tarea de `/review` que no llegaron al roadmap (`NNN/R#`).
- `/plan`: línea base SCA (vulnerabilidades previas a decidir antes de implementar) y tabla
  "Qué ve cada rol" cuando cambian permisos con interfaz.
- `/implement`: hallazgos colaterales de la spec se preguntan al momento; los tests que pasan
  desde el principio se comprueban rompiendo a mano lo que protegen.

### Changed
- `/review`: cada revisor recibe solo lo que su encargo necesita y devuelve solo hallazgos;
  "Plan y alcance" lo hace el orquestador con `scope.md`; Constitución y Calidad en un solo
  agente; `--rerun` sin subagentes si el diff es pequeño. Las tareas que añade cumplen las reglas
  de `/tasks` y no requieren otro `/analyze` salvo cambio de diseño. Sección "Aceptados sin tarea".
- `/analyze` recomienda la condición que debe cumplirse y su test, no el mecanismo; los aceptados
  llevan destino explícito.
- `--redo` de plan y tareas archiva la versión anterior en `history/` (antes: solo en commits).
- `/init --upgrade` migra rondas sueltas a `history/` y ofrece restaurar las borradas desde git.

### Fixed
- El aviso "cita riesgos por número" ya no salta por el Historial de la spec.

## [1.6.0] - 2026-09-24
Iterar más barato: una spec real llegó a 3 versiones de plan, 3 de tareas y 3 análisis completos,
cada vuelta regenerando ~70 KB y releyendo todo el código.

### Added
- `/analyze` en modo **delta** tras la primera ronda: solo verifica los hallazgos abiertos y el
  diff desde el análisis anterior (`aidd.py changes`); vuelve a completo si cambió la
  constitución, el alcance o más de ~40 % del plan o las tareas. Conserva cada ronda como
  `analysis.r<N>.md`, numera los hallazgos de forma continua y separa "Seguimiento", "Hallazgos
  nuevos" y "Decisiones pendientes del usuario". Propone aceptar BAJOS y MEDIOS no estructurales
  para resolverlos en `/implement`.
- `/plan --fix <IDs>` y `/tasks --fix <IDs>`: edición en su lugar de las secciones o tareas
  afectadas, con diff por hallazgo; `--redo` queda para cambios estructurales.
- `/plan` Paso 2b "Decisiones pendientes del usuario": antes de escribir el plan pregunta en una
  ronda las excepciones o enmiendas de la constitución, el orden frente a otras specs en curso que
  comparten archivos, cambios de alcance y contratos visibles que rompen tests existentes.
- Límite de tamaño: `/specify` y `/plan` proponen dividir specs con más de ~10 criterios, dos
  capacidades separables, más de 4 specs extendidas o más de 3 módulos; el validador avisa.
- `aidd.py snapshot` y `aidd.py changes`.

### Changed
- Con git, las versiones anteriores de plan y tareas viven en commits; ya no se crean copias
  `plan.v<N>.md` / `tasks.v<N>.md` (solo sin git).

## [1.5.6] - 2026-09-24
### Fixed
- Pérdida de correcciones al resumir riesgos (detectado en uso real): `init` escribió un objetivo
  del roadmap que citaba un riesgo de `security.md` con cuatro correcciones y recogía solo dos;
  la spec heredó el recorte (una corrección quedó solo como nota técnica, sin decidir) y el plan
  iba a declarar el riesgo mitigado. Solo `/analyze` lo detectó.

### Added
- Cobertura de riesgos: IDs para riesgos y correcciones (`RS1`/`RS1.a` en `security.md`, `OB` en
  `observability.md`, `RD` en `deployment.md`). Todo objetivo, spec, plan o tarea que cite un
  riesgo declara **cada** corrección dentro o fuera (con motivo y destino); un riesgo solo pasa a
  mitigado con todas sus correcciones mitigadas o aceptadas.
- Sección "Cobertura de riesgos" en la plantilla de spec; `specify` lee el riesgo en su documento
  de origen, no el resumen del roadmap.
- Validador: errores si una spec o un objetivo del roadmap cita un riesgo sin declarar todas sus
  correcciones, o si un plan o una tarea lo declara mitigado sin cubrirlas; avisos si se citan
  riesgos por número o falta "parcialmente" en el Problema.
- `analyze` (categoría 7), `review` y `release` revisan y actualizan el estado por corrección.
- `init --upgrade` propone numerar riesgos existentes y reporta objetivos y specs con cobertura
  incompleta.

## [1.5.5] - 2026-09-24
### Added
- Re-sincronizar sin perder decisiones (`references/brownfield.md` §5): el contenido marcado
  `(confirmado por el usuario, …)` o `(decisión del usuario, …)`, las excepciones, retenciones y
  responsables, y las secciones Aclaraciones/Historial/Enmiendas nunca se reescriben; los
  documentos `approved` solo reciben propuestas por sección; las contradicciones se preguntan.
- `init` escribe esos marcadores cada vez que el usuario confirma o decide algo.
- `--force` avisa de que se pierden las confirmaciones y pide confirmación explícita.

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
