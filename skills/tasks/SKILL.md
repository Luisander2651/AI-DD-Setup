---
name: tasks
description: Divide un plan aprobado en tareas pequeñas, ordenadas y verificables (tasks.md). Úsala con /tasks NNN o cuando el usuario pida desglosar un plan en tareas.
---

# /tasks — De plan a tareas ejecutables

Cuarto paso del flujo:

```
/init → /specify → /plan → [/tasks] → /implement → /review → /release
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Convierte un plan aprobado en una lista de tareas que `/implement` pueda ejecutar **una por una,
sin tener que tomar decisiones de diseño**. Si una tarea obliga a decidir algo que el plan no dice,
el problema está en el plan.

## Uso

```
/tasks <NNN|slug>
/tasks                  # toma el plan approved más antiguo sin tasks.md
/tasks <NNN> --redo     # regenera conservando las tareas ya hechas
```

## Reglas

- **No escribas código** ni modifiques la spec o el plan.
- **Cada tarea es pequeña:** toca de 1 a 3 archivos y se completa en una sesión corta. Si no,
  divídela.
- **Cada tarea es verificable:** tiene un criterio de hecho observable (un test que pasa, un
  comando que funciona, un archivo que existe con cierto contenido).
- **Nada fuera del plan.** Si falta algo para cumplir la spec, detente y sugiere `/plan --redo`.
- **Nunca apruebes por tu cuenta.** `tasks.md` nace en `draft`.
- Escribe en el idioma del proyecto.

---

## Paso 0 — Precondiciones

1. Si no existe `.ai/project.yaml`, detente y sugiere `/init`.
2. La spec debe estar `approved` y su `plan.md` en `status: approved`.
   - Plan en `draft` → sugiere aprobarlo.
   - Plan en `blocked` → detente: hay una violación de la constitución sin resolver.
3. Si ya existe `tasks.md` y no vino `--redo`, muestra su avance y pregunta si regenerarlo.

## Paso 1 — Contexto

Lee la spec (criterios `CA1`, `CA2`…), el plan completo (Cambios por módulo, Contratos y datos,
Estrategia de pruebas, Trazabilidad, Rollout, Impacto en arquitectura), `docs/constitution.md`
(sobre todo la estrategia de testing) y `.ai/project.yaml`. Usa la plantilla de
`docs/templates/tasks.md`.

## Paso 2 — Desglose

Genera tareas a partir del plan, en este orden de fases:

| Fase | Contenido | Fuente en el plan |
|---|---|---|
| Preparación | Dependencias, configuración, flags, migración *expand* | Decisiones, Rollout |
| Tests | Tests que fallan y describen el comportamiento esperado | Trazabilidad, Estrategia de pruebas |
| Implementación | Cambios en código, módulo por módulo | Cambios por módulo, Contratos y datos |
| Integración y documentación | Cableado final, T090–T092 | Impacto en arquitectura |
| Despliegue | T095–T098 (las ejecuta `/release`) | Rollout |

**Seguridad:** por cada amenaza `TM#` del plan, una tarea de test (en la fase Tests) y una de
control (en Implementación); por cada `CA (abuso)`, al menos un test. Los controles no se agrupan
en una tarea genérica tipo "añadir seguridad": cada uno va junto al módulo que protege.

**Orden de tests e implementación:**
- Si la constitución exige TDD: cada tarea de implementación depende de la tarea de test que
  cubre su criterio, y el test se escribe primero.
- Si no: el test puede ir en la misma tarea que la implementación, pero nunca después de la fase
  de Integración.

**Specs con varias historias de usuario:** si las historias pueden entregarse por separado,
agrupa Tests e Implementación por historia (`### Historia 1: …`), de modo que al terminar cada
grupo haya algo funcionando y probado.

**Formato de cada tarea:**

```
- [ ] T012 [P] <verbo + qué> — <archivos> — hecho cuando: <criterio> — cubre: CA2 — depende: T010
```

- `T###`: T001–T089 para el trabajo; **T090–T099 están reservadas** para las tareas fijas de la
  plantilla. Si necesitas más de 89 tareas, la spec es demasiado grande: sugiere dividirla.
- `[P]`: solo si no comparte archivos con otra tarea abierta y no depende de una tarea sin hacer.
- `cubre`: los criterios de aceptación que la tarea ayuda a cumplir (omitir en tareas de soporte).
- `depende`: solo si hay dependencia real; si no, se asume el orden de la lista.

## Paso 3 — Cobertura

Construye y comprueba estas dos tablas (van al final de `tasks.md`):

```markdown
## Cobertura
| Criterio | Tarea(s) de test | Tarea(s) de implementación |
|---|---|---|
| CA1 | T010 | T020, T021 |

| Cambio del plan (módulo) | Tarea(s) |
|---|---|
| src/notifications | T020, T022 |
```

- Todo `CA` de la spec necesita al menos una tarea de test y una de implementación.
- Todo módulo de "Cambios por módulo" necesita al menos una tarea.
- Toda amenaza `TM#` necesita una tarea de control y una de test (tabla de amenazas de la plantilla).
- Toda tarea de implementación debe poder rastrearse a un cambio del plan. Si no, sobra o el plan
  está incompleto.

## Paso 4 — Constitution Check

Revisa las tareas contra cada principio (no repitas el análisis del plan; busca lo que el
desglose pudo romper). Ejemplos: una tarea que agrega una dependencia sin su ADR, tests puestos
después de la implementación cuando se exige TDD, una migración destructiva antes del deploy.
Registra el resultado en la sección "Constitution Check" con el mismo formato que el plan
(✅ / ➖ / ❌). Un ❌ se corrige reordenando o dividiendo tareas; si no se puede, detente.

## Paso 5 — Autoverificación

- [ ] Todas las tareas tienen archivos y criterio de hecho.
- [ ] Ninguna tarea toca más de 3 archivos.
- [ ] Las marcas `[P]` no comparten archivos entre sí.
- [ ] No hay dependencias circulares.
- [ ] Tablas de cobertura completas.
- [ ] T090–T098 presentes.
- [ ] Cada `TM#` y cada `CA (abuso)` con sus tareas.

## Paso 6 — Escritura y aprobación

1. Escribe `docs/specs/NNN-<slug>/tasks.md` con `status: draft`.
2. Muestra al usuario: número de tareas por fase, cuántas son paralelizables, la ruta crítica
   (cadena de dependencias más larga) y cualquier tarea de riesgo alto.
3. Pregunta si lo aprueba:
   - **Aprueba** → `status: approved`.
   - **Pide cambios** → aplica, repite el Paso 5 y vuelve a preguntar.

Siguiente paso sugerido: `/implement NNN`.

---

## Modo `--redo`

- Conserva tal cual las tareas marcadas `[x]` y su número.
- Las tareas pendientes que ya no tengan sentido con el nuevo plan se eliminan; las nuevas toman
  números libres (nunca reutilices un número de una tarea eliminada).
- Si una tarea hecha contradice el nuevo plan, añade una tarea para revertirla o adaptarla y
  avísale al usuario.
- Guarda la versión anterior como `tasks.v<N>.md`.
