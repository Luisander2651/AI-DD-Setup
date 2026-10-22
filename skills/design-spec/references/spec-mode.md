# Diseño de una spec (`/design-spec NNN`)

Aplica a specs que crean o rehacen pantallas cuando `.ai/project.yaml → design.status` es `draft`
o `approved`. Produce `docs/specs/NNN-<slug>/design.md` (plantilla
`../../init/templates/design/spec-design.md`), que `/plan` exige aprobado. Criterios:
`criterios.md`; ciclo: `evaluacion.md`; movimiento: `movimiento.md`.

## 1. Cuándo aplica y cuándo se omite

- **Aplica** si la spec crea una pantalla, una sección o una vista, o cambia su composición; también
  a piezas fuera de pantalla con identidad visual (íconos, tarjeta para compartir, correos).
- **Se omite** si la spec solo cambia datos o comportamiento dentro de componentes ya diseñados,
  o el usuario lo pide: `design.md` con `exploration: none` y el motivo en "Resultado".
- Sin sistema aprobado o en borrador, primero `/design-spec system`.
- Un rediseño del sistema entero sigue además §5.

## 2. Criterios y ciclo

1. **Criterios.** Si la spec no tiene "Criterios de diseño", propónlos desde `criterios.md` §4 según
   el modo de cada pantalla, con un KPI o una puerta por cada criterio de aceptación con interfaz,
   y pide aprobación (es la única pregunta obligatoria). Escribe `design/criterios.json`.
2. **Ciclo** (`evaluacion.md`): candidato → `evaluate.mjs` → evaluador de la rúbrica → siguiente
   candidato con los fallos, hasta uno **aceptado** o hasta agotar `budget`.
3. **Acta:** `design.md` con cada candidato, su resultado y el aceptado (§3).
4. **Aprobación:** el usuario aprueba el acta (`status: approved`) o ajusta criterios y se repite el
   ciclo. No hay elección entre opciones.

## 3. Acta de diseño y cambios al sistema

Con un candidato aceptado (o el mejor, si el usuario lo acepta bajo el umbral), `design.md`
(`status: draft` hasta que el usuario lo aprueba) registra:
- frontmatter del ciclo (`exploration: loop`, `threshold`, `floor`, `budget`, `accepted`, `score`);
- **Candidatos:** una fila por candidato con su resultado y la ruta de su informe;
- **Resultado:** del aceptado, cada puerta y KPI con lo medido y la rúbrica con sus notas y evidencia;
- **Componentes:** los del sistema que usa (con estados) y los exclusivos de esta pantalla;
- **"Cambios a incorporar al sistema":** todo valor, token, componente o regla nueva, con su
  **modo** (`fijo`, `fluido` entre los anchos de `design.widths`, o un punto de corte) y motivo. La
  **primera tarea** de `/tasks` los aplica a `system.md` y `system.html` (con su entrada en
  "Decisiones") en el mismo commit que el código que los necesita, y añade sus colores a
  `criterios.json → tokens.colors`;
- **Movimiento** (fichas `M-n` de `movimiento.md` §5), **accesibilidad** y **Decisiones** (tipos del
  contrato; `refinado` para lo que cambia tras la revisión manual de `/implement`).

Después: en la spec, la sección "Diseño" enlaza `design.md` y "Decisiones" gana una fila (tipo
`diseño`); no se toca nada más de la spec salvo "Criterios de diseño". Si `design` está en
`skills.enabled`, añade la nota "Revisar con `design:design-handoff` antes de `/implement`". En la
Trazabilidad del plan, la tarea que construye cada pantalla lleva en `hecho cuando:` que
`evaluate.mjs` pase con `design/criterios.json` sobre la build servida en local.

**Refinado** (`/design-spec NNN --fix <qué>`): tras una revisión manual que pide otro valor o
comportamiento, aplica el cambio al candidato aceptado, vuelve a medirlo con `evaluate.mjs` (debe
seguir pasando puertas y KPIs) y registra la decisión `refinado`; `/plan NNN --fix` añade la tarea.
Si el cambio contradice un criterio, primero se cambia el criterio con el usuario.

## 4. Movimiento

Sigue `movimiento.md`: el filtro de cada animación, los tokens, lo que se permite y lo que no, la
ficha `M-<n>` y las reglas de rendimiento.

