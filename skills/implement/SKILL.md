---
name: implement
description: Ejecuta las tareas aprobadas de una spec una por una, con tests primero, y marca el avance en tasks.md. Úsala con /implement NNN o cuando el usuario pida implementar una spec ya desglosada.
---

# /implement — De tareas a código

Quinto paso del flujo:

```
/init → /specify → /plan → /tasks → [/implement] → /review → /release
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Ejecuta las tareas de `tasks.md` en orden, una a la vez, verificando cada una antes de pasar a la
siguiente. **Implementa exactamente lo que dice el plan**: no rediseña, no agrega alcance.

## Uso

```
/implement <NNN|slug>                 # continúa desde la primera tarea pendiente
/implement <NNN> --task T012          # ejecuta solo una tarea
/implement <NNN> --until T030         # se detiene al terminar T030
/implement <NNN> --parallel           # delega grupos [P] en subagentes
```

## Reglas

- **Una tarea a la vez.** No empieces la siguiente hasta que la actual cumpla su criterio de hecho.
- **Solo los archivos de la tarea.** Si necesitas tocar otros, detente (ver "Desvíos").
- **Tests primero** cuando la tarea es de test o la constitución exige TDD: el test debe fallar
  antes de implementar y pasar después. Un test que pasa sin implementación es sospechoso: revísalo.
- **Nunca debilites un test** para que pase (borrar aserciones, añadir `skip`, ampliar
  tolerancias) sin aprobación explícita del usuario.
- **Sigue las convenciones** de `AGENTS.md` y el código vecino, no tus preferencias.
- **Sin secretos** en el código ni en los logs.
- **Código seguro por defecto** (guía completa en `../../shared/security-checklist.md`): consultas
  parametrizadas, validación de entradas en el servidor, autorización verificada en el servidor
  para cada recurso, salida codificada según contexto, sin `eval` ni deserialización insegura,
  errores sin detalles internos, mínimo privilegio. Implementa los controles del modelo de
  amenazas tal como los define el plan.
- **No despliegues.** Las tareas T095–T098 son de `/release`; `/implement` se detiene en T092.
- **No hagas push.** Los commits siguen la política del Paso 0.

---

## Paso 0 — Precondiciones

1. Spec `approved`, plan `approved` y `tasks.md` en `status: approved`. Si no, detente e indica
   qué falta aprobar.
2. Lee los comandos de `AGENTS.md` (test, lint, build, type-check). Si no están, detente y sugiere
   `/init` en modo re-sincronizar.
3. Revisa el estado de git:
   - Cambios sin commitear ajenos a esta spec → pregunta antes de seguir.
   - Si estás en la rama principal, propone crear una rama `feat/NNN-<slug>` (o la convención de
     `AGENTS.md`).
4. **Política de commits** (pregunta una vez por sesión si no está en `AGENTS.md`):
   (a) un commit por tarea, (b) un commit por fase, (c) sin commits, el usuario los hace.
   Mensajes con la convención del proyecto e incluyendo el ID: `feat(notificaciones): T020 …`.
5. Ejecuta la suite de tests una vez. Si ya hay tests fallando antes de empezar, regístralos como
   **línea base** (nota bajo el encabezado de `tasks.md`) y avísale al usuario; no son
   responsabilidad de esta spec, pero no deben aumentar.

## Paso 1 — Contexto

Lee la spec, el plan y `tasks.md`. Para cada tarea, relee la parte del plan que la origina y los
archivos que va a tocar antes de modificarlos.

## Paso 2 — Ciclo por tarea

Para la siguiente tarea pendiente cuyas dependencias estén hechas:

1. **Anuncia** en una línea: `T012 — <descripción>`.
2. **Si es de test:** escríbelo, ejecútalo y confirma que **falla por la razón esperada** (no por
   un error de sintaxis o import).
3. **Si es de implementación:** haz el cambio mínimo que cumple el criterio.
4. **Verifica:**
   - Los tests relacionados con la tarea pasan.
   - La suite completa no tiene fallos nuevos respecto a la línea base (en suites lentas, corre
     los tests del módulo en cada tarea y la suite completa al cerrar cada fase).
   - Lint y type-check limpios en los archivos tocados.
   - Si `.ai/project.yaml → security.tools.secrets` o `security.tools.sast` están configurados,
     córrelos sobre los archivos tocados. Un hallazgo crítico o alto se corrige dentro de la tarea;
     uno que parezca falso positivo se anota como nota y lo decide `/review`.
5. **Marca** la tarea `[x]` en `tasks.md`. Si hubo algo relevante, añade una nota debajo:
   `  - nota: <decisión menor, archivo extra justificado, deuda detectada>`.
6. **Commit** según la política elegida.

Si la verificación falla, corrige dentro del alcance de la tarea. Tras **3 intentos** sin éxito,
detente y reporta: qué se intentó, el error exacto y tu hipótesis.

## Paso 3 — Desvíos

Detente y consulta al usuario (no improvises) cuando:

| Situación | Acción sugerida |
|---|---|
| La tarea requiere una decisión de diseño que el plan no tomó | `/plan NNN --redo` |
| El comportamiento esperado no está claro en la spec | `/specify --edit NNN` |
| Hay que tocar archivos fuera de la tarea (más allá de imports triviales) | Proponer una tarea nueva |
| Hace falta una dependencia que no está en el plan | ADR + actualizar plan |
| Un cambio violaría un principio de la constitución | Detenerse; nunca seguir |
| Se descubre un bug o deuda ajena a la spec | Anotarlo en `docs/roadmap.md` → Pendientes, sin arreglarlo |

Si el usuario aprueba una tarea nueva, añádela a `tasks.md` con el siguiente número libre y la
nota `añadida durante /implement: <motivo>`.

## Paso 4 — Paralelo (`--parallel`)

Solo para tareas `[P]` consecutivas sin dependencias pendientes:
- Lanza un subagente por tarea, cada uno en su propio worktree o rama si el entorno lo permite,
  con: la tarea exacta, los archivos permitidos, el criterio de hecho, los comandos de
  verificación y las reglas de esta skill.
- Al terminar, integra los resultados uno por uno y corre la suite completa.
- Si dos subagentes tocaron el mismo archivo, la marca `[P]` estaba mal: resuelve el conflicto
  manualmente y avísale al usuario.

## Paso 5 — Cierre de la implementación

Cuando todas las tareas hasta **T089** estén hechas:
1. **T090:** actualiza `docs/architecture.md` según "Impacto en arquitectura" del plan.
2. **T091:** actualiza `docs/deployment.md` si cambiaron variables, entornos o pasos.
3. Corre la suite completa, lint, type-check y build. Todo debe pasar (salvo la línea base).
   Corre también el escaneo de secretos sobre todo el diff de la spec.
4. Marca cada criterio `CA` de la spec como `[x]` solo si su test pasa.
5. **T092:** cambia la spec a `status: implemented` y actualiza `docs/specs/README.md`.

## Paso 6 — Informe

Entrega al usuario, sin recapitular cada tarea:
- Tareas completadas / totales, y las añadidas durante la implementación.
- Resultado de tests, lint y build (y la línea base, si había).
- Notas relevantes y deuda anotada en el roadmap.
- Commits creados y la rama.
- Si se detuvo antes de terminar: en qué tarea y por qué.

Siguiente paso sugerido: `/review NNN`.

## Reanudación

`/implement` siempre retoma desde `tasks.md`: la primera tarea sin marcar con dependencias
cumplidas. Antes de continuar una sesión anterior, verifica que la última tarea marcada realmente
pase sus tests; si no, desmárcala y repítela.
