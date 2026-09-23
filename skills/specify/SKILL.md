---
name: "specify"
description: "Crea o modifica una spec (qué y por qué, sin cómo) en docs/specs/NNN-slug/spec.md. Úsala con /specify o cuando el usuario describa una feature nueva en un proyecto inicializado con /init."
---

# /specify — De idea a especificación

Segundo paso del flujo:

```
/init → [/specify] → /plan → /tasks → /implement → /review → /release
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Convierte una idea en una spec clara, verificable y **libre de decisiones técnicas**. La spec
responde *qué* y *por qué*; el *cómo* es trabajo de `/plan`.

## Uso

```
/specify <descripción de la feature>
/specify --from <ruta a archivo o texto de issue>
/specify --edit <NNN|slug>        # modificar una spec existente
```

## Reglas

- **Sin tecnología.** Prohibido mencionar frameworks, lenguajes, endpoints, tablas, librerías o
  estructura de código. Si el usuario los menciona, guárdalos en "Notas para /plan" y no los uses
  en el resto de la spec.
- **Todo criterio de aceptación es verificable.** Formato Dado / Cuando / Entonces, con resultado
  observable. "Debe ser rápido" no vale; "responde en < 2 s para 95 % de las búsquedas" sí.
- **No inventes requisitos.** Lo que no se sepa se pregunta o se marca como supuesto.
- **Nunca apruebes por tu cuenta.** La spec nace en `draft`; solo el usuario la pasa a `approved`.
- **No escribas código** ni crees `plan.md` o `tasks.md`.
- Escribe en el idioma del proyecto (el de `AGENTS.md`).
---

## Paso 0 — Precondiciones

1. Si no existe `.ai/project.yaml`, detente y sugiere ejecutar `/init`.
2. Lee `docs/constitution.md`. Si su `status` es `draft`, avisa en una línea que la constitución
   aún no está aprobada y continúa.
3. Localiza la plantilla en `.ai/project.yaml → paths.templates` (por defecto
   `docs/templates/spec.md`). Si no existe, detente y sugiere `/init` en modo re-sincronizar.
## Paso 1 — Contexto

Lee, en este orden y solo lo necesario:
- `.ai/project.yaml` (tipo de proyecto, etapa).
- `docs/constitution.md` (principios y restricciones que afectan requisitos: accesibilidad,
  compliance, performance).
- `docs/roadmap.md` (¿esta feature está en los objetivos?).
- `docs/security.md` (clasificación de datos y modelo de permisos), si existe.
- `docs/specs/README.md` y los títulos de las specs existentes.
- `docs/architecture.md` solo para entender el dominio y el glosario, **no** para diseñar.
## Paso 2 — Duplicados y tamaño

1. **Duplicados:** si una spec existente cubre total o parcialmente la idea, muéstrala y pregunta:
   (a) modificar esa spec (`--edit`), (b) crear una nueva que la extienda, (c) cancelar.
2. **Tamaño:** una spec debe poder entregarse de forma independiente. Si la idea contiene varias
   capacidades que se pueden liberar por separado (señal: > 6 historias de usuario, o historias sin
   relación entre sí), propone dividirla y lista las specs resultantes. Crea solo las que el
   usuario confirme, una por una.
## Paso 3 — Identificador

- `NNN` = siguiente número libre en `docs/specs/`, con 3 dígitos (`001`, `002`…). Nunca reutilices
  un número, aunque la carpeta se haya borrado (revisa también `docs/specs/README.md`).
- `slug` = 2–4 palabras en kebab-case, sin artículos (`notificaciones-push`, no
  `las-notificaciones-push-del-usuario`).
## Paso 4 — Borrador

Completa la plantilla. Guía por sección:

| Sección | Cómo llenarla |
|---|---|
| Problema | Situación actual, a quién afecta y qué pasa si no se resuelve. 2–4 frases. |
| Historias de usuario | "Como <rol>, quiero <acción> para <beneficio>". Roles reales del dominio, no "usuario" genérico si hay más precisión. |
| Criterios de aceptación | Al menos uno por historia, más los casos límite: vacío, error, permisos, límites. |
| Fuera de alcance | Lo que alguien razonablemente esperaría y **no** se hará. Nunca vacía. |
| Seguridad y privacidad | Qué datos sensibles toca (según la clasificación de `docs/security.md`), quién puede hacer qué, y **casos de abuso**: "Como atacante/usuario malintencionado, intento X → se rechaza/limita/registra". Cada caso de abuso genera un criterio `CA` marcado `(abuso)`. Sin tecnología: describe el comportamiento, no el mecanismo. Si la feature no toca datos sensibles, permisos ni entradas externas, escribe "No aplica" y el motivo. |
| Requisitos no funcionales | Solo los que apliquen, medibles. Incluye los que exija la constitución según el tipo (p. ej. WCAG AA en frontend). |
| Preguntas abiertas | Marcadores `[NECESITA ACLARACIÓN]`. **Máximo 3.** |

Añade al final, si hacen falta, estas dos secciones aunque la plantilla no las traiga:

```markdown
## Supuestos
- <decisión razonable tomada sin preguntar, para que el usuario la revise>