## 5. Spec de rediseño o con pantallas que el sistema no cubre

Un rediseño **siempre** es una spec propia; `/init` nunca lo hace. Antes del ciclo (§2):

0. **Documentos de partida.** Si faltan `docs/design/brief.md` o `anti-cliches.md` (lo normal con un
   sistema `extracted`), haz la entrevista de diseño (`../../init/references/interview.md` → Ronda
   4b) y créalos desde `../../init/templates/design/` con aprobación del usuario.
1. **Criterios del rediseño:** además de los de §2, una puerta por cada problema medible del diseño
   anterior que motiva el rediseño (p. ej. contraste, toque, acción principal fuera de la primera
   pantalla) y el punto de la rúbrica que el diseño anterior suspendía, con su nota mínima.
2. **Ciclo** con candidatos en `docs/specs/NNN-<slug>/design/candidatos/`; el primero puede partir
   del diseño anterior corregido.
3. "Cambios a incorporar al sistema" recoge todo lo que cambia de `system.md` (tokens, componentes,
   pantallas) y la primera tarea lo aplica, subiendo `version` de `system.md`.
4. **Migración por pantalla:** una tarea por pantalla (o grupo pequeño), cada una con
   `evaluate.mjs` sobre la pantalla migrada y el test de "solo tokens". Si conviven dos versiones de
   tokens, dilo en Rollout y en Riesgos.

## 6. Estados de pantalla

- **Carga y avisos para lectores de pantalla:** una sola región de estado (`<output>` o
  `role="status"`) siempre montada; el texto llega **después** de montarla (p. ej. en una tarea
  posterior) y se retira al terminar. Una región que aparece ya con su texto no se anuncia de forma
  fiable, y dos regiones a la vez compiten.
- **Errores:** `role="alert"` con qué pasó, qué pasa con los datos y la acción para reintentar.

## 7. Íconos e imagen para compartir

Aplica si la spec crea o cambia rutas públicas de un sitio indexable, o toca los íconos o la tarjeta
para compartir (`docs/design/system.md` → "Marca en el navegador y al compartir").
- **Qué imagen usa cada ruta:** en "Descubribilidad" (`../../plan/references/contracts-by-type.md` → "Sitio indexable"):
  general, **generada** desde su contenido con la tarjeta del sistema o propia. Por defecto, una
  ruta con contenido propio (artículo, producto, servicio) la genera; el resto usa la general.
- **Generación en la build:** la herramienta la decide el plan según el stack (una librería que
  convierte HTML o JSX en imagen, un navegador sin interfaz sobre una plantilla HTML, o un PNG
  estático en un sitio de una sola página). Una dependencia nueva lleva ADR y la verificación de
  `../../../shared/agent-security.md` §2; si el proyecto aún no genera imágenes, prueba de concepto en
  el Paso 1b. Las fuentes de la tarjeta son los archivos que ya usa el sitio, nunca un servicio
  externo en la build.
- **La plantilla de la imagen es el componente del sistema:** misma pieza firma, medidas, tokens y
  límites. Si la spec la cambia, va a "Cambios a incorporar al sistema".
- **Si falta o es genérica** (la spec introduce los íconos o la tarjeta y `system.md` no los define,
  o lo que define es la base de la plantilla, un logo sobre un degradado o iniciales sobre un
  cuadrado): la tarjeta y el ícono entran en el ciclo como un candidato más (`evaluacion.md`), con
  sus propios KPIs: tarjeta de 1200×630 que repite una pieza reconocible del sitio, título real de
  dos rutas dentro de la zona segura y sin cortes, contraste de la tarjeta, ícono legible a 16 px en
  pestaña clara y oscura, y ningún `<text>` en el SVG. El aceptado va a "Cambios a incorporar al
  sistema" con la composición **con medidas** (`system-mode.md` §2.4).
- **Tests:** cada ruta indexable de la spec tiene `og:image` que apunta a un archivo generado que
  existe, de 1200×630 y ≤ 300 kB; los datos que recibe el generador para esa ruta son su título y su
  sección o descripción (no se hace OCR de la imagen); los íconos existen con sus tamaños, se
  enlazan en el `<head>` y no son los de la plantilla del framework (compara con su huella).
