# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[SemVer](https://semver.org/lang/es/).

## [1.11.0] - 2026-10-02
Diseño en el flujo (plan en `docs/plan-integracion-design.md`). La prueba 8.13 llegó a producción
con los componentes por defecto de Ionic y campos sin margen porque ninguna skill pedía diseño; el
portafolio personal, que sí lo tuvo desde el principio, mantuvo 15 specs coherentes con un solo
sistema.

### Added
- **Greenfield con interfaz:** Ronda 4b de diseño en la entrevista (objetivo, marca y colores,
  tipografía, referencias) y **opciones en HTML**: 3 por defecto, 2 si el usuario ya trae marca.
  La elegida pasa a `docs/design/system.md` y `system.html`; sus tokens se escriben en el tema del
  proyecto base y la auditoría de la plantilla compara también con el sistema.
- **Brownfield con interfaz:** solo si el usuario acepta (pregunta en la Fase 0), documenta el
  diseño existente: subagente G, capturas con datos de prueba, auditoría, `system.md` extraído,
  `system.html` y deuda `DS` propuesta al roadmap. Nunca rediseña; `declined` si no se quiere.
- `/init --upgrade` §5e: solo la documentación del diseño existente, si el usuario acepta.
- **Rediseño como spec propia:** `/plan` (`references/design.md`) genera las opciones en la carpeta
  de la spec, "Cambios a incorporar al sistema" como primera tarea y migración por pantalla.
- Plantillas `templates/design/`: `system.md`, `brief.md`, `creative-direction.md`,
  `anti-cliches.md` (base por tipo de proyecto) y `option.html` (autocontenida, sin red, modo
  oscuro, "Sin movimiento" y **contraste calculado por la propia página**).
- Bloque `design` en `project.yaml` y principio "La interfaz usa solo el sistema de diseño".
- La skill `design` (canvas a partir de un brief) como dependencia opcional junto al plugin
  `design` de Anthropic: si la sesión la ofrece se usa para las opciones; el HTML es siempre el
  entregable.
- Validador: `design.status`/`source`, `system.md` y su HTML, contraste declarado en cada color de
  texto, spec con "Diseño" que no enlaza el sistema. Fixtures `web-app-en` y prueba de que
  `option.html` no carga nada externo.

### Changed
- Espacio en `init` y `plan`: las señales y secciones por tipo pasan a
  `init/references/project-types.md` y los contratos por tipo a `plan/references/contracts-by-type.md`.

## [1.10.0] - 2026-10-02
Prácticas tomadas del flujo del portafolio personal (sitio estático en Astro, 15 specs de punta a
punta con 4 skills y sin subagentes): decisiones con origen, estado que sobrevive a una sesión
cortada y comprobaciones más tempranas.

### Added
- **"Decisiones"** en la spec (`| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |`), que
  sustituye a "Supuestos" y "Aclaraciones". `/specify` Paso 1b clasifica cada duda: `implícita` (la
  responde un documento: no se pregunta, se anota con su ruta), `contradicción` (solo la decide el
  usuario), `brecha` o `supuesto`. Validador: contradicción sin el usuario (error), implícita sin
  documento y tipo desconocido (avisos).
- **Jerarquía de fuentes** en el contrato: contrato → constitución → `AGENTS.md` → security,
  architecture y sistema de diseño → specs aprobadas → petición actual.
- **Bloqueo** escrito en la tarea (`  - bloqueo: AAAA-MM-DD — <qué falta> — <skill>`): `/implement`
  lo deja al detenerse y `status` propone esa skill como siguiente paso. Validador: formato y
  tareas hechas con bloqueo.
- **Tareas obsoletas** `[-]` con `obsoleta: <motivo>`: al replanificar no se borran tareas hechas o
  empezadas; no cuentan como abiertas, hechas ni como cobertura.
- Constitution Check del plan con columna **"Cómo se verifica"** (`test:`, `lint:`, `manual:`): un
  principio con umbral o prohibición comprobable se verifica con test o lint (aviso si un ✅ no lo
  dice; `/analyze` y `/review` lo comprueban).
- **Commits trazables**: `Cubre: CA1, CA3` y la ruta de `tasks.md` en el cuerpo.

### Changed
- `verificación manual:` va en la tarea que construye la pieza (`hecho cuando: … · verificación
  manual: …`): `/implement` la hace o la pide, con capturas en los anchos de la constitución o del
  diseño cuando hay navegador, y espera la confirmación del usuario. T095 conserva solo las que
  exigen staging, dispositivo físico o tienda.

## [1.9.0] - 2026-10-02
Primer proyecto **nuevo** recorrido de punta a punta (8.13): app Ionic/Capacitor sin backend con
datos de salud, de `/init` a `/release` (4 rondas de `/analyze`, 2 de `/review`, 57 + 21 tests).
38 hallazgos; informe en `docs/pruebas/8.13-greenfield-ionic.md`.

