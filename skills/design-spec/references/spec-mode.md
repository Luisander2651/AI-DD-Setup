# Diseño de una spec (`/design-spec NNN`)

Aplica a specs que crean o rehacen pantallas cuando `.ai/project.yaml → design.status` es `draft`
o `approved`. Formato del sistema y de los HTML: `system-mode.md` (§2.4 y §5) y
`../../init/templates/design/`. Produce `docs/specs/NNN-<slug>/design.md` (plantilla
`../../init/templates/design/spec-design.md`), que `/plan` exige aprobado.

## 1. Cuándo aplica y cuándo se omite

- **Aplica** si la spec crea una pantalla, una sección o una vista, o cambia su composición; también
  a piezas fuera de pantalla con identidad visual (íconos, tarjeta para compartir, correos).
- **Se omite** si la spec solo cambia datos o comportamiento dentro de componentes ya diseñados,
  o el usuario lo pide: `design.md` con `exploration: none` y el motivo en "Dirección elegida".
- Sin sistema aprobado o en borrador, primero `/design-spec system`.
- Un rediseño del sistema entero sigue además §5.

## 2. Composiciones

Antes de diseñar, lee el sistema (`system.md`, `system.html`), `creative-direction.md`,
`anti-cliches.md`, `nicho.md` si existe, y los `design.md` de las specs ya diseñadas: qué
composiciones y componentes firma usa cada pantalla vecina. Pregunta (máximo 4 por ronda) solo lo
que falte: contenido real, estados, qué merece movimiento.

Genera **2–3 composiciones** sobre el sistema aprobado en
`docs/specs/NNN-<slug>/design/opcion-<a|b|c>.html` desde `option.html` (solo las secciones que
apliquen: pantallas, movimiento, al compartir), cada una con:
1. **Nombre corto y metáfora** sacada del contenido real de la spec, no de una moda: qué cuenta la
   composición y con qué dato (p. ej. "la ficha del paciente como expediente con pestañas",
   "el catálogo como estante con lomos", "la agenda como tablero de turnos"). Una composición que no
   cambia la estructura es solo un nombre: rehazla.
2. **Vecino más parecido** del mismo producto (otra pantalla o sección ya diseñada) y en qué se
   diferencia: estructura, ritmo, densidad o componente firma. Dos pantallas con el mismo esqueleto
   son un cliché aunque cada una por separado esté bien.
3. **Jerarquía declarada:** con varios elementos del mismo tipo, la proporción o la variación de
   tamaño (p. ej. destacado 7:5 delante del resto, mosaico 5:7, alturas igualadas con el pie
   alineado). Una rejilla de iguales necesita motivo ("solo hay dos y son simétricos").
4. **Riesgo asumido** y cómo se compensa. Una composición puede llevar a propósito un elemento de
   riesgo (p. ej. un medidor que roza el cliché de "barra de nivel"), **marcado como tal**: el
   usuario decide si lo quita.
5. **Contenido real** de la spec y adornos generados desde datos (índices desde el orden, rutas
   desde el ancla, código o fichas desde el registro real), nunca texto de relleno; los adornos van
   ocultos a lectores de pantalla y la página funciona sin ellos.
6. **Anchos:** los de `design.widths` **y uno intermedio** (≈ 900 px) cuando haya composiciones en
   fila: lo que a 1440 px es una fila de tres puede quedar en columnas de 200 px. Si se rompe,
   declara un punto de corte propio de la composición (sin crear un modo nuevo de tokens).
7. **Estados** que la spec pide (vacío, carga, error, foco, hover y su equivalente táctil).

Las composiciones son **distintas de verdad** (`system-mode.md` §2.4) y se revisan contra
`anti-cliches.md` y `system-mode.md` §6 antes de enseñarlas. Presenta una tabla (composición,
metáfora, vecino y diferencia, riesgo, ruta del HTML). El usuario elige, combina, afina un eje
(`system-mode.md` §2.8) o pide rehacerlas (§2.7, archivando en
`docs/specs/NNN-<slug>/design/history/ronda-<N>/`). Las descartadas se conservan.

