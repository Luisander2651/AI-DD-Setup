---
name: "plan"
description: "Genera el plan técnico de una spec aprobada (plan.md con Constitution Check, trazabilidad y Rollout). Úsala con /plan NNN o cuando el usuario pida diseñar cómo implementar una spec."
---

# /plan — De spec a diseño técnico

Tercer paso del flujo:

```
/init → /specify → [/plan] → /tasks → /implement → /review → /release
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Decide **cómo** se implementa una spec aprobada, respetando la constitución, la arquitectura y la
forma de desplegar del proyecto. No escribe código.

## Uso

```
/plan <NNN|slug>
/plan                 # toma la spec approved más antigua sin plan.md
/plan <NNN> --redo    # regenera un plan existente
```

## Reglas

- **No escribas código** ni crees `tasks.md`. Fragmentos de firma, esquema o contrato sí están
  permitidos cuando aclaran una decisión.
- **La constitución manda.** Un principio violado sin justificación aceptada por el usuario
  bloquea el plan.
- **Cada criterio de aceptación de la spec queda cubierto** por al menos un cambio y un test.
- **No cambies la spec.** Si el plan revela que la spec está mal o incompleta, detente y sugiere
  `/specify --edit`.
- **Nunca apruebes por tu cuenta.** El plan nace en `draft`.
- Escribe en el idioma del proyecto.
---

## Paso 0 — Precondiciones

1. Si no existe `.ai/project.yaml`, detente y sugiere `/init`.
2. Localiza la spec. Comprueba:
   - `status: approved`. Si está en `draft` o `inferred`, detente y sugiere aprobarla con
     `/specify --edit`.
   - Sin marcadores `[NECESITA ACLARACIÓN]`. Si hay, detente.
3. Si ya existe `plan.md` y no vino `--redo`, muestra su estado y pregunta si regenerarlo.
4. Lee `docs/constitution.md`. Si está en `draft`, avisa que el Constitution Check se hará contra
   una constitución no aprobada y continúa.
## Paso 1 — Contexto

Lee:
- La spec completa, incluidas "Supuestos" y "Notas para /plan".
- `.ai/project.yaml`: tipo, stack, `deploy`, `skills.enabled`.
- `docs/constitution.md`, `docs/architecture.md`, `docs/deployment.md`.
- ADRs vigentes en `docs/adr/` (ignora los `superseded`).
- Planes de specs relacionadas o que esta extiende.
**Código existente:** identifica los módulos que la feature probablemente toca y léelos. Si son
muchos o no está claro dónde encaja, lanza **un** subagente de solo lectura con este encargo:

> Para implementar "<resumen de la spec>" en `<root>`, identifica: módulos y archivos que habría
> que modificar, patrones existentes que deben seguirse (con un ejemplo por patrón), código
> reutilizable, tests existentes relacionados y riesgos de romper otras features. Devuelve rutas
> concretas y nivel de confianza. No modifiques nada.

## Paso 2 — Decisiones

Lista las incógnitas técnicas (cómo guardar X, qué librería para Y, dónde vive Z). Para cada una:
- Opciones reales (2–3), con pros y contras breves.
- Decisión y motivo, preferentemente alineada con lo que ya usa el proyecto.
- Si la decisión introduce una dependencia nueva, cambia la arquitectura o contradice un ADR,
  márcala como **→ ADR**.
Si una decisión depende de una preferencia del usuario y ambas opciones son razonables, pregúntale
antes de seguir (máximo 3 preguntas, en una ronda).

## Paso 3 — Diseño

Completa `docs/templates/plan.md`. Guía por sección:

| Sección | Contenido |
|---|---|
| Enfoque técnico | 3–6 frases: la idea central del diseño y por qué. |
| Cambios por módulo | Tabla módulo → cambio → riesgo. Rutas reales del repo. |
| Contratos y datos | Según tipo (ver abajo). |
| Estrategia de pruebas | Qué se prueba, a qué nivel (unit, integración, e2e) y con qué herramienta del proyecto. |
| Rollout | Según `docs/deployment.md` (ver Paso 5). |
| Decisiones | Las del Paso 2, las marcadas → ADR incluidas. |
| Riesgos y mitigaciones | Técnicos, de datos, de performance, de seguridad. |

**Contratos y datos según `project.type`:**
- `backend` / `fullstack`: endpoints o mensajes (método, ruta, request, response, errores),
  cambios de modelo de datos y migraciones (patrón expand → migrate → contract), permisos.
- `frontend` / `fullstack`: pantallas y componentes nuevos o modificados, estados (carga, vacío,
  error, éxito), manejo de estado, accesibilidad. Si `design` está en `skills.enabled`, añade la
  nota: "Revisar con la skill `design` antes de `/implement`".
- `fullstack` / `monorepo`: dónde vive el contrato compartido y cómo se regenera.
- `library`: cambios en la API pública y su impacto en SemVer (patch, minor o major).
Añade siempre esta sección, aunque la plantilla no la traiga:

```markdown
## Trazabilidad
| Criterio de aceptación | Cambio(s) | Test(s) |
|---|---|---|
| CA1: <resumen> | <módulo> | <tipo y nombre del test> |
```

Todo criterio de la spec debe aparecer. Un criterio sin test es un error del plan.

## Paso 4 — Constitution Check

Evalúa **cada** principio de la constitución, sin omitir ninguno:

| Resultado | Cuándo |
|---|---|
| ✅ Cumple | Indica cómo (evidencia en el plan). |
| ➖ No aplica | Indica por qué. |
| ❌ Viola | Explica la violación. |

Ante un ❌:
1. Intenta rediseñar para cumplir. Si lo logras, cambia a ✅.
2. Si no es posible, presenta al usuario la violación, la justificación y la alternativa más
   cercana. Solo con su aceptación explícita queda como `❌ aceptado: <motivo> — aprobado por el
   usuario el <fecha>`.
3. Sin aceptación, el plan queda en `status: blocked` y te detienes.
Si una violación se repite en varios planes, sugiere al usuario enmendar la constitución en lugar
de seguir aceptando excepciones.

## Paso 5 — Rollout

Basado en `docs/deployment.md` y `.ai/project.yaml → deploy`:
- **Feature flag:** obligatorio si la feature cambia un flujo existente o es de riesgo medio/alto.
- **Orden de despliegue:** p. ej. migración expand → backend → frontend → migración contract.
- **Compatibilidad:** ¿convive con la versión anterior durante el deploy?
- **Rollback:** pasos concretos. Si hay migración, cómo se revierte o por qué no hace falta.
- **Métricas a vigilar** tras el deploy.
Si `deploy.strategy` es `none`, escribe "Sin despliegue configurado" y solo registra lo que
habría que considerar al configurarlo.

## Paso 6 — Impacto en arquitectura

- Por cada decisión marcada → ADR, crea `docs/adr/NNNN-<slug>.md` desde la plantilla con
  `status: proposed` y enlázalo desde el plan.
- **No edites** `docs/architecture.md` todavía: los cambios de arquitectura se reflejan cuando la
  feature se implementa (tarea T090 de `/tasks`). Lista en el plan qué secciones habrá que
  actualizar.
## Paso 7 — Autoverificación

- [ ] Todos los criterios de aceptación están en Trazabilidad con cambio y test.
- [ ] Todos los principios de la constitución están en el Constitution Check.
- [ ] Ningún ❌ sin aceptación explícita.
- [ ] Las rutas de "Cambios por módulo" existen, o están marcadas como nuevas.
- [ ] Las dependencias nuevas tienen ADR.
- [ ] Rollout completo o justificado como no aplicable.
- [ ] No se modificó la spec.
## Paso 8 — Escritura y aprobación

1. Escribe `docs/specs/NNN-<slug>/plan.md` con `status: draft`.
2. Muestra al usuario: enfoque en 2–3 frases, módulos afectados, decisiones clave, resultado del
   Constitution Check (conteo ✅/➖/❌), ADRs propuestos y riesgos principales.
3. Pregunta si lo aprueba:
   - **Aprueba** → `status: approved` en el plan; los ADRs `proposed` pasan a `accepted`.
   - **Pide cambios** → aplica, repite el Paso 7 y vuelve a preguntar.
Siguiente paso sugerido: `/tasks NNN`.

---

## Modo `--redo`

- Si existe `tasks.md` con tareas marcadas como hechas, avisa que regenerar el plan puede dejar
  código implementado fuera del nuevo diseño y pide confirmación.
- Conserva el plan anterior como `plan.v<N>.md` antes de sobrescribir.
- Tras aprobar el nuevo plan, `tasks.md` queda desactualizado: sugiere `/tasks NNN --redo`.