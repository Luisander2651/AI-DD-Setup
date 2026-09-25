---
name: "plan"
description: "Genera el plan técnico de una spec aprobada (plan.md con Constitution Check, trazabilidad y Rollout). Úsala con /plan NNN o cuando el usuario pida diseñar cómo implementar una spec."
---

# /plan — De spec a diseño técnico

Tercer paso del flujo:

```
/init → /specify → [/plan] → /tasks → /analyze → /implement → /review → /release
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Decide **cómo** se implementa una spec aprobada, respetando la constitución, la arquitectura y la
forma de desplegar del proyecto. No escribe código.

## Uso

```
/plan <NNN|slug>
/plan                 # toma la spec approved más antigua sin plan.md
/plan <NNN> --fix A3,A7   # corrige solo lo que piden esos hallazgos de /analyze (lo habitual)
/plan <NNN> --redo        # regenera el plan completo (solo cambios estructurales)
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
3. Si ya existe `plan.md` y no vino `--redo` ni `--fix`, muestra su estado y pregunta si
   corregirlo (`--fix`) o regenerarlo (`--redo`).
4. **Tamaño.** Si la spec tiene más de ~10 criterios, extiende más de 4 specs, o tras leer el
   código resulta que toca más de 3 módulos o ~25 archivos, **propón dividirla antes de diseñar**
   (muestra el corte: qué capacidades van en cada spec y cuáles se pueden liberar por separado).
   Una spec grande multiplica las vueltas de `/plan` y `/analyze`. Si el usuario decide seguir,
   regístralo en Decisiones como `(decisión del usuario, fecha)`.
5. Lee `docs/constitution.md`. Si está en `draft`, avisa que el Constitution Check se hará contra
   una constitución no aprobada y continúa.

## Paso 1 — Contexto

Lee:
- La spec completa, incluidas "Supuestos" y "Notas para /plan".
- `.ai/project.yaml`: tipo, stack, `deploy`, `skills.enabled`.
- `docs/constitution.md`, `docs/architecture.md`, `docs/deployment.md`, `docs/security.md`,
  `docs/observability.md`.
- `../../shared/security-checklist.md` (relativo a este archivo) para el modelo de amenazas.
- ADRs vigentes en `docs/adr/` (ignora los `superseded`).
- Planes de specs relacionadas o que esta extiende.
**Línea base de dependencias:** ejecuta la herramienta SCA de `.ai/project.yaml → security.tools`
(p. ej. `npm audit`, `composer audit`, `pip-audit`). Si ya hay vulnerabilidades críticas o altas sin
excepción vigente en `docs/security.md`, **no son de esta spec pero bloquearán `/release`**:
llévalas al Paso 2b (actualizar dentro de esta spec, o excepción con motivo, aprobador y
vencimiento, con su riesgo `RS`). Descubrirlas en `/review` cuesta una ronda más.

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
- **Toda dependencia nueva** pasa la verificación de `../../shared/agent-security.md` §2 (existe,
  antigüedad, reputación, licencia, scripts de instalación) **antes** de proponerla. Registra el
  resultado en la decisión. Si no se puede verificar, no la propongas: pregunta.

## Paso 2b — Decisiones pendientes del usuario

Antes de escribir el plan, reúne **todo** lo que solo el usuario puede decidir y pregúntalo en una
sola ronda (hasta ~6 preguntas, opción múltiple con una recomendada). Cada una descubierta después,
en `/analyze`, cuesta una vuelta completa. Busca en particular:

- **Constitución:** un principio que el diseño no puede cumplir tal cual o que no encaja con el caso
  (¿excepción, enmienda PATCH o cambio de diseño?). Ejemplo: tests de acceso por actor en rutas cuya
  autorización no cambia.
- **Conflictos con otras specs en curso:** cruza los archivos que tocará este plan con los de los
  planes y specs `approved` o `draft` (sección "Cambios por módulo" y "Notas para /plan"). Si
  comparten archivos o contratos, pregunta el orden y qué comportamiento esperar tras la otra.
- **Alcance:** correcciones de riesgos, criterios de specs extendidas o casos límite que el diseño
  obliga a incluir o dejar fuera.
- **Contratos visibles:** textos de error, códigos HTTP o formatos que cambian respuestas que hoy
  asertan tests existentes o consumen clientes.
- **Vulnerabilidades previas** de la línea base de dependencias (Paso 1).
- **Preferencias técnicas** con dos opciones razonables.

Registra cada respuesta en Decisiones con `(decisión del usuario, AAAA-MM-DD)`. Si algo requiere
cambiar la spec, detente y sugiere `/specify --edit` antes de seguir.

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
- **Si cambian permisos o roles** y hay interfaz: una tabla **"Qué ve cada rol"** por pantalla
  afectada (saludos y textos, menús, columnas, botones y enlaces, estados vacíos). Ocultar un
  control no basta: los textos que prometen una acción ("gestiona", "ver y editar"), las columnas
  que quedan vacías y los mensajes pensados para otro rol también cambian, y cada fila lleva su
  test. Es la fuente habitual de hallazgos de `/review` en specs de control de acceso.
- `fullstack` / `monorepo`: dónde vive el contrato compartido y cómo se regenera.
- `library`: cambios en la API pública y su impacto en SemVer (patch, minor o major).
Añade siempre esta sección, aunque la plantilla no la traiga:

```markdown
## Trazabilidad
| Criterio de aceptación | Cambio(s) | Test(s) |
|---|---|---|
| CA1: <resumen> | <módulo> | <tipo y nombre del test> |
```

Todo criterio de la spec (incluidos los `(abuso)`) y toda amenaza `TM#` deben aparecer. Un criterio
o amenaza sin test es un error del plan.