## 3. Documento de diseño y cambios al sistema

Con la elección, `design.md` (`status: draft` hasta que el usuario lo aprueba):
- **Dirección elegida**, motivo y riesgo; lo combinado de otras composiciones.
- **Composición y jerarquía:** orden de lectura, proporciones, puntos de corte, todo con tokens.
- **Componentes:** los del sistema que usa (con estados) y los **exclusivos** de esta pantalla
  (un componente firma no se reutiliza en otra sección; si debe compartirse, pasa al sistema).
- **"Cambios a incorporar al sistema":** todo valor, token, componente o regla nueva, con su
  **modo** (`fijo`, `fluido` entre los anchos de `design.widths`, o un punto de corte) y motivo. La
  **primera tarea** de `/tasks` los aplica a `system.md` y `system.html` (con su entrada en
  "Decisiones") en el mismo commit que el código que los necesita, para que el test de tokens no
  quede en rojo.
- **Movimiento** (§4), **accesibilidad** (contraste calculado de cada par, encabezados, decorativos
  ocultos, teclado, contenido sin animación) y **anti-clichés** de esta pantalla: cada uno con la
  alternativa que se usó.
- **Decisiones** (tipos del contrato; `refinado` para lo que cambia tras la revisión manual de
  `/implement`, con el motivo).

Después: en la spec, la sección "Diseño" enlaza `design.md` y "Decisiones" gana una fila (tipo
`diseño`); no se toca nada más de la spec. Si `design` está en `skills.enabled`, añade la nota
"Revisar con `design:design-handoff` antes de `/implement`" y usa `design:ux-copy` para textos de
error, estados vacíos y confirmaciones. En la Trazabilidad del plan, cada criterio visual llevará
`verificación manual: <pantalla> a <anchos> contra <opcion-x.html>`.

**Refinado** (`/design-spec NNN --fix <qué>`): tras una revisión manual que pide otro valor o
comportamiento, actualiza `design.md` (y "Cambios a incorporar al sistema" si toca el sistema), con
la decisión `refinado`; `/plan NNN --fix` añade la tarea.

## 4. Movimiento

Cada animación de la pantalla es una ficha `M-<n>`:
- disparador (carga, entrada en pantalla, puntero fino, foco, toque) y si ocurre **una sola vez** o
  se repite;
- elementos y propiedades (solo `transform`, `opacity` o `filter` salvo justificación);
- duración y curva con tokens; estado inicial → final; secuencia o escalonado;
- técnica, en orden de preferencia: CSS → transiciones entre vistas del framework → Web Animations
  API → librería (solo si el diseño justifica que lo anterior no basta, y con ADR);
- versión **reducida** (`prefers-reduced-motion`), **sin JavaScript** (contenido completo y visible)
  y **táctil** (`hover: none`: qué se ve, o nada si el elemento no es interactivo);
- **coste** en JavaScript, contra el presupuesto de la constitución, y qué propiedades comparte con
  otras animaciones del mismo elemento (dos animaciones no animan la misma propiedad);
- fotogramas en el HTML de la composición.

Reglas de rendimiento, salvo prueba en contra registrada:
- sin `filter` animado sobre superficies grandes (paneles, cards a todo el ancho) ni
  `backdrop-filter` en elementos fijos;
- revelados disparados al entrar en pantalla (por tiempo) antes que ligados al scroll: los ligados
  al scroll traban el desplazamiento con trackpad cuando se acumulan;
- ningún trabajo por fotograma de scroll; un solo script común por patrón (revelado, luz que sigue
  al puntero), no uno por sección.

**Racionar el efecto firma:** respeta las "Reglas de uso" de `system.md` (cuántos momentos
protagonistas por página, dónde se permite el efecto firma, cuántos por pantalla en reposo). Una
composición que las rompe lo dice como riesgo y la regla se cambia en el sistema, no en silencio.

