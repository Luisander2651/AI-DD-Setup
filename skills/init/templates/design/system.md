---
status: draft            # draft | approved (solo el usuario aprueba)
source: {{chosen|extracted}}   # chosen: elegido entre opciones · extracted: documentado del código
version: 1.0.0
extracted_with: {{skills_version}}   # solo source: extracted — versión del plugin que lo extrajo (--upgrade ofrece re-extraer si es anterior a 1.11.2)
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
y bordes de control). Modo oscuro: {{"no aplica", o la misma tabla con columnas "Claro" y "Oscuro" en lugar de "Valor", los
valores oscuros de **todos** los colores y el contraste de ambos como `13.0:1 · 15.2:1`}}.

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

## Marca en el navegador y al compartir

Cómo se reconoce el producto fuera de sus pantallas: en la pestaña del navegador, en la pantalla de
inicio del móvil y en la vista previa de un enlace compartido. Vista: `system.html#compartir`.
Comprobación técnica: `shared/seo-checklist.md` temas 7 y 12 del plugin.

### Íconos

| Archivo | Tamaño | Origen | Estado |
|---|---|---|---|
| `favicon.svg` | vectorial (retícula de 64) | {{marca que ya aparece en la interfaz: letras de la barra, símbolo del logo · monograma provisional}} | {{✅ · pendiente · DS<n>}} |
| `favicon-32.png` | 32×32 | rasterizado del SVG | |
| `apple-touch-icon.png` | 180×180 | el mismo dibujo con fondo `--color-bg` y margen interior | |

- **Dibujo:** {{retícula, fondo, borde, letras o símbolo con familia, peso y tamaño, acento de la
  marca y su posición; p. ej. "LM" en mono 600 a 26/64 con el punto de luz en (14, 14)}}.
- **Texto convertido a trazos** en el SVG (sin `<text>`, filtros ni imágenes): con `<text>` cada
  sistema lo dibuja con otra fuente.
- **Legible a 16 y 32 px** en pestaña clara **y** oscura: trazo grueso, sin detalles finos; qué se
  simplifica respecto al logo: {{…}}.
- `theme-color`: `--color-bg` ({{#…}}{{; oscuro: #… si hay modo oscuro}}).
- {{Si es monograma: "provisional hasta que el proyecto tenga logo (decisión del usuario pendiente)"}}.

<!-- if seo.indexable=true -->
### Tarjeta para compartir

Imagen Open Graph de 1200×630 que **repite la pieza firma del sitio**, para que el enlace compartido y
la web se reconozcan como la misma pieza. Solo tokens de este sistema; peso ≤ 300 kB.

- **Pieza firma de origen:** {{el elemento más reconocible del sitio (tarjeta del hero, momento
  firma, cabecera de la ficha…) y qué conserva: superficie, borde, luz, retícula, tipografía}}.
- **Composición** (medidas sobre 1200×630):

| Elemento | Posición y tamaño | Tipografía | Tokens |
|---|---|---|---|
| Lienzo | 1200×630, margen seguro {{64}} px | — | {{--color-bg, superficies del sistema}} |
| Marca | {{arriba a la izquierda, a 64 px}} | {{familia, peso, tracking}} | {{…}} |
| Pieza firma | {{ancho, padding, radio, posición}} | — | {{superficie, borde, sombra o luz}} |
| {{Dato 1, p. ej. título}} | {{…}} | {{tamaño, peso, tracking, líneas máx.}} | {{…}} |
| {{Dato 2…}} | | | |

- **Datos y de dónde salen** (los que dan identidad, no solo título y descripción): {{título ←
  `<title>` sin el nombre del sitio; sección ← ruta; autor, fecha, precio, categoría ← contenido
  de la página}}. Nada inventado: sin un dato, esa línea no aparece; sin el título, se usa la
  general.
- **Zona segura:** marca y título dentro del cuadrado central de 630×630 y a ≥ 60 px de los bordes.
- **Contraste:** cada texto sobre su fondo, medido ({{n.n:1}}).
- **Variantes:** general (portada y rutas sin imagen propia) · {{por tipo de página}}.
- **`og:image:alt`:** {{el título de la página}}.
- **Fuentes:** las del sitio, desde sus archivos; nunca la fuente de reemplazo.
- **Generación:** {{estática · generada en la build por ruta (herramienta y ADR en el plan que la
  introduce)}}.
<!-- endif -->

## Pantallas principales

| Pantalla | Móvil | Escritorio | Componentes |
|---|---|---|---|
| {{nombre}} | `system.html#{{id}}-m` | `system.html#{{id}}-d` | {{…}} |

<!-- if source: extracted -->
## Inventario de vistas

**Todas** las vistas de la app (rutas, plantillas, modales con URL propia), no solo las principales,
con capturas de la app real hechas con datos de prueba. Nada se dibuja a mano.

| Vista | Ruta / plantilla | Rol | Capturas | Estado |
|---|---|---|---|---|
| {{Citas}} | {{/citas · resources/views/citas/index.blade.php}} | {{personal}} | {{capturas/citas-390.png · capturas/citas-1440.png}} | {{capturada}} |
| {{Facturación}} | {{/facturacion}} | {{admin}} | — | {{sin captura (motivo)}} |

Estados: `capturada` · `sin captura (motivo)` · `no accesible (motivo)`. El validador comprueba
que las capturas citadas existan.
<!-- endif -->

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

Estados: `pendiente` · `la resuelve NNN` · `resuelta por NNN` · `no se confirma (re-extracción
AAAA-MM-DD: evidencia)`. Un ID nunca se reutiliza: una re-extracción conserva los vigentes y numera
lo nuevo a partir del último.
<!-- endif -->

## Decisiones

| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |
|---|---|---|---|---|
| {{date}} | {{diseño · implícita · brecha · contradicción · supuesto}} | {{…}} | {{…}} | {{usuario · ruta · /skill}} |
