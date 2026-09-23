---
name: "review"
description: "Revisa una spec implementada contra la spec, el plan, la constitución y los tests, y deja un review.md con veredicto. Úsala con /review NNN o cuando el usuario pida revisar una implementación antes de liberarla."
---
 
# /review — Verificación antes de liberar
 
Sexto paso del flujo:
 
```
/init → /specify → /plan → /tasks → /implement → [/review] → /release
```
 
Comprueba que lo implementado cumple la spec, sigue el plan, respeta la constitución y está listo
para desplegarse. Produce un veredicto que `/release` exige.
 
## Uso
 
```
/review <NNN|slug>
/review <NNN> --rerun      # nueva ronda tras corregir hallazgos
```
 
## Reglas
 
- **No corrijas código.** La review informa; las correcciones las hace `/implement`.
- **Revisión independiente.** Las revisiones de código las hacen subagentes con contexto limpio,
  que no participaron en la implementación. Si el entorno no permite subagentes, revísalo tú pero
  releyendo los archivos desde cero, no desde memoria de la sesión.
- **Todo hallazgo lleva evidencia:** archivo y línea, o el comando y su salida.
- **No inventes hallazgos para parecer exhaustivo.** Una review sin hallazgos es válida.
- **Severidades:**
  - `bloqueante`: incumple un criterio de aceptación, viola la constitución, rompe tests, abre
    un problema de seguridad o hace el rollback imposible.
  - `importante`: riesgo real (bug probable, caso límite sin manejar, test que no prueba lo que
    dice), pero no incumple un criterio.
  - `menor`: estilo, nombres, legibilidad.
- Escribe en el idioma del proyecto.
---
 
## Paso 0 — Precondiciones
 
1. La spec está en `status: implemented` y T001–T092 de `tasks.md` están marcadas. Si no,
   detente y sugiere `/implement`.
2. Determina el rango a revisar: `base` = merge-base con la rama principal (o el commit anterior a
   la primera tarea), `head` = commit actual. Si hay cambios sin commitear, pregunta si incluirlos.
3. Si ya existe `review.md` y no vino `--rerun`, muestra su veredicto y pregunta si iniciar una
   nueva ronda.
## Paso 1 — Verificación automática
 
Ejecuta los comandos de `AGENTS.md`: tests (suite completa), lint, type-check y build. Compara con
la línea base registrada por `/implement` (si existe en las notas de `tasks.md`). Cualquier fallo
nuevo es `bloqueante`.
 
## Paso 2 — Revisiones en paralelo
 
Lanza estos subagentes de solo lectura en paralelo. A cada uno pásale: rutas de la spec, del plan,
de `tasks.md`, de la constitución, el rango `base..head` y el formato de hallazgo
(`severidad | archivo:línea | hallazgo | sugerencia`).
 
| Subagente | Revisa |
|---|---|
| A. Spec | Por cada `CA`: existe un test que lo prueba de verdad (no solo que existe), el test pasa, y el comportamiento implementado coincide con el texto del criterio. Revisa también los casos límite y los requisitos no funcionales. |
| B. Plan y alcance | Los cambios coinciden con "Cambios por módulo" y "Contratos y datos". Lista archivos modificados que no aparecen en ninguna tarea (alcance extra) y partes del plan sin implementar. |
| C. Constitución y seguridad | Cada principio evaluado sobre el **código real**, no sobre el plan. Además: secretos, validación de entradas, autorización, inyección, datos sensibles en logs, dependencias nuevas sin ADR. |
| D. Calidad y tests | Convenciones de `AGENTS.md`, legibilidad, duplicación, manejo de errores. Calidad de los tests: aserciones significativas, sin `skip`, sin mocks que vacíen la prueba, sin tests que pasarían con cualquier implementación. |
 
Si `design` está en `skills.enabled` y la spec toca UI, añade un subagente E que revise
accesibilidad y consistencia con el sistema de diseño.
 
## Paso 3 — Preparación para release
 
Revisa tú mismo, contra la sección Rollout del plan y `docs/deployment.md`:
- El rollback descrito es factible con lo implementado.
- Las migraciones son compatibles con la versión anterior del código (no hay *contract* en la
  misma entrega que el *expand*).
- Existen los feature flags que el plan pide, y su valor por defecto es seguro.
- `docs/architecture.md` y `docs/deployment.md` reflejan los cambios (T090, T091).
Lo que falle aquí es `bloqueante` si impide revertir, `importante` en otro caso.
 
## Paso 4 — Consolidación
 
1. Deduplica hallazgos entre subagentes y **verifica cada uno** abriendo el archivo: descarta
   los que no se sostienen.
2. Numera `R1, R2…` (en `--rerun` continúa la numeración).
3. Decide el veredicto:
| Veredicto | Cuándo |
|---|---|
| `approved` | Sin bloqueantes. Los importantes quedan aceptados explícitamente por el usuario o convertidos en tareas. |
| `changes_requested` | Hay bloqueantes o importantes que el usuario decide corregir antes de liberar. |
| `blocked` | El problema está en la spec o el plan (no en el código), o hay una violación de la constitución que no se resuelve con tareas. Sugiere `/specify --edit` o `/plan --redo`. |
 
## Paso 5 — Escritura
 
Escribe `docs/specs/NNN-<slug>/review.md` desde `docs/templates/review.md`. En `--rerun`, conserva
la ronda anterior renombrándola `review.r<N>.md` y sube `round`.
 
Muestra al usuario: veredicto, conteo por severidad y los bloqueantes e importantes con su
sugerencia. Para cada importante pregunta: corregir ahora o aceptar (con motivo).
 
## Paso 6 — Consecuencias del veredicto
 
**`changes_requested`:**
1. Por cada hallazgo a corregir, añade una tarea a `tasks.md` con el siguiente número libre
   (≤ T089) y la nota `añadida por /review: R3`.
2. Desmarca T092 y cambia la spec a `status: approved`.
3. Registra en "Tareas añadidas" de `review.md` la relación tarea ← hallazgo.
4. Siguiente paso: `/implement NNN`, y luego `/review NNN --rerun`.
**`approved`:**
- Si la definición de terminado de la constitución exige revisión humana, deja
  `human_signoff: pending` y pide al usuario que confirme; registra nombre y fecha al confirmar.
  `/release` no avanza con `pending`.
- Siguiente paso: `/release NNN`.
**`blocked`:** la spec queda en `implemented`; indica qué skill debe resolverlo.
 
## Modo `--rerun`
 
Revisa solo: los hallazgos abiertos de la ronda anterior (¿se corrigieron?), el diff desde el
`head` anterior y la verificación automática completa. No reabras hallazgos ya aceptados salvo que
el código nuevo los empeore.