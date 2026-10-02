# Plan — Diseño en `/init` con `design` (1.11.0)

**Estado:** implementado en 1.11.0 (2026-10-02), salvo la prueba de punta a punta (§12, paso 6). Decisiones en §9.
**Origen:** la prueba 8.13 ("Mi Presión" llegó a `/release` con los componentes de Ionic por
defecto y los campos del formulario pegados al borde, sin ninguna fase de diseño) y la skill
`design-spec` del portafolio personal (sistema de diseño aprobado antes de la primera pantalla,
2–3 direcciones, diseño enlazado desde cada spec), leída en `.claude/skills/design-spec/`.

## 1. Objetivo

Que todo proyecto con interfaz (`frontend`, `fullstack`, `mobile`) tenga, cuando el usuario lo
quiera:

1. Un **sistema de diseño escrito**, `docs/design/system.md`: tokens, tipografía, componentes con
   estados, patrones y pantallas principales, con el contraste calculado.
2. Un **HTML principal**, `docs/design/system.html`: la página visual de ese sistema. Es un archivo
   del repo que se abre cuantas veces se quiera, sin red ni sesión.
3. Reglas para que `/specify`, `/plan`, `/tasks`, `/implement` y `/review` trabajen **sobre** ese
   sistema y no lo reinventen en cada spec.

| Caso | Qué hace |
|---|---|
| Greenfield con interfaz | Entrevista de diseño y **3 opciones en HTML** (2 si el usuario ya trae marca); la elegida pasa a ser el sistema |
| Brownfield con interfaz | **Solo si el usuario acepta:** documenta el diseño existente (extracción, auditoría y HTML del sistema actual). No propone ni genera rediseños |
| Rediseño | Siempre **spec propia** (`/specify` → `/plan` con el paso de diseño del §6), nunca dentro de `/init` |
| `/init --upgrade` | Solo la documentación del diseño existente, si el usuario acepta (§7) |

## 2. Las dos dependencias de diseño (comprobado)

En la sesión aparecen dos cosas distintas con el nombre `design`:

| Qué | Qué hace | Uso en el flujo |
|---|---|---|
| **Skill `design`** (crear un artifact Design a partir de un brief; la que usa `design-spec` del portafolio con la herramienta `Skill` y un brief en `args`) | Genera el canvas visual con direcciones y artboards | Generar las opciones y el sistema cuando la sesión la ofrece |
| **Plugin `design` de Anthropic** (`anthropics/knowledge-work-plugins`, v1.2.0): `design-system`, `design-critique`, `accessibility-review`, `design-handoff`, `ux-copy`… | Trabaja con texto, capturas o Figma; **no genera visuales** | Auditar y documentar el sistema, criticar y revisar accesibilidad de las opciones, handoff en `/plan`, review |

**Decisión: el HTML es siempre el entregable.** Si la sesión ofrece la skill `design`, se le pasa el
brief del §5 y se guarda en `docs/design/` una copia HTML del resultado (se lee el artifact
publicado; si no se puede, se genera el HTML desde el mismo brief) y el enlace del canvas queda en
`system.md` para hacer retoques finos. Sin la skill `design`, el HTML se genera directamente desde el
brief con la plantilla `design-option.html`. Sin el plugin de Anthropic se usan las guías propias
(contraste calculado, estados mínimos) y se avisa una vez (contrato → "Dependencias externas").

## 3. Lo que se crea en el proyecto

```
docs/design/
  brief.md                 ← respuestas de la entrevista (greenfield)
  creative-direction.md    ← dirección creativa fijada (patrón del portafolio)
  anti-cliches.md          ← clichés prohibidos del tipo de proyecto, con alternativa
  system.md                ← sistema de diseño (status: draft | approved; source: chosen | extracted)
  system.html              ← HTML principal del sistema (se abre sin red)
  opciones/opcion-a.html … ← greenfield: las opciones exploradas (se conservan las descartadas)
  capturas/                ← brownfield: pantallas actuales, solo con datos de prueba
```

`.ai/project.yaml`:

```yaml
design:
  status: none             # none | declined | draft | approved
  source: null             # chosen (greenfield) | extracted (brownfield)
  system: docs/design/system.md
  html: docs/design/system.html
  canvas: null             # enlace al canvas si se usó la skill design
  widths: [390, 1440]      # anchos de comprobación (mobile: [360, 412])
```

`declined` registra que el usuario no quiso documentar el diseño, para que `--upgrade` no vuelva a
preguntar.

