# `/init --upgrade` — poner al día un proyecto

Actualiza un proyecto inicializado con una versión anterior del plugin **sin re-explorar el
código ni tocar la constitución, las specs ni las decisiones del usuario**. Todo cambio se muestra
como diff y se aplica solo con confirmación.

## Pasos

1. **Versiones.** Lee `skills_version` de `.ai/project.yaml` y la versión de `../SKILL.md`. Si son
   iguales, dilo y termina. Lee las entradas de `../../../CHANGELOG.md` del plugin entre ambas
   versiones y resume al usuario qué cambia para su proyecto.
2. **Validador.** Compara `python .ai/bin/aidd.py --version` con `../../../scripts/aidd.py`.
   Si es anterior, reemplázalo por la copia del plugin.
3. **Plantillas.** Para cada archivo de `docs/templates/`, compáralo con `../templates/` (ignora
   finales de línea). Muestra el diff de los que cambiaron y reemplázalos tras confirmar. Si el
   usuario personalizó una plantilla, ofrece fusionar en lugar de reemplazar.
4. **`.gitignore`.** Si falta `.ai/cache/`, propón añadirlo (lo usa `/analyze` delta desde 1.6.0).
   **`project.yaml`.** Añade las claves nuevas de `../templates/project.yaml` que falten, con su
   valor por defecto o `TODO(init)`. Nunca cambies valores existentes.
5. **Migración de formato.** Si `security.md`, `observability.md` o `deployment.md` no numeran
   sus riesgos y correcciones (`RS1`/`RS1.a`, `OB`, `RD`, desde 1.5.6), propone numerarlos con
   diff, sin cambiar su contenido. Después revisa los objetivos del roadmap y las specs que citan
   riesgos ("riesgo 1", "riesgos 1 y 3"…) y **reporta** las correcciones que no cubren ni
   excluyen de forma explícita; propone cómo declararlas, sin aplicarlo sin confirmación.
5b. **Historial de specs (desde 1.7.0).** Para cada spec con rondas o versiones sueltas en su
   carpeta (`analysis.r<N>.md`, `review.r<N>.md`, `plan.v<N>.md`, `tasks.v<N>.md`; el validador lo
   avisa), propone `python .ai/bin/aidd.py history docs/specs/NNN-<slug> --migrate` (las mueve a
   `history/` y corrige los enlaces). Si git registra versiones o rondas **borradas** de una spec
   (`git log --diff-filter=D --name-only -- docs/specs/NNN-*/`), ofrece restaurarlas en `history/`
   con `git show <commit>^:<ruta>`. **Nunca borres** archivos de historial durante un upgrade.
   Si la spec está en curso (`approved` con tareas empezadas) y `tasks.md` no tiene `impl_base`,
   propone el commit que aprobó las tareas.
6. **Documentos nuevos del paquete.** Si la versión nueva introduce un documento que el proyecto
   no tiene (p. ej. `docs/observability.md` desde 1.5.0), ofrece generarlo. Para hacerlo, ejecuta
   **solo** el subagente de exploración correspondiente de `explore-agents.md` y las preguntas de
   entrevista de ese bloque; no repitas el resto de `/init`. Después **concilia** las brechas
   del documento nuevo con el roadmap existente según `brownfield.md` §4: enlaza las que ya cubre
   un objetivo, propone (con confirmación) las parciales y las nuevas, e informa lo que los
   objetivos del usuario mencionan y la exploración no detectó.
7. **Constitución.** No la modifiques. Si la versión nueva propone principios nuevos (p. ej. de
   observabilidad), preséntalos como **propuesta de enmienda** con su versión nueva (MINOR) para
   que el usuario decida; si acepta, añádelos y registra la enmienda.
8. **CI.** Si existe `.github/workflows/ai-dd.yml` y la plantilla cambió, muestra el diff; es una
   ruta protegida: solo con confirmación explícita.
9. **Enlaces.** Si hay documentos nuevos, añádelos a la sección "Documentación" de `AGENTS.md`.
10. **Cierre.** Actualiza `skills_version`, añade una entrada en `CHANGELOG.md` del proyecto
   (`### Changed — flujo AI-DD actualizado a X.Y.Z`), ejecuta `python .ai/bin/aidd.py validate` y
   resume qué se cambió, qué se ofreció y se rechazó, la conciliación con el roadmap y qué queda
   pendiente.
