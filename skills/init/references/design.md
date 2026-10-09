# Diseño: sistema de diseño y opciones en HTML

Lo usa `/init` (y `/init --upgrade` paso 9) en proyectos con interfaz: `frontend`, `fullstack`,
`mobile`, o un paquete de esos tipos en un monorepo. En `backend` y `library` no se escribe el
bloque `design` de `project.yaml`.

| Caso | Qué haces |
|---|---|
| Greenfield con interfaz | §2: entrevista de diseño y opciones en HTML; la elegida es el sistema |
| Brownfield con interfaz | §3: **solo si el usuario acepta**, documentas el diseño que ya usa el código |
| Rediseño | Nunca aquí: es una spec propia (`/specify`, y `/plan` sigue `../../plan/references/design.md`) |

El entregable visual es siempre **HTML en el repo** (`docs/design/*.html`, a partir de
`../templates/design/option.html`): se abre sin red cuantas veces se quiera. Lo escrito vive en
`docs/design/system.md` (`../templates/design/system.md`).

## 1. Herramientas

Comprueba qué ofrece la sesión antes de empezar y dilo en una línea:

- **Skill `design`** (crea un artifact Design —canvas— a partir de un brief): si está, genera las
  opciones con ella pasando el brief del §5 como `args` de la herramienta `Skill`, y guarda el
  enlace del canvas en `design.canvas`. **Además** escribe cada opción en HTML (§2.4): el canvas es
  para retoques finos; el HTML es lo que se versiona y lo que leen las demás skills.