## Notas para /plan
- <preferencias técnicas que mencionó el usuario; no son requisitos>
```

**Límite de preguntas:** si hay más de 3 dudas, conserva como `[NECESITA ACLARACIÓN]` solo las
que cambian el alcance, la seguridad o la experiencia del usuario. Las demás se resuelven con un
valor razonable registrado en "Supuestos".

## Paso 5 — Aclaración

Si quedan marcadores `[NECESITA ACLARACIÓN]`, hazle esas preguntas al usuario (opción múltiple
cuando se pueda, todas en una sola ronda). Incorpora las respuestas y elimina los marcadores.
Si el usuario no responde o la sesión es desatendida, deja los marcadores: la spec no podrá
aprobarse con marcadores abiertos.

## Paso 6 — Autoverificación

Antes de escribir, confirma cada punto; corrige lo que falle:

- [ ] Ninguna mención de tecnología fuera de "Notas para /plan".
- [ ] Cada historia tiene al menos un criterio de aceptación.
- [ ] Cada criterio es observable y verificable por un test o una persona.
- [ ] Hay al menos un caso de error o límite.
- [ ] "Fuera de alcance" tiene contenido.
- [ ] No contradice ningún principio de la constitución.
- [ ] Máximo 3 `[NECESITA ACLARACIÓN]`.
- [ ] Si toca datos sensibles, permisos o entradas externas: al menos un caso de abuso con su
      `CA (abuso)` (acceso a datos de otro usuario, entradas maliciosas, abuso de volumen…).
## Paso 7 — Escritura

1. Crea `docs/specs/NNN-<slug>/spec.md` con `status: draft` y la fecha de hoy.
2. Añade una fila en `docs/specs/README.md` (créalo si no existe):
   `| NNN | [nombre](NNN-slug/spec.md) | draft | fecha |`.
3. Si la feature corresponde a un objetivo de `docs/roadmap.md`, enlaza la spec en la columna
   "Spec" de ese objetivo.
## Paso 8 — Aprobación

Muestra al usuario un resumen: problema en una frase, historias, número de criterios, supuestos y
preguntas abiertas. Pregunta si la aprueba.
- **Aprueba y no hay marcadores abiertos** → `status: approved`, actualiza el README.
- **Pide cambios** → aplica, repite el Paso 6 y vuelve a preguntar.
- **Hay marcadores abiertos** → no puede aprobarse; indícalo.
Siguiente paso sugerido: `/plan NNN`.

---

## Modo `--edit`

1. Lee la spec y su `status`.
2. Si está en `implemented` o `released`, **no la modifiques**: propone crear una spec nueva que
   la extienda y enlázalas entre sí ("Extiende: NNN").
3. Si está en `approved` y ya existe `plan.md`, avisa que el cambio invalida el plan: la spec
   vuelve a `draft` y el plan deberá regenerarse con `/plan`.
4. Registra el cambio al final de la spec:
   ```markdown
   ## Historial
   | Fecha | Cambio | Motivo |
   |---|---|---|
   ```
5. Repite los Pasos 6 a 8.
## Specs inferidas por /init

Si la spec tiene `status: inferred`, `/specify --edit` sirve para validarla: revisa con el usuario
la sección "Observaciones", decide qué es requisito real y qué es deuda, y al aprobarla cambia a
`approved`. Elimina `confidence` al aprobar.