# `/init --upgrade` — poner al día un proyecto

Actualiza un proyecto inicializado con una versión anterior del plugin **sin re-explorar el
código ni tocar la constitución, las specs ni las decisiones del usuario**. Todo cambio se muestra
como diff y se aplica solo con confirmación. Los pasos van en el orden en que se ejecutan; cada uno
dice desde qué versión existe y no hace nada si el proyecto ya lo cumple.

## Pasos

1. **Versiones.** Lee `skills_version` de `.ai/project.yaml` y la versión de `../SKILL.md`. Si son
   iguales, dilo y termina. Lee las entradas de `../../../CHANGELOG.md` del plugin entre ambas
   versiones y resume al usuario qué cambia para su proyecto.
2. **Validador.** Compara `python .ai/bin/aidd.py --version` con `../../../scripts/aidd.py`.
   Si es anterior, reemplázalo por la copia del plugin (los pasos siguientes usan sus comandos).
3. **Plantillas.** Ejecuta `python .ai/bin/aidd.py templates`: compara cada archivo de
   `docs/templates/` con la huella que se guardó al copiarlo (`project.yaml → template_hashes`).
   - `sin cambios` → el usuario no la tocó: muestra el diff con `../templates/` y reemplázala tras
     confirmar.
   - `personalizada` → ofrece **fusionar**: conserva lo que añadió el usuario y aplica los cambios
     de la plantilla nueva; muestra el resultado antes de escribirlo.
   - `sin registro` (proyectos anteriores a 1.11.1) → busca en git la versión con que se copió
     (`git log --diff-filter=A -- docs/templates/<archivo>` y `git show <commit>:<ruta>`); si es
     igual al archivo actual, trátala como `sin cambios`; si no hay historia, pregunta.
   Al terminar, guarda las huellas nuevas: añade o reemplaza el bloque `template_hashes` de
   `project.yaml` con la salida de `python .ai/bin/aidd.py templates --yaml`.
4. **`project.yaml` y `.gitignore`.** Añade las claves nuevas de `../templates/project.yaml` que
   falten, con su valor por defecto o `TODO(init)`. Nunca cambies valores existentes. Si falta
   `.ai/cache/` en `.gitignore`, propón añadirlo (lo usa `/analyze` delta desde 1.6.0).
5. **Riesgos numerados (desde 1.5.6).** Si `security.md`, `observability.md` o `deployment.md` no
   numeran sus riesgos y correcciones (`RS1`/`RS1.a`, `OB`, `RD`), propone numerarlos con diff, sin
   cambiar su contenido. Después revisa los objetivos del roadmap y las specs que citan riesgos
   ("riesgo 1", "riesgos 1 y 3"…) y **reporta** las correcciones que no cubren ni excluyen de forma
   explícita; propone cómo declararlas, sin aplicarlo sin confirmación.
6. **Idioma (desde 1.8.0).** Si falta `language` en `project.yaml`, infiérelo de los documentos
   existentes y pide confirmación. Los títulos y marcadores ya escritos siguen siendo válidos
   (español o inglés, `shared/vocabulary.md`).
7. **Herramientas con estado y dependencias externas (desde 1.9.0).** Si `security.tools` usa el
   formato anterior (`secrets: <comando>`), conviértelo a `{ command, status }` y **pregunta** el
   estado real de cada una (`propuesta` · `instalada` · `en-ci` · `no-aplica`) ejecutando
   `<comando> --version`; no supongas `instalada`. Si el SAST es `semgrep … --config auto`, avisa
   de que exige enviar métricas a semgrep.dev y propone reglas fijadas con `--metrics=off`, o
   registrar el servicio como aprobado en `docs/security.md`. **En el mismo diff** actualiza la
   tabla "Herramientas" de `docs/security.md` (columna Estado y comando nuevo), para que los dos
   documentos no se contradigan. Si `skills.enabled` contiene `design`, pregunta si el plugin
   oficial `design` de Anthropic sigue instalado; si no, quítalo. Si el proyecto es greenfield y
   `AGENTS.md` sigue con comandos `TODO(init)`, ofrece `references/greenfield.md` §2–§3.