`system.md` sigue la plantilla `system-template.md` del portafolio, generalizada: Dirección elegida ·
Color (token, valor, uso, contraste sobre su fondo) · Tipografía (familias, pesos, escala móvil y
escritorio) · Espaciado, radios y bordes · Componentes base (anatomía y estados: reposo, hover, foco,
activo, deshabilitado, error, carga; tamaño mínimo de toque) · Tokens y patrones de movimiento (con
versión `prefers-reduced-motion`) · Reglas de uso · Decisiones (tabla con tipo y fuente, como las
specs).

Además:
- **Constitución:** principio propuesto "La interfaz usa solo tokens del sistema de diseño" con
  *Cómo se verifica: test o lint que falla con colores, tamaños o espaciados literales* (práctica 5
  de 1.10.0; en el portafolio mantuvo la coherencia de 15 specs).
- **`AGENTS.md`:** enlaces a `system.md` y `system.html`.
- **Jerarquía de fuentes:** el sistema de diseño ya está en el contrato (1.10.0), por debajo de la
  constitución y de `AGENTS.md`.

## 4. Greenfield: entrevista y opciones

**Fase 2, Ronda 4b "Diseño"** (solo si habrá interfaz; rondas de hasta 4 preguntas con la opción
recomendada primero):
1. Objetivo del diseño y qué debe sentir quien lo usa; público y contexto de uso (prisa, una mano,
   luz exterior, edad).
2. Colores pedidos o marca existente (logo, paleta), y colores que hay que evitar.
3. Tipografía preferida o estilo (geométrica, humanista, monoespaciada para datos); claro u oscuro.
4. Referencias que gustan y que no; intensidad del movimiento; librería de componentes prevista (p.
   ej. Ionic) y cuánto se personaliza.

Lo que responden la constitución o el tipo (nivel WCAG, toque ≥ 44 pt/48 dp en mobile) no se
pregunta: va a las decisiones de `brief.md` como `implícita`. Con las respuestas se escriben
`creative-direction.md` y `anti-cliches.md`, que el usuario aprueba antes de generar nada.

**Opciones:** **3 por defecto; 2 si el usuario ya trae marca y paleta cerradas** (solo cambia la
composición, no el color). Cada opción, con el **contenido real** del proyecto (nombre, textos de la
primera feature del roadmap, nunca lorem ipsum) y en `design.widths`:
- paleta (marca, semánticos, neutros) con **contraste calculado** en cada par texto/fondo;
- tipografía: dos familias como máximo, escala con tamaños y pesos;
- componentes clave: botón (variantes y estados), campo con error, lista o card, modal o aviso,
  estados vacío, carga y error;
- 1–2 pantallas principales;
- una línea de "por qué" y el riesgo asumido.

Las opciones deben ser **distintas de verdad** (no tres tonos de la misma), cumplir la constitución y
evitar `anti-cliches.md`. `design:design-critique` y `design:accessibility-review` revisan cada una
antes de enseñarla; los fallos de contraste se corrigen antes, no se señalan después.

**Elección:** el usuario elige una o combina elementos. `design:design-system document` (o la
plantilla propia) escribe `system.md` con `source: chosen`; la opción elegida, ajustada, pasa a ser
`system.html`; las demás se quedan en `opciones/`. La elección va a Decisiones (tipo `diseño`).

**Fase 3b (proyecto base):** los tokens se escriben en el archivo de tema del stack (variables CSS,
tema de Ionic, `ThemeData`…) dentro de la spec del proyecto base, y la **auditoría de valores por
defecto de la plantilla** (1.9.0) se hace también contra `system.md`: tamaños de control, márgenes de
los campos, colores por defecto. En "Mi Presión" esto habría detectado los botones de 32 px y los
campos sin margen antes de la primera spec.

## 5. Brief para la skill `design`

Mismo esquema que `design-spec` del portafolio, sin nada propio de un portafolio:

```
Proyecto: <nombre> — <descripción de AGENTS.md> (<tipo>, <stack de UI>)
Modo: sistema | spec NNN-slug
Objetivo: <del brief o de la spec>
Dirección creativa: <resumen de docs/design/creative-direction.md>
Sistema de diseño: <tokens clave de system.md, o "a definir" en modo sistema>
Contenido real: <textos y datos exactos de la spec o del roadmap; nunca lorem ipsum>
Artboards:
  - Opciones A, B (y C): claramente distintas entre sí
  - Cada una en <design.widths>
  - Estados: vacío, carga, error, foco, deshabilitado
  - Movimiento como fotogramas anotados (inicio → medio → final), con versión sin movimiento
Restricciones: <constitución: WCAG, toque mínimo, plataforma>; sin clichés de anti-cliches.md;
  solo tokens del sistema (modo spec)
```

