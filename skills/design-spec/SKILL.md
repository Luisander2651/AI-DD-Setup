---
name: "design-spec"
description: "Diseña la interfaz: el sistema de diseño del proyecto (opciones en HTML o el diseño existente documentado) y, en cada spec con pantallas, 2–3 composiciones sobre el sistema antes de planear. Úsala con /design-spec system, /design-spec NNN o cuando el usuario pida diseñar, rediseñar o documentar pantallas."
---

# /design-spec — Diseño de interfaz

Paso del flujo en proyectos con interfaz:

```
/init → /specify → [/design-spec NNN] → /plan → /tasks → /analyze → /implement → /review → /release
            └─ /init llama a /design-spec system para el sistema de diseño
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Decide **cómo se ve y se mueve** el producto. El sistema de diseño fija el lenguaje de todo el
producto; el diseño de cada spec elige entre composiciones distintas sobre ese lenguaje, para que
ninguna pantalla sea la plantilla de otra.

## Uso

```
/design-spec system                       # greenfield: opciones y sistema · brownfield: documentar el existente
/design-spec system --redo-design         # re-extraer un sistema documentado del código
/design-spec system --redo-options [--only <eje> --base <a|b|c>]   # rehacer opciones o afinar un eje
/design-spec <NNN|slug>                   # composiciones de una spec con pantallas
/design-spec <NNN> --fix <qué>            # refinar tras la revisión manual (decisión `refinado`)
```

## Reglas

- **Solo proyectos con interfaz** (`frontend`, `fullstack`, `mobile`, paquetes de esos tipos). En
  otro tipo, dilo y detente.
- **HTML en el repo.** Toda opción o composición es un HTML desde `../init/templates/design/` que se
  abre sin red. Si la sesión ofrece la skill externa `design` (canvas), úsala además y enlaza el
  canvas; no es esta skill (contrato → "Dependencias externas").
- **Contenido real.** Textos y datos del proyecto o de la spec; nunca lorem ipsum ni cifras
  inventadas. Los adornos (índices, rutas, código decorativo) se generan desde datos reales.
- **No cambia código de la app** ni la spec, salvo la sección "Diseño" y una fila de "Decisiones".
  Escribe solo en `docs/design/` y `docs/specs/NNN-<slug>/design*`.
- **Aprobación humana.** `system.md` y cada `design.md` nacen en `draft`; solo el usuario los aprueba.
  Las opciones descartadas no se borran.
- **Antes de enseñar** cualquier opción: contraste sin ningún "no cumple", repaso contra
  `docs/design/anti-cliches.md` y `references/system-mode.md` §6, y la revisión de "Al compartir".
- Escribe en el idioma del proyecto.

---

## Modo `system`

Sigue `references/system-mode.md`:
- **Greenfield** (§2): investigación del nicho (`references/nicho.md`), entrevista de diseño
  (`../init/references/interview.md` → Ronda 4b), documentos de partida, 2–3 opciones distintas de
  verdad, elección y `docs/design/system.md` + `system.html`.
- **Brownfield** (§3): solo si el usuario aceptó documentar el diseño existente; fidelidad a lo que
  ve el usuario (capturas con datos de prueba, medidas), deuda `DS`, sin rediseñar.
- `--redo-design` → §3b · `--redo-options` → §2.7 · `--only <eje> --base <opción>` → §2.8.

Al terminar, actualiza `.ai/project.yaml → design` y ejecuta `python .ai/bin/aidd.py validate`.
Cuando lo llama `/init`, devuelve el control a la fase en que estaba.

## Modo `NNN` — diseño de una spec

### Paso 0 — Precondiciones
1. La spec existe y está en `approved` (o en `draft` si el usuario quiere diseñar antes de cerrarla;
   avísale de que un cambio de criterios puede rehacer el diseño).
2. `design.status` es `draft` o `approved`. Si no, propone `/design-spec system` primero.
3. Si ya existe `design.md` aprobado, pregunta si regenerar las composiciones o solo refinar.

### Paso 1 — ¿Hace falta explorar?
Sigue `references/spec-mode.md` §1. Si no hay pantalla nueva ni recomposición (o el usuario lo
pide), escribe `design.md` con `exploration: none` y el motivo, y salta al Paso 4.

### Paso 2 — Composiciones
`references/spec-mode.md` §2: contexto y pantallas vecinas, preguntas que falten, **2–3
composiciones** con nombre y metáfora del contenido real, vecino más parecido y diferencia,
jerarquía declarada, riesgo marcado, anchos de `design.widths` más uno intermedio si hay filas, y
estados. Si es un rediseño o hay pantallas que el sistema no cubre, añade §5. Íconos o tarjeta para
compartir: §7.

### Paso 3 — Elección
El usuario elige, combina, afina un eje o pide rehacer (`references/spec-mode.md` §2). Registra la
elección.

### Paso 4 — Documento
`docs/specs/NNN-<slug>/design.md` desde `../init/templates/design/spec-design.md`
(`references/spec-mode.md` §3 y §4): dirección y motivo, composición con proporciones y puntos de
corte, componentes del sistema y exclusivos, "Cambios a incorporar al sistema" con su modo,
movimiento en fichas `M-n` con versiones reducida, sin JavaScript y táctil, accesibilidad,
anti-clichés con su alternativa y decisiones. Enlázalo desde la sección "Diseño" de la spec con su
fila en "Decisiones" (tipo `diseño`).

### Paso 5 — Autoverificación y aprobación
- [ ] Cada composición tiene metáfora, vecino y diferencia, y riesgo; ninguna repite el esqueleto
      de otra pantalla del producto.
- [ ] Ningún valor visual fuera de los tokens o de "Cambios a incorporar al sistema".
- [ ] Toda animación con versión reducida, sin JavaScript y táctil, y su coste; reglas de
      rendimiento y de "Reglas de uso" respetadas (`references/spec-mode.md` §4).
- [ ] Contraste calculado de cada par; adornos ocultos a lectores de pantalla.
- [ ] `python .ai/bin/aidd.py validate docs/specs/NNN-<slug>` sin errores.

Presenta el resumen (composición elegida, cambios al sistema, animaciones, riesgos) y pide
aprobación: `design.md` pasa a `approved`. Siguiente paso: `/plan NNN`.

## Modo `--fix`

Tras una revisión manual de `/implement` que pide otro valor o comportamiento: actualiza
`design.md` (y "Cambios a incorporar al sistema" si toca el sistema) con la decisión `refinado` y su
motivo, sin regenerar composiciones. Después, `/plan NNN --fix` añade la tarea.