- **Plugin `design` de Anthropic** (`design:design-system`, `design:design-critique`,
  `design:accessibility-review`…): no genera visuales. Úsalo para auditar y documentar el sistema
  y para revisar las opciones. Solo si está en `skills.enabled` (contrato → "Dependencias
  externas").
- Sin ninguna de las dos: genera el HTML directamente desde el brief con la plantilla y revisa el
  contraste con la propia página. Nunca bloquees `/init` por su ausencia.

## 2. Greenfield

### 2.1 Entrevista
`interview.md` → Ronda 4b. Lo que ya responden la constitución o el tipo (nivel WCAG, toque
≥ 44 pt/48 dp en `mobile`) no se pregunta: se anota como `implícita`.

### 2.2 Documentos de partida
Con las respuestas escribe, desde `../templates/design/`:
- `docs/design/brief.md`.
- `docs/design/creative-direction.md`: referencias de sensación **con nombre** (productos, sitios o
  apps concretos, no adjetivos) y, si el usuario lo dio, el **concepto firma**: la idea que debe
  reconocerse en el producto y el momento en que se ve (p. ej. "el código se escribe y se compila
  en la tarjeta de presentación"). Si no lo dio, la sección dice "lo deciden las opciones".
- `docs/design/anti-cliches.md`: conserva las filas de "todos los tipos" y las del tipo del
  proyecto, borra las demás, añade los clichés que el usuario rechazó en "Referencias" y los
  **del sector** del producto (Ronda 4b), cada uno con una alternativa dentro de la dirección, no
  solo la prohibición.

Muéstralos y pide aprobación antes de generar nada: las opciones cuestan tokens.

### 2.3 Número de opciones
**3 por defecto. 2 si el usuario ya trae marca y paleta cerradas** (las opciones cambian
tipografía, forma, densidad y composición, no el color). Regístralo en `brief.md` (`options:`).

Qué se explora depende de `creative-direction.md`:
- **Con concepto firma:** la dirección ya está decidida; las opciones son **composiciones** de esa
  idea (cómo se ordena y se presenta el contenido principal, dónde vive el momento firma), con la
  misma estética de partida.
- **Sin concepto firma:** cada opción es una **dirección** con su propia idea y su propio momento
  firma.

### 2.4 Generar las opciones
Por cada opción, `docs/design/opciones/opcion-<a|b|c>.html` desde `option.html`:

1. Tokens completos en el bloque de estilos `tokens` (si hay modo oscuro, **todos** los colores
   redefinidos). Para rellenar los bloques, busca la etiqueta **después** del comentario de
   instrucciones de la plantilla (el comentario los nombra).
2. Componentes ajustados a la dirección en el bloque `components`, solo con tokens.
3. Tipografía real: la fuente de marca no es una fuente del sistema (system-ui, Segoe, Roboto,
   Arial, Verdana, Trebuchet, Bahnschrift…) salvo que el brief lo pida; varían por equipo y aplanan
   cualquier dirección. Tampoco se elige por estética: escribe antes qué debe lograr la letra
   según `brief.md` (legibilidad en el contexto de uso, tono, cifras, idioma) y justifica cada
   familia contra eso en la "Idea" de la opción. Incrusta en el bloque `fonts` cada peso que
   uses como `@font-face` con el subconjunto latino en woff2 y base64, tomado del mismo paquete o
   archivo que usará la app (p. ej. `@fontsource/<familia>/files/<familia>-latin-400-normal.woff2`);
   sin él, el usuario elegiría sobre la fuente de reemplazo. Comprueba que carga
   (`[...document.fonts].some(f => f.family === '<familia>' && f.status === 'loaded')`;
   `document.fonts.check()` da `true` aunque la fuente no exista).
4. Pares de contraste: deja en "Color" solo los pares cuyos tokens existen en la opción (marca los
   demás con `data-optional`, que la página oculta si falta un token).
5. Contenido **real**: nombre del producto y textos de la primera feature del roadmap, datos de
   prueba realistas; nunca lorem ipsum ni cifras inventadas.
6. Pantallas: 1–2 principales en cada ancho de `design.widths`. Lo que cambia con el ancho se
   escribe con `@container`, no con `@media` (el marco no es la ventana).
7. **Idea** en una frase, anclada en un dato concreto de `brief.md` (público, contexto de uso,
   producto, lugar) o en el concepto firma; debajo, las 2–3 decisiones de **estructura** que la
   materializan, y el riesgo asumido. Ejemplo: "Campo al sol — se usa en el teléfono a pleno sol:
   bordes gruesos y sombra dura, cuerpo de 19 px, botones de 56 px". Una idea que no cambia la
   estructura es solo un nombre: rehaz la opción.
8. Un solo **momento firma**, derivado de la idea, dibujado en fotogramas (inicio → medio → final)
   con su versión sin movimiento; el resto, sobrio.

Las opciones deben ser **distintas de verdad**: cambian **siempre la composición** de la pantalla
principal (orden, jerarquía y forma de presentar el contenido principal) y además al menos uno de
familia de color, pareja tipográfica, forma y densidad. Si comparten esqueleto (mismas secciones
en el mismo orden, mismos textos, misma rejilla) son la misma opción con otra piel: rehazlas. Evita
los clichés de `anti-cliches.md` y, salvo que el brief lo pida, los rasgos por defecto de las
interfaces generadas (§6).

**Antes de enseñarlas:**
- Repasa cada opción contra §6 y `anti-cliches.md`, rasgo por rasgo, haya o no plugin `design`;
  corrige lo que aparezca o, si el brief lo pide, dilo en su "Idea". Compara también las opciones
  entre sí con la regla de composición de arriba.
- Abre cada HTML en un navegador si lo hay (o pídele al usuario que lo abra) en claro, oscuro y
  "Sin movimiento". Ningún par de "Color" puede salir "no cumple": corrige los tokens, no el umbral.
- Si el plugin `design` está habilitado: `design:design-critique` y `design:accessibility-review`
  sobre cada una; corrige lo grave antes de presentarla.

**Presenta** una tabla (opción, idea, riesgo, ruta del HTML y enlace del canvas si lo hay) y pide
que elija una o combine elementos.

### 2.5 Elección → sistema
1. `docs/design/system.md` con `source: chosen`, `status: draft`: los tokens de la opción elegida
   (y lo combinado; con modo oscuro, columnas "Claro" y "Oscuro" y el contraste como
   `13.0:1 · 15.2:1`), contraste de cada color de texto (el que calculó la página), componentes con
   estados, pantallas principales y la elección en "Decisiones" (tipo `diseño`, fuente `usuario`).
   Con el plugin habilitado, redacta componentes y patrones con `design:design-system document`.
2. `docs/design/system.html`: la opción elegida ajustada, con "sistema de diseño aprobado" en la
   cabecera. Las opciones se quedan en `opciones/` (también las descartadas).
3. `.ai/project.yaml → design`: `status: draft` (pasa a `approved` cuando el usuario aprueba
   `system.md`), `source: chosen`, `canvas`, `widths`.
4. Constitución: el principio condicional "La interfaz usa solo el sistema de diseño".
5. `AGENTS.md` → Documentación: enlaces a `system.md` y `system.html`.

### 2.6 Proyecto base
En `greenfield.md` §2, los tokens se escriben en un único archivo de tema del stack (variables CSS,
`src/theme/tokens.css` en Ionic, `ThemeData` de Flutter) **conectados al tema de la librería de
componentes** (`../../plan/references/design.md` §4), y la auditoría de §3 compara también con
`system.md`: tamaño de controles, margen lateral de campos y pantallas, colores y radios por
defecto de la librería.

### 2.7 Rehacer las opciones antes de elegir

`/init --upgrade --redo-options`. Para cuando las opciones ya se generaron, ninguna convence y aún
no hay sistema aprobado. Sin esto, el usuario aprueba una opción a medias para poder abrir un
rediseño, o pide regenerarlas a mano sin procedimiento.

**Condiciones:** existe `docs/design/opciones/` y `design.status` no es `approved`. Si es
`approved`, detente: cambiar el sistema es un rediseño (spec propia, `/specify "rediseño de …"`).
Si es `declined` o el sistema es `extracted`, no aplica: es §3b o un rediseño.

1. **Qué falló.** Pregunta en una sola ronda qué no convenció de cada opción y qué se conserva
   (una opción como base, o elementos sueltos de otras). Repite de la Ronda 4b solo lo que cambie
   la siguiente ronda: casi siempre el concepto firma (punto 5), los clichés del sector y las
   referencias. Las respuestas van a "Decisiones" de `brief.md` (tipo `diseño`, fuente `usuario`).
2. **Documentos de partida.** Actualiza `brief.md`, `creative-direction.md` y `anti-cliches.md`
   (§2.2) con lo nuevo: lo rechazado pasa a `anti-cliches.md` con su alternativa, y una base
   elegida se convierte en el concepto firma. Muestra el cambio y pide aprobación.
3. **Archiva** las opciones actuales en `docs/design/opciones/history/ronda-<N>/` (`N` = 1, 2…,
   la primera libre), con sus HTML intactos. Si había un `system.md`/`system.html` en `draft`
   de una elección anterior, archívalos en esa misma carpeta y deja `design.status: none` y
   `source: null` hasta la nueva elección. Nunca borres una ronda.
4. **Genera** la nueva ronda con §2.3–§2.4 (y la skill `design` si está; el canvas nuevo sustituye a
   `design.canvas` y el anterior queda citado en "Decisiones"). Si hay una base conservada, las
   opciones son composiciones de su idea y ninguna repite el esqueleto de la ronda anterior.
5. **Presenta** la tabla de §2.4 con una columna más, "Qué cambia respecto a la ronda <N>", y
   sigue con §2.5.

En un rediseño (spec propia), las opciones viven en la carpeta de la spec: aplica los mismos pasos
desde `/plan` (`../../plan/references/design.md` §2), archivando en
`docs/specs/NNN-<slug>/design/history/ronda-<N>/`.

### 2.8 Ronda acotada a un eje

Para cuando una opción ya convence en composición pero falla en un solo aspecto ("la A, pero no me
gusta la letra"). Rehacer las opciones completas tiraría lo que funciona.

**Cómo se pide:** en `/init`, `--upgrade --redo-options --only <eje> --base <a|b|c>`; en `/plan`
(opciones de una spec), al elegir (`../../plan/references/design.md` §2, paso 3). Ejes:
`tipografia`, `color`, `forma` (radios, bordes, sombras, densidad). La composición no es un eje:
cambiarla es §2.7. Mismas condiciones que §2.7: sin sistema `approved`.

1. **Congela la base.** Composición, textos y los demás ejes no cambian. Solo cambian los tokens
   del eje:
   | Eje | Tokens que cambian |
   |---|---|
   | `tipografia` | `--font-*`, `--text-*` (tamaño, interlineado, peso, interletrado) y el bloque `fonts` |
   | `color` | `--color-*` |
   | `forma` | `--radius-*`, `--border-*`, `--shadow-*`, `--space-*` |
   Un ajuste de otro eje que el usuario pida a la vez (p. ej. aligerar bordes) se aplica a la
   base **antes** de la comparación y se registra aparte, nunca mezclado en las variantes.
2. **Criterios primero.** Antes de proponer variantes, escribe 3–4 criterios del eje sacados de
   `brief.md` (tipografía: legibilidad en el contexto de uso, tono, cifras, acentos; color:
   contraste, lectura al sol, significado de los colores en el sector; forma: toque mínimo,
   densidad). Muéstralos al usuario junto con las variantes.
3. **2–3 variantes**, cada una justificada contra los criterios, con su riesgo. Nada de §6 sin
   motivo del brief.
4. **Lámina comparativa** desde `../templates/design/eje.html`, en la misma carpeta que las
   opciones (`eje-<eje>.html`): las mismas piezas de la base con cada variante, lado a lado al ancho
   más chico de `design.widths` y el hero a ancho completo. La página comprueba la carga de las
   fuentes y el contraste de cada variante y tiene "Simular sol"; anota el peso de las fuentes en
   KB. Ábrela en un navegador (o pide al usuario que lo haga) antes de enseñarla: ninguna fuente
   "no cargada", ningún par que no cumpla. Con la skill `design`, añade la lámina al canvas.
5. **Elección.** La variante elegida se aplica a la opción base (su HTML y el canvas); la decisión
   va a "Decisiones" de `brief.md` (o del plan) con el criterio que la decidió; la lámina se
   archiva en `history/ronda-<N>-<eje>/`. Después se sigue con §2.5 (o con el plan) usando la base
   ya afinada. Se puede encadenar otra ronda de otro eje.

## 3. Brownfield: documentar el diseño existente

**Pregunta en la Fase 0**, al detectar interfaz y antes de explorar: *"¿Documento el diseño que
usa hoy el código? Extraigo colores, tipografía y componentes, audito contraste y valores fijos, y
dejo `docs/design/system.md` y una vista en HTML. No cambio código."* Con un **no**:
`design.status: declined`, no lances el subagente G y no vuelvas a preguntar (tampoco
`--upgrade`).

Con un **sí**, la regla es **fidelidad**: el documento describe la app que ve el usuario, no una
interpretación. Nada se dibuja a mano ni se redacta: lo que no se puede capturar o leer del código
queda marcado como pendiente.

1. **Subagente G** (`explore-agents.md`) en la Fase 1, junto a los demás: tokens, valores fijos,
   lo declarado que no se carga, **inventario completo de vistas** y recursos de marca.
2. **Datos de prueba.** Las capturas se hacen **solo con datos de prueba**, nunca con datos reales.
   Para tenerlos, en este orden: helpers o fixtures de los tests de pantalla del proyecto (p. ej.
   un almacén simulado), una base de datos de pruebas con su semilla (`migrate --seed`, factories,
   fixtures) en un entorno local aparte, o pregunta. Si el usuario no quiere capturas, explícale
   que sin ellas el HTML no puede ser fiel y ofrece la base de pruebas; si aun así no, sigue sin
   capturas (paso 4, estado `sin captura`).
3. **Capturas y medidas de todas las vistas** del inventario, en cada ancho de `design.widths`, con
   el rol que haga falta para verlas (usuarios de prueba). Es automático (Playwright o equivalente):
   no te limites a las "principales". Incluye estados que se puedan provocar con datos de prueba
   (vacío, error de validación, modal abierto). Van a `docs/design/capturas/<vista>-<ancho>.png`.
   En cada vista **mide** los estilos calculados (`getComputedStyle`): fondo y texto de pantalla,
   barras, tarjetas y filas, familia de fuente, margen lateral, alto de botones y campos; con
   `prefers-color-scheme: dark` emulado si el código declara modo oscuro. `system.md` documenta
   **lo medido**: si difiere de lo que declara el código (G), lo medido manda y la diferencia es
   deuda `DS`.
4. **Inventario de vistas** en `system.md`: una fila por vista con ruta o plantilla, rol, capturas
   y estado (`capturada` · `sin captura (motivo)` · `no accesible (motivo)`). El resumen final dice
   cuántas de cuántas se capturaron.
5. **Auditoría:** con el plugin, `design:design-system audit` sobre el informe de G y
   `design:accessibility-review` sobre las capturas; sin él, la misma revisión con el checklist de
   `system.md` (contraste, valores fijos, estados, toque mínimo).
6. `system.md` con `source: extracted`, `status: draft`, `extracted_with: <versión del plugin>`: el
   sistema **tal como está**, sin mejoras. Lo no determinado se marca y se pregunta. La deuda va a
   "Deuda de diseño" con IDs (`DS1`, `DS2`…) y evidencia.
7. `system.html` desde `option.html` con los valores reales; los pares que no cumplen se ven en
   rojo (es deuda, no se corrige aquí):
   - **Marca:** el logo del repo (SVG, o PNG/WebP en base64) y el nombre comercial que muestra la
     app, no el nombre del repositorio.
   - **Textos:** copiados de las vistas y plantillas del código (títulos, botones, mensajes),
     nunca redactados. Datos de ejemplo: los de prueba.
   - **Pantallas:** todas las vistas del inventario como galería de capturas
     (`<img src="capturas/<vista>-<ancho>.png" alt="<vista> a <ancho> px">`), agrupadas por sección
     de la app; una vista sin captura es un hueco con su ruta y el motivo, **nunca una maqueta**.
   - **Componentes:** recortes de las capturas (botón, campo, fila, tarjeta, aviso, menú), no los
     sintéticos de la plantilla, que no reproducen iconos, librerías ni detalles reales.
8. **Roadmap:** las `DS` prioritarias se proponen como objetivos con la conciliación de
   `brownfield.md` §4; el usuario decide.
9. Constitución: el principio "solo tokens" se propone con la regla de "Código previo": aplica a
   pantallas nuevas o modificadas; el código anterior no bloquea.

No propongas rediseño ni generes opciones. Si el usuario lo pide, el resumen indica que es una
spec propia (`/specify "rediseño de …"`).

### 3b. Re-extraer un sistema ya documentado

`/init --upgrade --redo-design`, u ofrecido por `--upgrade` cuando `system.md` es
`source: extracted` y `extracted_with` falta o es anterior a 1.11.2. Sirve para rehacer con estas
reglas una documentación hecha con un procedimiento anterior o que ya no se parece a la app. No
aplica a un sistema `chosen` (cambiarlo es un rediseño: spec propia).

1. **Archiva, no borres:** mueve `system.md` y `system.html` a `docs/design/history/`
   (`system.v<N>.md`, `system.v<N>.html`, con `N` = versión mayor anterior) y las capturas a
   `docs/design/history/capturas-v<N>/`.
2. **Re-extrae** con los pasos 1–7 de §3 (sin volver a preguntar si documentar: el usuario ya dijo
   que sí).
3. **Concilia la deuda:** compara cada `DS` del sistema archivado con lo nuevo.
   - Sigue ocurriendo → conserva su **mismo ID** con evidencia actualizada.
   - Ya no ocurre → fila con su ID y estado `no se confirma (re-extracción <fecha>: <evidencia>)`.
   - Problema nuevo → ID nuevo a partir del mayor usado (nunca reutilices uno).
   Si la `DS` vieja mezclaba dos problemas, consérvala para el que sigue y crea uno nuevo para el
   otro, y dilo en "Decisiones".
4. **Referencias:** lista dónde se citan las `DS` y el sistema (roadmap, specs, planes,
   constitución, `AGENTS.md`) y qué cambia para cada una; **no las edites** sin confirmación. El
   validador avisa si algo cita una `DS` que no existe ni en el sistema ni en `history/`.
5. `system.md` sube la versión **menor** (`1.0.0` → `1.1.0`), `extracted_with` nuevo, `status:
   draft` (y `design.status: draft` en `project.yaml`) hasta que el usuario lo apruebe, y una fila en
   "Decisiones" (tipo `diseño`, "re-extracción con el procedimiento X").

## 4. `/init --upgrade`

`upgrade.md` paso 9 ejecuta **solo** el §3 (pregunta incluida) sobre un proyecto ya inicializado, sin
re-explorar el resto del código: lanza únicamente el subagente G. Con un sistema extraído por un
procedimiento anterior, ofrece §3b (re-extraer); `--redo-design` lo ejecuta directamente.
`--redo-options` sigue §2.7 (rehacer las opciones de un proyecto nuevo antes de elegir sistema);
con `--only <eje> --base <opción>`, §2.8 (afinar un solo eje de una opción).

## 5. Brief (para la skill `design` y para escribir el HTML)

```
Proyecto: <nombre> — <descripción de AGENTS.md> (<tipo>, <stack de UI>)
Modo: sistema | spec NNN-slug
Objetivo: <de brief.md o de la spec>
Dirección creativa: <resumen de docs/design/creative-direction.md, con sus referencias con nombre>
Concepto firma: <el de creative-direction.md, o "ninguno: cada opción propone el suyo">
Clichés del sector: <los de anti-cliches.md, con su alternativa>
Sistema de diseño: <tokens clave de system.md, o "a definir" en modo sistema>
Contenido real: <textos y datos exactos; nunca lorem ipsum>
Artboards:
  - Opciones A, B (y C) con composición distinta de la pantalla principal; cada una con su idea
    en una frase, anclada en un dato del brief, y las decisiones de estructura que la materializan
  - Cada una a <design.widths>
  - Estados: vacío, carga, error, foco, deshabilitado
  - Movimiento como fotogramas anotados (inicio → medio → final), con versión sin movimiento
Restricciones: <constitución: WCAG, toque mínimo, plataforma>; sin clichés de anti-cliches.md;
  solo tokens del sistema (modo spec)
```

En modo sistema los artboards son *style tiles*: paleta, tipografía, escala de espaciado, radios,
botones, campos, listas o tarjetas, avisos y una pantalla principal.

## 6. Rasgos por defecto que hay que evitar

Salvo que el brief los pida, una opción no se apoya en los rasgos que delatan una interfaz
generada sin dirección:
- fondo crema con serif de alto contraste y acento terracota; negro casi puro con un único acento
  ácido;
- todo troceado en tarjetas idénticas con el mismo radio y la misma sombra suave, y degradados
  como decoración; en especial la tríada de tarjetas icono + título + texto para "quiénes somos"
  o las ventajas;
- fuentes del sistema como tipografía de marca, o fuentes de moda elegidas sin motivo del brief
  (Bricolage Grotesque, Epilogue, Space Grotesk, Inter, DM Sans, Manrope, Plus Jakarta Sans);
  botones y filtros en píldora con hero de color
  plano y un botón de acento como única decisión;
- etiquetas en mayúsculas espaciadas sobre cada título, metadatos unidos con puntos medios,
  monoespaciada para cualquier dato pequeño, flechas añadidas a todos los botones;
- numeración decorativa (01, 02, 03) en contenido que no es una secuencia;
- animaciones de entrada en cada sección en lugar de un único momento con sentido;
- el mismo esqueleto de página en todas las opciones, con solo el color, el radio y la sombra
  cambiados.

Gasta la audacia en un solo elemento reconocible y mantén el resto sobrio.
