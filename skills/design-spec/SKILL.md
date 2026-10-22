---
name: "design-spec"
description: "Diseña la interfaz por criterios: define puertas, KPIs y una rúbrica, genera un candidato tras otro, los mide en el navegador y acepta solo el que supera el umbral. Hace el sistema de diseño (o documenta el existente) y el diseño de cada spec con pantallas antes de planear. Úsala con /design-spec system, /design-spec NNN o cuando el usuario pida diseñar, rediseñar o documentar pantallas."
---

# /design-spec — Diseño por criterios

Paso del flujo en proyectos con interfaz:

```
/init → /specify → [/design-spec NNN] → /plan → /tasks → /analyze → /implement → /review → /release
            └─ /init llama a /design-spec system para el sistema de diseño
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

El diseño **no se elige por gusto**: se acepta cuando supera un nivel medible. Primero se fijan los
criterios (puertas, KPIs y rúbrica: `references/criterios.md`); después se genera un candidato, se
mide con `scripts/evaluate.mjs`, lo puntúa un evaluador que no lo diseñó y, si no llega, el
siguiente candidato corrige sus fallos, hasta aceptar uno o agotar el presupuesto
(`references/evaluacion.md`). El usuario aprueba el resultado con su acta; no elige entre bocetos.

## Uso

```
/design-spec system                       # greenfield: criterios y ciclo del sistema · brownfield: documentar el existente
/design-spec system --redo-design         # re-extraer un sistema documentado del código
/design-spec system --redo-options [--only <eje> --base <cN>]   # repetir el ciclo con criterios nuevos, o ajustar un eje
/design-spec <NNN|slug>                   # criterios y ciclo de una spec con pantallas
/design-spec <NNN> --fix <qué>            # refinar el aceptado tras la revisión manual (decisión `refinado`)
```

## Reglas

- **Solo proyectos con interfaz** (`frontend`, `fullstack`, `mobile`, paquetes de esos tipos). En
  otro tipo, dilo y detente.
- **Criterios antes que diseño.** Sin criterios aprobados no se genera ningún candidato. Cada
  criterio de aceptación con interfaz tiene al menos un KPI o una puerta que lo comprueba.
- **Aceptar solo lo que supera el umbral:** todas las puertas, todos los KPIs y la rúbrica ≥
  `threshold` sin ningún punto por debajo de `floor` (`.ai/project.yaml → design`). Bajo el umbral,
  solo el usuario puede aceptar, con una decisión registrada.
- **Presupuesto:** como mucho `budget` candidatos por ciclo; al agotarlo, para y presenta el mejor
  con lo que le falta (`references/evaluacion.md` §5).
- **El evaluador no diseña:** la rúbrica la puntúa un subagente (perfil `critical`) que solo ve las
  capturas, los criterios y la rúbrica.
- **Candidatos en HTML en el repo**, autocontenidos (sin red), desde `../init/templates/design/`:
  páginas reales a ancho de ventana (`pagina.html`); en modo sistema, además, el visor `option.html`.
  Los descartados no se borran.
- **Contenido y recursos reales.** Textos y datos del proyecto o de la spec; los recursos de marca
  que existen (logo, fotos, íconos) se abren y se usan tal como son. Nunca lorem ipsum,
  testimonios, cifras ni logos inventados. Toda imagen declara su origen; las fotos de muestra solo
  si el brief o el usuario lo permiten, sin representar al negocio, listadas para sustituirlas
  (`references/criterios.md` §7).
- **Lo elaborado se pide como criterio:** fondos propios, escenas de scroll y fotos entran como
  KPIs (`scenes`, `moving_elements`, `custom_background`) y como peso del punto `riqueza` de la
  rúbrica (`references/criterios.md` §6).
- **No cambia código de la app** ni la spec, salvo "Criterios de diseño", la sección "Diseño" y una
  fila de "Decisiones". Escribe solo en `docs/design/` y `docs/specs/NNN-<slug>/design*`.
- **Aprobación humana.** `system.md` y cada `design.md` nacen en `draft`; solo el usuario los aprueba.
- Si la sesión ofrece la skill externa `design` (canvas), puede usarse para el primer candidato; no
  es esta skill (contrato → "Dependencias externas"). El candidato que se mide es siempre el HTML.
- Escribe en el idioma del proyecto.

---

## Modo `system`

Sigue `references/system-mode.md`:
- **Greenfield** (§2): investigación del nicho (`references/nicho.md`), entrevista de diseño
  (`../init/references/interview.md` → Ronda 4b), documentos de partida, **criterios del sistema**
  (§2.3), **ciclo** de candidatos (§2.4) y el aceptado como `docs/design/system.md` +
  `system.html` (§2.5).
- **Brownfield** (§3): solo si el usuario aceptó documentar el diseño existente; fidelidad a lo que
  ve el usuario (capturas con datos de prueba, medidas), deuda `DS`, sin rediseñar.
- `--redo-design` → §3b · `--redo-options` → §2.7 · `--only <eje> --base <cN>` → §2.8.

Al terminar, actualiza `.ai/project.yaml → design` y ejecuta `python .ai/bin/aidd.py validate`.
Cuando lo llama `/init`, devuelve el control a la fase en que estaba.

## Modo `NNN` — diseño de una spec

### Paso 0 — Precondiciones
1. La spec existe y está en `approved` (o en `draft` si el usuario quiere diseñar antes de cerrarla;
   avísale de que un cambio de criterios puede rehacer el diseño).
2. `design.status` es `draft` o `approved`. Si no, propone `/design-spec system` primero.
3. Si ya existe `design.md` aprobado, pregunta si repetir el ciclo (con los mismos criterios o con
   criterios nuevos) o solo refinar (`--fix`). Repetirlo archiva el acta y los candidatos en
   `design/history/ronda-<N>/`.

### Paso 1 — ¿Hace falta diseñar?
`references/spec-mode.md` §1. Si no hay pantalla nueva ni recomposición (o el usuario lo pide),
escribe `design.md` con `exploration: none` y el motivo, y salta al Paso 5.

### Paso 2 — Criterios
`references/criterios.md`: si la spec no tiene "Criterios de diseño", propónlos según el modo de
cada pantalla (§4) con un KPI o una puerta por cada criterio de aceptación con interfaz, la rúbrica
con sus pesos (§5) y el umbral, el mínimo y el presupuesto de `project.yaml`. Pide aprobación: es la
pregunta que decide todo lo demás. Escribe la tabla en la spec y `design/criterios.json`.

### Paso 3 — Ciclo
`references/evaluacion.md`: lee el sistema, las pantallas vecinas y el contenido, abre los recursos
de marca, y repite **candidato → `evaluate.mjs` → evaluador → fallos al siguiente** hasta un
aceptado o hasta `budget`. Movimiento solo el que pidan los criterios, con `references/movimiento.md`.
Íconos o tarjeta para compartir: `references/spec-mode.md` §7. Rediseño o pantallas que el sistema no
cubre: §5.

### Paso 4 — Acta
`docs/specs/NNN-<slug>/design.md` desde `../init/templates/design/spec-design.md`
(`references/spec-mode.md` §3): frontmatter del ciclo, una fila por candidato, el resultado del
aceptado (puertas, KPIs, rúbrica con evidencia), componentes, "Cambios a incorporar al sistema" con
su modo, fichas `M-n` si hay movimiento, accesibilidad y decisiones. Enlázalo desde la sección
"Diseño" de la spec con su fila en "Decisiones" (tipo `diseño`).

### Paso 5 — Autoverificación y aprobación
- [ ] Cada criterio de aceptación con interfaz tiene su KPI o puerta en `criterios.json`.
- [ ] El aceptado pasa todas las puertas y KPIs (`report.json` del último `evaluate.mjs`) y su
      puntuación supera el umbral sin ningún punto bajo el mínimo; o la decisión del usuario que lo
      acepta por debajo está en "Decisiones".
- [ ] Ningún valor visual fuera de los tokens o de "Cambios a incorporar al sistema".
- [ ] Cada candidato tiene su fila en el acta; ninguno se borró.
- [ ] `python .ai/bin/aidd.py validate docs/specs/NNN-<slug>` sin errores.

Presenta el acta y abre el candidato aceptado (o pasa sus capturas). Pide aprobación: `design.md`
pasa a `approved`. Siguiente paso: `/plan NNN`. Si el usuario no lo aprueba, pregúntale qué criterio
falta o sobra, cámbialo y repite el ciclo.

## Modo `--fix`

Tras una revisión manual de `/implement` que pide otro valor o comportamiento: aplica el cambio al
candidato aceptado, vuelve a medirlo con `evaluate.mjs` (debe seguir pasando) y actualiza
`design.md` (y "Cambios a incorporar al sistema" si toca el sistema) con la decisión `refinado` y su
motivo. Si el cambio contradice un criterio, primero se cambia el criterio con el usuario. Después,
`/plan NNN --fix` añade la tarea.
