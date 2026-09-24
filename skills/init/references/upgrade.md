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
4. **`project.yaml`.** Añade las claves nuevas de `../templates/project.yaml` que falten, con su
   valor por defecto o `TODO(init)`. Nunca cambies valores existentes.
5. **Documentos nuevos del paquete.** Si la versión nueva introduce un documento que el proyecto
   no tiene (p. ej. `docs/observability.md` desde 1.5.0), ofrece generarlo. Para hacerlo, ejecuta
   **solo** el subagente de exploración correspondiente de `explore-agents.md` y las preguntas de
   entrevista de ese bloque; no repitas el resto de `/init`. Después **concilia** las brechas
   del documento nuevo con el roadmap existente según `brownfield.md` §4: enlaza las que ya cubre
   un objetivo, propone (con confirmación) las parciales y las nuevas, e informa lo que los
   objetivos del usuario mencionan y la exploración no detectó.
6. **Constitución.** No la modifiques. Si la versión nueva propone principios nuevos (p. ej. de
   observabilidad), preséntalos como **propuesta de enmienda** con su versión nueva (MINOR) para
   que el usuario decida; si acepta, añádelos y registra la enmienda.
7. **CI.** Si existe `.github/workflows/ai-dd.yml` y la plantilla cambió, muestra el diff; es una
   ruta protegida: solo con confirmación explícita.
8. **Enlaces.** Si hay documentos nuevos, añádelos a la sección "Documentación" de `AGENTS.md`.
9. **Cierre.** Actualiza `skills_version`, añade una entrada en `CHANGELOG.md` del proyecto
   (`### Changed — flujo AI-DD actualizado a X.Y.Z`), ejecuta `python .ai/bin/aidd.py validate` y
   resume qué se cambió, qué se ofreció y se rechazó, la conciliación con el roadmap y qué queda
   pendiente.