### Added
- **Proyecto base en greenfield** (`skills/init/references/greenfield.md`, `/init` Fase 3b): detectar
  un andamiaje recién generado (no es brownfield), crear el proyecto base con el comando oficial o
  como spec 001, fijar comandos reales y **auditar los valores por defecto de la plantilla** contra
  la constitución (versiones mínimas, permisos, copias de seguridad, tamaños de control).
- `/plan` Paso 1b: **prueba de concepto** desechable de herramientas de test, frameworks y plugins
  nuevos antes de fijar el diseño.
- `verificación manual:` en la Trazabilidad del plan → comprobaciones de T095; tabla de requisitos
  no funcionales en la Cobertura de `tasks.md`.
- `(generado por <comando>)` en las tareas: cuenta como un archivo y `review-pack` lo deja fuera de
  `code.diff` (salvo los archivos que otra tarea cita) y lo resume en `scope.md`.
- Estado por herramienta en `security.tools` (`propuesta` · `instalada` · `en-ci` · `no-aplica`);
  solo se ejecutan las instaladas o en CI, y una `propuesta` no cubre ningún tema (`/review` la
  reporta como importante y `/release` se detiene con una SCA propuesta).
- Mobile: perfil MASVS en la entrevista (`security.masvs_level`), variante "sin servidor" de la ronda
  de observabilidad y de `observability.md`, riesgo `RD` por falta de flag remoto, control MASVS junto a la categoría
  OWASP en el modelo de amenazas y tema Mobile del checklist ampliado (copias de seguridad, iCloud, permisos
  de la plantilla, recientes y capturas, teclado, `FileProvider`, log del puente, SDK mínimo).
- Política de tests inestables: los tests nuevos de UI/e2e se ejecutan dos veces en `/implement` y
  `/review`.
- Validador: aviso cuando plan o tareas citan un riesgo que la spec no cita.
- Hook: `AGENTS.md` y `CLAUDE.md` piden aprobación (también en modo `block`, para no bloquear a
  `/init`); editar un manifiesto (`package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`,
  `Gemfile`, `.csproj`…) que añade dependencias pide la verificación de §2 (y se deniega en modo
  `block` sin spec activa).
- `/implement`: excepción para la spec del proyecto base, cuyas tareas fijan los comandos.

### Changed
- `agent-security.md` §2: la antigüedad es la de la **versión**; instalar con el límite de fecha del
  gestor (`npm --before`, pnpm `minimumReleaseAge`, `uv --exclude-newer`) para las transitivas; una
  transitiva importada en el código cuenta como dependencia nueva; tabla en el ADR para andamiajes.
- SAST por defecto con reglas fijadas y `--metrics=off`: `semgrep --config auto` exige enviar
  métricas a semgrep.dev.
- `/analyze` delta pequeño (< ~30 KB, sin cambio estructural) sin subagente.
- `/specify --edit` por hallazgos de `/analyze` → `/plan --fix`, no regenerar el plan.
- `/implement`: "no existe el módulo" es razón esperada (mejor: stub en la tarea de test);
  comprobación rompiendo lo protegido obligatoria para controles de seguridad.
- `/release`: compara el **código** desde el head de la review (el commit de `review.md` no cuenta);
  T095 en mobile con resultados del usuario por comprobación.
- `[P]` redefinido: paralelizable dentro de su grupo una vez cumplidas sus dependencias.
- `aidd.py status`: con `/analyze` en `fail` propone las correcciones; sin tareas abiertas,
  `/review --rerun`.
- `review-pack --base`: en un rerun solo cuentan las tareas nuevas.
- Línea `Conteo:` fija en análisis y review (la usa `history`).

### Fixed
- Validador: "no lo declara mitigado" / "not mitigated" ya no cuenta como declarar mitigado un riesgo
  (la negación se evalúa pegada a la palabra y por cláusula: "RS2 mitigado; RS3 no mitigado" sí
  afirma RS2).
- Validador: los "Aceptados sin tarea" de rondas de review **archivadas** también se exigen en el
  roadmap al liberar (antes se perdían).
- Validador: sin aviso de "Auditoría" si `observability.audit.required: false`.
- `review-pack`: las rutas que empiezan por punto (`.gitignore`, `.oxlintrc.json`) se reconocen
  (`lstrip` borraba el punto).
- `aidd.py … | head` ya no termina con `BrokenPipeError`.

- `design` se declara como **dependencia externa**: es el plugin oficial `design` de Anthropic, no
  una skill de este plugin (`/init` la habilitaba y `/plan`, `/implement` y `/review` la citaban sin
  decirlo). `/init` pregunta si está instalado antes de registrarla; si falta en la sesión, las
  skills avisan y siguen con su revisión propia (contrato → "Dependencias externas"; README →
  "Dependencias"). La revisión de accesibilidad de `/review` se hace en toda UI, con o sin `design`.

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