En modo sistema los artboards son *style tiles*: paleta, tipografía, escala de espaciado, radios,
botones, campos, cards o listas, avisos y una pantalla principal.

## 6. Brownfield: documentar el diseño existente (si el usuario acepta)

**Fase 0:** marcar `ui: true` si hay frontend (dependencias de UI, carpetas de componentes, archivos
de tema: variables CSS, `tailwind.config.*`, `theme.*`, `variables.scss`, `src/theme/` de Ionic,
`ThemeData` de Flutter, `StyleSheet` de React Native).

**Fase 2:** una pregunta: *"¿Documento el diseño que usa hoy el código (sistema de diseño + HTML +
auditoría)?"*. Con un **no**: `design.status: declined` y no se hace nada más.

Con un **sí**:
1. **Fase 1, séptimo subagente "G. Interfaz y diseño"** (`references/explore-agents.md`, mismo formato
   Hallazgos / No determinado / Contradicciones): tokens declarados y dónde, fuentes cargadas,
   iconografía; **valores fijos** en estilos con conteo por archivo; componentes reutilizables y los
   estados que implementan; rutas y pantallas principales; tokens que nadie usa y valores repetidos
   que deberían ser token.
2. Si la app arranca (comandos de `AGENTS.md` verificados): capturas de las pantallas principales en
   `design.widths`, **solo con datos de prueba o semilla, nunca con datos reales**; si no arranca sin
   datos reales, no se capturan y se dice.
3. `design:design-system audit` sobre el inventario y `design:accessibility-review` sobre las capturas.
4. `system.md` con `source: extracted` y `status: draft`; lo no determinado se marca y se pregunta,
   nada se inventa. `system.html` muestra el sistema **tal como está** (paleta y escala reales,
   componentes y capturas), sin mejoras.
5. Deuda de diseño con IDs (`DS1`… en `system.md`: valores fijos, contraste insuficiente, toque
   pequeño, componentes sin estados) → conciliación con el roadmap como los riesgos de seguridad: se
   proponen objetivos, el usuario decide.
