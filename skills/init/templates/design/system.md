---
status: draft            # draft | approved (solo el usuario aprueba)
source: {{chosen|extracted}}   # chosen: elegido entre opciones · extracted: documentado del código
version: 1.0.0
html: docs/design/system.html
canvas: {{enlace del canvas de la skill design | null}}
widths: [{{390, 1440}}]
created: {{date}}
updated: {{date}}
---

# Sistema de diseño de {{project_name}}

Fuente de verdad visual del proyecto. Toda pantalla nueva o modificada usa estos tokens y
componentes; un valor que no esté aquí se añade primero aquí (sección "Cambios a incorporar" del
plan que lo necesite). Vista: [system.html](system.html).

## Dirección

{{Opción elegida (A/B/C) y qué se combinó de otras, o "sistema extraído del código el <fecha>".
Qué debe sentir quien lo usa, en 2–3 frases. Dirección creativa: creative-direction.md.}}

## Color

| Token | Valor | Uso | Contraste sobre su fondo |
|---|---|---|---|
| `--color-bg` | `{{#…}}` | Fondo base | — |
| `--color-surface` | `{{#…}}` | Tarjetas, paneles, campos | — |
| `--color-text` | `{{#…}}` | Texto principal | {{n.n:1 sobre --color-bg}} |
| `--color-text-muted` | `{{#…}}` | Texto secundario | {{n.n:1 sobre --color-bg}} |
| `--color-primary` | `{{#…}}` | Acción principal | — |
| `--color-on-primary` | `{{#…}}` | Texto sobre la acción principal | {{n.n:1 sobre --color-primary}} |
| `--color-border` | `{{#…}}` | Bordes y separadores | {{n.n:1 sobre --color-bg (≥ 3:1 si delimita un control)}} |
| `--color-focus` | `{{#…}}` | Anillo de foco | {{n.n:1 sobre --color-bg (≥ 3:1)}} |
| `--color-danger` | `{{#…}}` | Errores | {{n.n:1 sobre --color-bg}} |
| `--color-success` | `{{#…}}` | Confirmaciones | {{n.n:1 sobre --color-bg}} |
| `--color-warning` | `{{#…}}` | Avisos | {{n.n:1 sobre su fondo}} |

Todo color de texto declara su contraste calculado (WCAG: ≥ 4.5:1 texto normal, ≥ 3:1 texto grande
y bordes de control). Modo oscuro: {{"no aplica", o la misma tabla con los valores oscuros de **todos** los colores y su contraste}}.

## Tipografía

| Token | Familia | Pesos | Uso |
|---|---|---|---|
| `--font-sans` | {{familia, alternativas del sistema}} | {{400, 600}} | Contenido |
| `--font-mono` | {{familia o "no aplica"}} | {{400}} | Datos, código, etiquetas |

| Nivel | Móvil | Escritorio | Interlineado |
|---|---|---|---|
| `--text-h1` | {{28px}} | {{40px}} | {{1.2}} |
| `--text-h2` | {{22px}} | {{28px}} | {{1.3}} |
| `--text-body` | {{16px}} | {{16px}} | {{1.5}} |
| `--text-small` | {{14px}} | {{14px}} | {{1.4}} |

Fuentes: {{autoalojadas en … / del sistema}}; nunca cargadas desde un servicio externo sin
aprobarlo en `docs/security.md`.

## Espaciado, radios, bordes y sombras

- Escala de espaciado: `--space-1` … `--space-8` = {{4, 8, 12, 16, 24, 32, 48, 64}} px.
- Margen lateral de pantalla: `--space-gutter` = {{16px móvil · 32px escritorio}}.
- Radios: `--radius-sm` {{4px}} · `--radius-md` {{8px}} · `--radius-lg` {{16px}}.
- Bordes: `--border-width` {{1px}}. Sombras: `--shadow-1` {{…}}.
- Objetivo de toque mínimo: `--touch-min` {{44px}} (`mobile`: 44 pt iOS / 48 dp Android).

## Componentes

Para cada uno: anatomía, variantes, estados (reposo, hover, foco, activo, deshabilitado, error,
carga), tamaño mínimo y accesibilidad (rol, nombre, teclado). Vista en `system.html` → Componentes.

### Botón
{{primario, secundario, peligro · estados · altura ≥ --touch-min · foco visible con --color-focus}}

### Campo de formulario
{{etiqueta visible, ayuda, error junto al campo con --color-danger y texto (no solo color),
margen lateral --space-gutter, altura ≥ --touch-min}}

### Lista o tarjeta
{{…}}

### Aviso, diálogo y mensajes
{{informativo, éxito, error; diálogo modal con foco atrapado y retorno del foco}}

### Estados de pantalla
{{vacío (con acción), cargando, error (con reintentar)}}

## Movimiento

| Token | Valor | Uso |
|---|---|---|
| `--duration-fast` | {{150ms}} | Microinteracciones |
| `--duration-base` | {{250ms}} | Entradas y transiciones |
| `--ease-out` | `{{cubic-bezier(0.2, 0, 0, 1)}}` | Entradas |

Cada animación declara su versión con `prefers-reduced-motion: reduce` (estática equivalente) y
anima solo `transform` y `opacity` salvo justificación.

## Pantallas principales

| Pantalla | Móvil | Escritorio | Componentes |
|---|---|---|---|
| {{nombre}} | `system.html#{{id}}-m` | `system.html#{{id}}-d` | {{…}} |

## Reglas de uso

- {{Una acción principal por pantalla; colores semánticos solo con su significado; …}}
- Ningún valor literal de color, tamaño o espaciado fuera de los tokens (principio "solo tokens"
  de la constitución, verificado por test o lint).

<!-- if source: extracted -->

## Deuda de diseño

Lo que el código hace hoy y no cumple este sistema o las pautas de accesibilidad. No bloquea el
código previo; se corrige cuando una spec toca la pantalla o como objetivo del roadmap.

| ID | Problema | Dónde (evidencia) | Corrección propuesta | Estado |
|---|---|---|---|---|
| DS1 | {{valores fijos de color en 23 archivos}} | {{rutas}} | {{sustituir por tokens}} | pendiente |
<!-- endif -->

## Decisiones

| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |
|---|---|---|---|---|
| {{date}} | {{diseño · implícita · brecha · contradicción · supuesto}} | {{…}} | {{…}} | {{usuario · ruta · /skill}} |
