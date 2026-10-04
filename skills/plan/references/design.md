# Diseño en `/plan`

Aplica a specs con interfaz cuando `.ai/project.yaml → design.status` es `draft` o `approved`.
Formato del sistema y de los HTML: `../../init/references/design.md` (§2.4 y §5) y
`../../init/templates/design/`.

## 1. Spec que usa el sistema (lo habitual)

En "Contratos y datos":
- Cada pantalla, con los **componentes del sistema** que usa y sus estados (vacío, carga, error,
  éxito). Ningún valor visual nuevo: si falta algo (un componente, una variante, un token), va a
  la subsección **"Cambios a incorporar al sistema"** del plan, con el valor propuesto y el motivo.
- Si hay "Cambios a incorporar al sistema", la **primera tarea** de `/tasks` actualiza
  `docs/design/system.md` y `system.html` (con su entrada en "Decisiones") antes del código.
- Si `design` está en `skills.enabled`, añade la nota: "Revisar con `design:design-handoff` antes de
  `/implement`" y usa `design:ux-copy` para textos de error, estados vacíos y confirmaciones.
- En Trazabilidad, cada criterio visual lleva `verificación manual: <pantalla> a <design.widths>
  contra system.html` (o contra el HTML de la spec del §2).

## 2. Spec de rediseño o con pantallas que el sistema no cubre

Un rediseño **siempre** es una spec propia; `/init` nunca lo hace. Antes del Paso 3 del plan:

0. **Documentos de partida.** Si faltan `docs/design/brief.md`, `creative-direction.md` o
   `anti-cliches.md` (lo normal con un sistema `extracted`), haz la entrevista de diseño
   (`../../init/references/interview.md` → Ronda 4b; `/specify` ya la habrá hecho si la spec es de
   rediseño, y sus respuestas están en "Decisiones") y créalos desde `../../init/templates/design/`
   (`../../init/references/design.md` §2.2), con aprobación del usuario, antes de generar opciones.
1. Brief en modo spec (`../../init/references/design.md` §5) con el contenido real de la spec.
2. Opciones en `docs/specs/NNN-<slug>/design/opcion-<a|b|c>.html` desde `option.html`: **3 por
   defecto, 2 si se mantiene la marca**; con la skill `design` si la sesión la ofrece (el canvas se
   enlaza en el plan), siempre también en HTML. Mismas reglas que en `/init`: distintas de verdad,
   contraste sin ningún "no cumple", sin clichés de `docs/design/anti-cliches.md`.
3. El usuario elige; la elección va a "Decisiones" del plan (tipo `diseño`).
4. "Cambios a incorporar al sistema" recoge todo lo que cambia de `system.md` (tokens, componentes,
   pantallas) y la primera tarea lo aplica, subiendo `version` de `system.md`.
5. **Migración por pantalla:** una tarea por pantalla (o grupo pequeño), cada una con su
   `verificación manual:` contra el HTML elegido y el test de "solo tokens". Las pantallas no
   migradas siguen funcionando con el sistema anterior hasta su tarea; si conviven dos versiones de
   tokens, dilo en Rollout y en Riesgos.
6. Si el rediseño cambia la dirección creativa, `creative-direction.md` se actualiza en la misma
   primera tarea, con aprobación del usuario.

## 3. Del sistema extraído al elegido

Cuando la spec sustituye un sistema `source: extracted`, la primera tarea:
- reescribe `system.md` con `source: chosen` y **versión mayor**, la elección en "Decisiones" y la
  deuda `DS` que resuelve marcada "la resuelve NNN" (pasa a "resuelta por NNN" en T092);
- genera `system.html` desde el HTML elegido con la cabecera "sistema de diseño aprobado";
- actualiza `.ai/project.yaml → design` (`source: chosen`; `status: approved` cuando el usuario
  aprueba `system.md`), que el validador compara con el frontmatter;
- las capturas de `docs/design/capturas/` se rehacen al cerrar la spec (T092), en claro y oscuro.

## 4. Conectar los tokens con la librería de componentes

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

## 5. Tests del sistema

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
- **Fuente dentro de la app:** el build contiene sus archivos y ningún CSS/JS pide fuentes o CDN
  externos; en pantalla, la fuente consta como cargada (`document.fonts` con `status: loaded`).

## 6. Estados de pantalla

- **Carga y avisos para lectores de pantalla:** una sola región de estado (`<output>` o
  `role="status"`) siempre montada; el texto llega **después** de montarla (p. ej. en una tarea
  posterior) y se retira al terminar. Una región que aparece ya con su texto no se anuncia de forma
  fiable, y dos regiones a la vez compiten.
- **Errores:** `role="alert"` con qué pasó, qué pasa con los datos y la acción para reintentar.