- **SVG del ícono:** sin `<text>`, filtros ni imágenes (el texto convertido a trazos); test que lo
  comprueba junto con el `viewBox`.
- **Imagen estática** (sin generación en la build): la tarjeta anota qué datos obligan a
  regenerarla (nombre, rol, título de la portada…) y un test compara esos datos con los de la
  fuente, para que un cambio de contenido no deje la imagen desfasada sin aviso.
- **Verificación manual** en la tarea que construye el generador: dos rutas reales contra
  `system.html#compartir` (pieza firma, zona segura, recorte del título, contraste) y el ícono en una
  pestaña real clara y oscura. La vista previa real en las redes va a T095.

## 8. Del sistema extraído al elegido

Cuando la spec sustituye un sistema `source: extracted`, la primera tarea:
- reescribe `system.md` con `source: chosen` y **versión mayor**, la elección en "Decisiones" y la
  deuda `DS` que resuelve marcada "la resuelve NNN" (pasa a "resuelta por NNN" en T092);
- genera `system.html` desde el candidato aceptado con la cabecera "sistema de diseño aprobado";
- actualiza `.ai/project.yaml → design` (`source: chosen`; `status: approved` cuando el usuario
  aprueba `system.md`), que el validador compara con el frontmatter;
- las capturas de `docs/design/capturas/` se rehacen al cerrar la spec (T092), en claro y oscuro.

## 9. Conectar los tokens con la librería de componentes

Con una librería (Ionic, Material, Vuetify, Chakra…), definir `--color-*` no basta: sus
componentes pintan con sus propias variables. "Cambios por módulo" incluye la conexión en el mismo
archivo de tokens, para cada modo:
- fondo, texto, superficies de barra, filas y diálogos (Ionic: `--ion-background-color`,
  `--ion-text-color`, `--ion-toolbar-background`, `--ion-item-background`,
  `--ion-overlay-background-color`), con sus variantes `-rgb`;
- colores semánticos con su texto encima y sus tonos (Ionic: `--ion-color-<n>`, `-contrast`,
  `-shade`, `-tint`);
- escalas de grises derivadas (Ionic: `--ion-background-color-step-N`, `--ion-text-color-step-N`),
  calculadas entre el fondo y el texto de cada modo;
- la familia tipográfica (`--ion-font-family`) y lo que la librería fuerza (mayúsculas de Material,
  altos de botón de barra).

## 10. Tests del sistema

Recetas para la Estrategia de pruebas (un principio "solo tokens" se verifica con test, no a mano):
- **Tokens = sistema:** el test lee la tabla Color de `system.md` y exige los **mismos valores**
  en el archivo de tokens, en cada modo (no basta con que existan).
- **Contraste:** pares texto/fondo ≥ 4.5:1 y borde/foco ≥ 3:1 calculados desde el archivo de
  tokens, en cada modo.
- **Solo tokens:** ningún color (`#…`, `rgb(`, `hsl(`), tamaño con unidad (salvo `0` y `1px`) ni
  `font-family` literal fuera del archivo de tokens, y ningún estilo en línea en componentes. Cada
  regla con un **control positivo** (el patrón detecta un literal de ejemplo). Cuidado con los
  lookahead tras `\s*`: `font-family\s*:\s*(?!var\()` acepta `font-family: var(…)` como literal
  porque `\s*` retrocede; escribe `font-family\s*:(?!\s*var\()`.
- **Modo oscuro en pantalla:** con `emulateMedia` (o equivalente), el color **calculado** del fondo
  de la pantalla, la barra, una fila y el diálogo (dentro de su shadow DOM si lo hay), no solo el
  del `body`: las superficies internas de la librería son las que se quedan claras.
- **Margen y toque:** cajas medidas en el navegador al ancho menor de `design.widths`.
- **`theme-color` = token:** el valor de `<meta name="theme-color">` en el HTML generado es el de
  `--color-bg` en el archivo de tokens (en cada modo si hay modo oscuro).
- **Tokens fluidos:** cada token `fluido` de `system.md` interpola entre sus dos valores en los
  anchos de `design.widths` (p. ej. con `clamp()`), comprobado en esos dos anchos.
- **Fuente dentro de la app:** el build contiene sus archivos y ningún CSS/JS pide fuentes o CDN
  externos; en pantalla, la fuente consta como cargada (`document.fonts` con `status: loaded`).