## 5. Spec de rediseño o con pantallas que el sistema no cubre

Un rediseño **siempre** es una spec propia; `/init` nunca lo hace. Antes de las composiciones (§2):

0. **Documentos de partida.** Si faltan `docs/design/brief.md`, `creative-direction.md` o
   `anti-cliches.md` (lo normal con un sistema `extracted`), haz la entrevista de diseño
   (`../../init/references/interview.md` → Ronda 4b; `/specify` ya la habrá hecho si la spec es de
   rediseño, y sus respuestas están en "Decisiones") y créalos desde `../../init/templates/design/`
   (`system-mode.md` §2.2), con aprobación del usuario, antes de generar opciones.
   Si falta `docs/design/nicho.md`, investiga antes el nicho (`nicho.md`).
1. Brief en modo spec (`system-mode.md` §5) con el contenido real de la spec. Si
   `creative-direction.md` tiene concepto firma, las opciones son composiciones de esa idea; si
   no, cada opción es una dirección con su idea y su momento firma (§2.3 de ese archivo).
2. Opciones en `docs/specs/NNN-<slug>/design/opcion-<a|b|c>.html` desde `option.html`: **3 por
   defecto, 2 si se mantiene la marca**; con la skill `design` si la sesión la ofrece (el canvas se
   enlaza en `design.md`), siempre también en HTML. Mismas reglas que en `/init`: distintas de verdad,
   contraste sin ningún "no cumple", sin clichés de `docs/design/anti-cliches.md`.
3. El usuario decide entre tres caminos:
   - **Elegir** una opción (o combinar elementos): va a "Decisiones" de `design.md` (tipo `diseño`).
   - **Afinar un eje de una opción** (tipografía, color o forma): sigue
     `system-mode.md` §2.8 en la carpeta de la spec y vuelve aquí con la base
     afinada. Hazlo **antes** de escribir "Cambios a incorporar al sistema": cambiarlo después
     obliga a `/design-spec NNN --fix` y `/plan NNN --fix`.
   - **Rehacer** las opciones: §2.7 de ese archivo, archivando en
     `docs/specs/NNN-<slug>/design/history/ronda-<N>/`.
4. "Cambios a incorporar al sistema" recoge todo lo que cambia de `system.md` (tokens, componentes,
   pantallas) y la primera tarea lo aplica, subiendo `version` de `system.md`.
5. **Migración por pantalla:** una tarea por pantalla (o grupo pequeño), cada una con su
   `verificación manual:` contra el HTML elegido y el test de "solo tokens". Las pantallas no
   migradas siguen funcionando con el sistema anterior hasta su tarea; si conviven dos versiones de
   tokens, dilo en Rollout y en Riesgos.
6. Si el rediseño cambia la dirección creativa, `creative-direction.md` se actualiza en la misma
   primera tarea, con aprobación del usuario.

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
- **Ronda de exploración si falta o es floja.** Si la spec introduce los íconos o la tarjeta y
  `system.md` no los define (sistemas extraídos o anteriores a 1.13.0), o lo que define es genérico
  (la base de la plantilla, un logo sobre un degradado, iniciales sobre un cuadrado), antes de
  diseñar el resto: 2–3 direcciones en `docs/specs/NNN-<slug>/design/opcion-<a|b|c>.html` con solo
  la sección "Al compartir" de `option.html`, **cada una con tarjeta e ícono**, cada una apoyada en
  una pieza distinta del sitio (p. ej. la tarjeta del hero, el índice o la barra, un detalle de
  código o de producto) y con los datos reales de dos rutas. El usuario elige o combina (tarjeta de
  una, ícono de otra) y la elección va a "Decisiones" (tipo `diseño`) y a "Cambios a incorporar al
  sistema", con la composición **con medidas** (`system-mode.md` §2.4 paso 10).
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
- genera `system.html` desde el HTML elegido con la cabecera "sistema de diseño aprobado";
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