8. **Decisiones y verificación (desde 1.10.0).** Nada se migra a la fuerza: las specs con
   "Supuestos" y "Aclaraciones" siguen siendo válidas. Para las specs en `draft` o `approved`
   (mira el estado de la **spec**, no el del plan: el plan de una spec terminada sigue en
   `approved`), ofrece convertir esas secciones a la tabla "Decisiones" (tipo `supuesto` o
   `brecha`, fuente `usuario` si lo decidió el usuario) y añadir la columna "Cómo se verifica" al
   Constitution Check de su plan. Las specs `implemented` y `released` no se tocan: sus avisos de
   reglas nuevas salen como "heredados" en `validate`.
9. **Diseño (desde 1.11.0).** Si el proyecto tiene interfaz (`frontend`, `fullstack`, `mobile`) y
   `design.status` falta o es `none`, pregunta si documentar el diseño que usa hoy el código. Con
   un sí, sigue **solo** `design.md` §3 (subagente G, capturas con datos de prueba y medidas,
   auditoría, `system.md` extraído, `system.html` y deuda `DS`), sin re-explorar el resto del
   código. Con un no, `design.status: declined` y no vuelvas a preguntar. Nunca ofrezcas rediseño
   ni opciones. Si `design.status` es `declined`, `draft` o `approved`, no hagas nada. Si
   `skills.enabled` no tiene `design` y el plugin está instalado, ofrece registrarlo.
10. **Historial de specs (desde 1.7.0).** Para cada spec con rondas o versiones sueltas en su
    carpeta (`analysis.r<N>.md`, `review.r<N>.md`, `plan.v<N>.md`, `tasks.v<N>.md`; el validador lo
    avisa), propone `python .ai/bin/aidd.py history docs/specs/NNN-<slug> --migrate` (las mueve a
    `history/` y corrige los enlaces). Si git registra versiones o rondas **borradas** de una spec
    (`git log --diff-filter=D --name-only -- docs/specs/NNN-*/`), ofrece restaurarlas en `history/`
    con `git show <commit>^:<ruta>`. **Nunca borres** archivos de historial durante un upgrade.
    Si la spec está en curso (`approved` con tareas empezadas) y `tasks.md` no tiene `impl_base`,
    propone el commit que aprobó las tareas.
11. **Documentos nuevos del paquete.** Si la versión nueva introduce un documento que el proyecto
    no tiene (p. ej. `docs/observability.md` desde 1.5.0), ofrece generarlo. Para hacerlo, ejecuta
    **solo** el subagente de exploración correspondiente de `explore-agents.md` y las preguntas de
    entrevista de ese bloque; no repitas el resto de `/init`. Después **concilia** las brechas
    del documento nuevo con el roadmap existente según `brownfield.md` §4: enlaza las que ya cubre
    un objetivo, propone (con confirmación) las parciales y las nuevas, e informa lo que los
    objetivos del usuario mencionan y la exploración no detectó.
12. **Constitución.** No la modifiques. Si la versión nueva propone principios nuevos (p. ej. de
    observabilidad o "solo el sistema de diseño"), preséntalos como **propuesta de enmienda** con su
    versión nueva (MINOR) para que el usuario decida; si acepta, añádelos y registra la enmienda en
    "Enmiendas" (la fila dice qué principio se añade). Los planes con `constitution_version` se
    siguen validando contra su versión; a los planes sin ese dato de specs abiertas (`draft`,
    `approved`) **propón** evaluar el principio nuevo en su Constitution Check y guardar
    `constitution_version` (si no, el validador dará error); los de specs cerradas no se tocan.
13. **CI.** Si existe `.github/workflows/ai-dd.yml` y la plantilla cambió, muestra el diff; es una
    ruta protegida: solo con confirmación explícita.
14. **Enlaces.** Si hay documentos nuevos, añádelos a la sección "Documentación" de `AGENTS.md`.
15. **Cierre.** Actualiza `skills_version`, añade una entrada en `CHANGELOG.md` del proyecto
    (`### Changed — flujo AI-DD actualizado a X.Y.Z`), ejecuta `python .ai/bin/aidd.py validate` y
    resume qué se cambió, qué se ofreció y se rechazó, la conciliación con el roadmap y qué queda
    pendiente. Un error del validador después del upgrade es un fallo del upgrade: corrígelo (o
    explica qué decisión del usuario falta) antes de cerrar.