## Paso 3a — Observabilidad

Completa la sección "Observabilidad" del plan. **Obligatoria** si la spec toca datos sensibles,
autenticación o permisos; en otro caso, una línea con el motivo.
- **Logs** que la feature añade: evento, nivel y campos, siempre con `request_id` y sin datos
  sensibles (reglas de `docs/observability.md`).
- **Eventos de auditoría:** uno por cada criterio de la sección "Auditoría" de la spec, con dónde
  se emite y el test que verifica que se registra (va también a Trazabilidad).
- **Métricas y alertas** nuevas o afectadas.
- **Verificación post-deploy:** qué consulta o dashboard demuestra que funciona.

Si `docs/observability.md` marca como *presente* pero no *en uso* una capacidad que la feature
necesita (p. ej. no hay correlación ni registro de auditoría), inclúyela en el plan como
prerrequisito o detente y sugiere una spec previa.

## Paso 3b — Modelo de amenazas

**Obligatorio** si la spec toca datos sensibles, autenticación, permisos, pagos, archivos subidos,
URLs o entradas externas nuevas. Si no aplica, escribe una línea con el motivo y continúa.

1. Dibuja mentalmente el flujo de datos de la feature: actores, puntos de entrada, datos que
   cruzan límites de confianza (navegador → API, API → base de datos, API → terceros).
2. Por cada punto de entrada y cada límite, aplica **STRIDE**: suplantación, manipulación,
   repudio, divulgación de información, denegación de servicio, elevación de privilegios.
3. Contrasta con los temas de `shared/security-checklist.md` que apliquen y mapea cada amenaza a
   su categoría del OWASP Top 10 (edición de `docs/security.md`). Para APIs, revisa también el API
   Security Top 10; si la feature usa LLMs, el Top 10 para LLM.
4. Por cada amenaza real (no teórica para este contexto): un **control** concreto en el diseño y un
   **test** que lo verifique (p. ej. "usuario B no puede leer el recurso de A → 404").
5. Cada caso de abuso de la spec debe quedar cubierto por al menos una amenaza `TM#`.
6. Registra todo en la tabla "Modelo de amenazas" del plan y añade los tests a Trazabilidad.

Si un control requiere una dependencia nueva (librería de rate limiting, WAF, etc.), va a
Decisiones y se marca → ADR.

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
- [ ] Observabilidad completa (o motivo de no aplicar); cada criterio de Auditoría con su test.
- [ ] Riesgos: el plan nunca dice que un riesgo queda "mitigado" si la spec deja alguna de sus
      correcciones fuera; habla por corrección ("RS1.a y RS1.d mitigadas; RS1.b y RS1.c
      pendientes → destino"). Las decisiones de diseño que cubren una corrección de forma
      indirecta (p. ej. un middleware que compensa un provider sin fijar) se registran en
      Decisiones con el ID de la corrección y su estado.
- [ ] Modelo de amenazas completo (o motivo de no aplicar); cada `TM#` con control y test; cada
      `CA (abuso)` cubierto.
- [ ] No se modificó la spec.
- [ ] Tras escribir el plan, `python .ai/bin/aidd.py validate docs/specs/NNN-<slug>` (o `python3`) sin errores.

## Paso 8 — Escritura y aprobación

1. Escribe `docs/specs/NNN-<slug>/plan.md` con `status: draft`.
2. Muestra al usuario: enfoque en 2–3 frases, módulos afectados, decisiones clave, resultado del
   Constitution Check (conteo ✅/➖/❌), ADRs propuestos y riesgos principales.
3. Pregunta si lo aprueba:
   - **Aprueba** → `status: approved` en el plan; los ADRs `proposed` pasan a `accepted`.
   - **Pide cambios** → aplica, repite el Paso 7 y vuelve a preguntar.
Siguiente paso sugerido: `/tasks NNN`.

---

## Modo `--fix <IDs>`

Corrige solo lo que piden los hallazgos indicados de `analysis.md` (o todos los abiertos si no se
indican IDs). Es la forma normal de responder a `/analyze`.

1. Para cada hallazgo, identifica la sección o las líneas del plan afectadas y **edítalas en su
   lugar**. No regeneres el resto del plan ni cambies redacción que no está en juego.
2. Si la corrección toca otra parte (p. ej. un cambio en Contratos que afecta a Trazabilidad o al
   Constitution Check), actualiza también esas referencias, y solo esas.
3. Si un hallazgo requiere una decisión del usuario, pregúntala primero (Paso 2b).
4. Muestra al usuario el diff por hallazgo y un resumen: hallazgo → cambio.
5. Lista las tareas afectadas y sugiere `/tasks NNN --fix <IDs>`, no `--redo`.
6. Repite la autoverificación (Paso 7) y el validador. El plan vuelve a `draft` si estaba
   `approved`, y se aprueba de nuevo.

Si al corregir descubres que el cambio es estructural (nuevo módulo, nuevo contrato, otro enfoque),
detente y propone `--redo`.

## Modo `--redo`

- Si existe `tasks.md` con tareas marcadas como hechas, avisa que regenerar el plan puede dejar
  código implementado fuera del nuevo diseño y pide confirmación.
- **Versión anterior:** antes de regenerar, archívala con
  `python .ai/bin/aidd.py rotate docs/specs/NNN-<slug> plan` (copia a `history/plan.v<N>.md`). Las
  versiones archivadas no se borran, tampoco en un upgrade; ninguna skill las lee.
- Tras aprobar el nuevo plan, `tasks.md` queda desactualizado: sugiere `/tasks NNN --redo`, o
  `--fix` si las tareas afectadas son pocas.