6. Al aprobar `system.md`, las pantallas nuevas o modificadas lo cumplen (misma regla que "Código
   previo" en la constitución): el código anterior no bloquea y mejora cuando una spec lo toca.

`/init` **no** ofrece rediseño ni genera opciones en brownfield. Si el usuario quiere uno, el resumen
final le indica que es una spec propia (`/specify "rediseño …"`).

**Rediseño como spec:** `/plan` de una spec de rediseño (o de una spec con pantallas que el sistema no
cubre) ejecuta el brief del §5 en modo spec: 3 opciones en HTML (2 si se mantiene la marca) en
`docs/specs/NNN-slug/design/`, elección, "Cambios a incorporar al sistema" y una primera tarea que
actualiza `system.md` y `system.html` (patrón del portafolio, spec 006). La migración del código se
hace en tareas por pantalla con su verificación manual contra el HTML.

## 7. `/init --upgrade`

Paso 5e: si el proyecto tiene interfaz y `design.status` falta o es `none`, pregunta si documentar el
diseño existente. Con un sí, ejecuta **solo** el §6 (pasos 1–6) sin volver a explorar el resto del
código; con un no, `design.status: declined` y no vuelve a preguntar. No ofrece rediseños ni
opciones. Si `design.status` ya es `draft` o `approved`, no hace nada.

## 8. Cómo lo usan las demás skills

| Skill | Cambio |
|---|---|
| `/specify` | Specs con UI: sección "Diseño" con qué debe sentirse y qué pantallas toca, enlazando `system.md`; sin tecnología. Microcopy con `design:ux-copy` si está habilitada. |
| `/plan` | Pantallas → componentes del sistema; lo que falte, a "Cambios a incorporar al sistema" con su primera tarea; nota `design:design-handoff`; paso de diseño del §6 en specs de rediseño o con pantallas nuevas sin cobertura. Validador: aviso si una spec con UI no cita `system.md` cuando `design.status: approved`. |
| `/tasks` | Tareas de UI con `verificación manual:` contra `system.html` (o el HTML de la spec) en `design.widths`. Tarea que crea el test o lint de "solo tokens" si aún no existe. |
| `/implement` | Capturas en `design.widths` comparadas con el HTML; espera confirmación. |
| `/review` | Subagente de accesibilidad con `design:accessibility-review` y `design:design-critique` contra `system.md` y el HTML. |

## 9. Decisiones tomadas (2026-10-02)

| Decisión | Fuente |
|---|---|
| El entregable visual es HTML en el repo (se abre cuantas veces se quiera); el canvas de la skill `design`, si existe, es un complemento enlazado | usuario |
| 3 opciones por defecto; 2 si el usuario ya trae marca | usuario |
| En brownfield solo se documenta el diseño existente, y solo si el usuario acepta | usuario |
| Los rediseños son siempre specs separadas; `/init` no los propone ni genera opciones en brownfield | usuario |
| `/init --upgrade` solo ejecuta la documentación del diseño existente | usuario |
| Se adoptan de `design-spec`: el brief, `creative-direction.md` y `anti-cliches.md` por proyecto, artboards en anchos fijos y especificación de movimiento con versión sin movimiento | /init (lectura de `.claude/skills/design-spec/`) |

## 10. Cambios por archivo

| Archivo | Cambio |
|---|---|
| `skills/init/references/design.md` (nuevo) | §4–§7 completos |
| `skills/init/SKILL.md` | Solo punteros (~80 palabras). **Está en 2 940 palabras**: antes hay que mover a `references/` la tabla "Secciones condicionales por tipo" |
| `skills/init/references/explore-agents.md` | Subagente G |
| `skills/init/references/interview.md` | Ronda 4b y la pregunta de brownfield |
| `skills/init/references/greenfield.md` | Tokens en la spec del proyecto base; auditoría de la plantilla contra `system.md` |
| `skills/init/references/upgrade.md` | Paso 5e |
| `skills/init/templates/design/` (nuevo) | `system.md`, `brief.md`, `creative-direction.md`, `anti-cliches.md` (base por tipo de proyecto) y `option.html` (HTML autocontenido, sin dependencias externas, modo claro/oscuro, anchos de comprobación) |
| `skills/init/templates/project.yaml` | Bloque `design` |
| `skills/init/templates/constitution.md` | Principio propuesto "solo tokens" (condicional a UI) |
| `skills/plan/references/design.md` (nuevo) y `skills/{specify,plan,tasks,implement,review}/SKILL.md` | §6 (rediseño como spec) y §8. `plan` está en 2 892 palabras: el detalle va en la referencia |
| `shared/contract.md` | Regla "Sistema de diseño" y las dos dependencias del §2 |
| `README.md` → "Dependencias" | Añadir la skill `design` (canvas) junto al plugin de Anthropic |
| `shared/vocabulary.md`, `scripts/aidd.py` | `Diseño`/`Design`, `DS<n>`; aviso de spec con UI sin enlace al sistema; validación de `system.md` (frontmatter, contraste en cada color de texto) y de `design.status` |
| `tests/` | Fixtures: frontend en inglés con `system.md` aprobado y una spec que no lo cita (aviso); `system.md` sin contraste (aviso); brownfield con `source: extracted`; `declined` |
| `CHANGELOG.md`, `docs/analisis-brechas.md` | Versión 1.11.0 |

## 11. Riesgos

- **Coste:** las opciones con pantallas reales son caras en tokens; se generan una vez por proyecto y
  el sistema se reutiliza en todas las specs (en el portafolio, 1 sistema sirvió para 15 specs).
- **Datos reales en capturas** (brownfield): solo datos de prueba.
- **Dependencias externas:** si la skill `design` o el plugin cambian, solo cambian los punteros; el
  formato de `system.md` y el HTML son del proyecto. La skill de diseño propia (hoja de ruta) partirá
  de este uso.
- **Tamaño de `/init` y `/plan`:** al límite; sin mover contenido a `references/` no cabe.

## 12. Orden de implementación

1. Mover contenido de `init/SKILL.md` y `plan/SKILL.md` a `references/` (sin cambio de comportamiento; tests en verde).
2. Plantillas de `templates/design/` y bloque `design` en `project.yaml`.
3. Greenfield (§4–§5) y proyecto base, probado con una app nueva (web en inglés, para no sobreajustar a Ionic).
4. Brownfield y `--upgrade` (§6–§7), probado con el portafolio: tiene `tokens.css` y sistema aprobado, así que el `system.md` extraído debe coincidir con su `designs/000-design-system`.
5. Rediseño como spec (§6) y skills del §8, validador y fixtures.
6. Prueba de punta a punta y entrada 8.15 en `analisis-brechas.md`.
