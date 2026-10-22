# Diseño: sistema de diseño por criterios

Modo `system` de `/design-spec` (lo llaman `/init` y `/init --upgrade` paso 9; también se ejecuta
solo) en proyectos con interfaz: `frontend`, `fullstack`, `mobile`, o un paquete de esos tipos en
un monorepo. En `backend` y `library` no se escribe el
bloque `design` de `project.yaml`.

| Caso | Qué haces |
|---|---|
| Greenfield con interfaz | §2: entrevista de diseño, criterios y ciclo de candidatos; el aceptado es el sistema |
| Brownfield con interfaz | §3: **solo si el usuario acepta**, documentas el diseño que ya usa el código |
| Rediseño | Nunca aquí: es una spec propia (`/specify`, y `/design-spec NNN` sigue `spec-mode.md` §5) |

El entregable visual es siempre **HTML en el repo** (`docs/design/*.html`, a partir de
`../../init/templates/design/option.html`): se abre sin red cuantas veces se quiera. Lo escrito vive en
`docs/design/system.md` (`../../init/templates/design/system.md`).

## 1. Herramientas

Comprueba qué ofrece la sesión antes de empezar y dilo en una línea:

- **Skill `design`** (crea un artifact Design —canvas— a partir de un brief): si está, genera las
  candidatos con ella pasando el brief del §5 como `args` de la herramienta `Skill`, y guarda el
  enlace del canvas en `design.canvas`. **Además** escribe cada opción en HTML (§2.4): el canvas es
  para retoques finos; el HTML es lo que se versiona y lo que leen las demás skills.
- **Plugin `design` de Anthropic** (`design:design-system`, `design:design-critique`,
  `design:accessibility-review`…): no genera visuales. Úsalo para auditar y documentar el sistema
  y para revisar el candidato aceptado. Solo si está en `skills.enabled` (contrato → "Dependencias
  externas").
- Sin ninguna de las dos: genera el HTML directamente desde el brief con la plantilla y revisa el
  contraste con la propia página. Nunca bloquees `/init` por su ausencia.

## 2. Greenfield

### 2.1 Investigación del nicho y entrevista
Antes de la entrevista, investiga el nicho con `nicho.md` (profundidad según el tipo de producto) y
escribe `docs/design/nicho.md`. Después, `../../init/references/interview.md` → Ronda 4b, que propone los territorios de
identidad salidos de esa investigación. Lo que ya responden la constitución o el tipo (nivel WCAG, toque
≥ 44 pt/48 dp en `mobile`) no se pregunta: se anota como `implícita`.

### 2.2 Documentos de partida
Con las respuestas escribe, desde `../../init/templates/design/`:
- `docs/design/nicho.md` (si no se escribió ya en §2.1), con el territorio elegido en "Elección".
- `docs/design/brief.md`.
- `docs/design/creative-direction.md`: referencias de sensación **con nombre** (productos, sitios o
  apps concretos, no adjetivos) y, si el usuario lo dio, el **concepto firma**: la idea que debe
  reconocerse en el producto y el momento en que se ve (p. ej. "el código se escribe y se compila
  en la tarjeta de presentación"). Si no lo dio, la sección dice "lo decide el ciclo".
  Con un territorio de identidad elegido (`nicho.md` §4), escribe también "Identidad",
  "Movimiento" y "Superficies y fondos" desde ese territorio.
- `docs/design/anti-cliches.md`: conserva las filas de "todos los tipos" y las del tipo del
  proyecto, borra las demás, añade los clichés que el usuario rechazó en "Referencias" y los
  **del sector** del producto ("Lo que todos repiten" de `nicho.md` y Ronda 4b), cada uno con una alternativa dentro de la dirección, no
  solo la prohibición.

Muéstralos y pide aprobación antes de generar nada (con los criterios de §2.3).

### 2.3 Criterios del sistema
Antes de generar nada, escribe y aprueba con el usuario los criterios del sistema
(`criterios.md`) en `docs/design/criterios.json` y en una tabla en `brief.md` ("Criterios de
diseño"):
- **Puertas** de `criterios.md` §2, con el contraste y el toque de la constitución.
- **KPIs** de la pantalla principal según su modo (`criterios.md` §4), con los textos reales de la
  primera feature del roadmap, y `fonts_loaded` con las familias elegidas.
- **Rúbrica** de `criterios.md` §5, donde `sistema` se lee como "adecuación al brief y al nicho"
  (`brief.md`, `nicho.md`, `creative-direction.md` y `anti-cliches.md`).
- `threshold`, `floor` y `budget` de `.ai/project.yaml → design`.

Muéstralos junto con los documentos de partida y pide aprobación: los candidatos cuestan tokens.

### 2.4 El ciclo del sistema
Sigue `evaluacion.md` con un candidato de sistema en vez de una pantalla. Cada candidato son dos
archivos en `docs/design/candidatos/`:
- `c<N>.html` desde `option.html`: tokens completos (si hay modo oscuro, **todos** los colores
  redefinidos), componentes con estados, tipografía, superficies y "Al compartir". Para rellenar los
  bloques, busca la etiqueta **después** del comentario de instrucciones de la plantilla.
- `c<N>-pagina.html` desde `pagina.html`: la pantalla principal como página real con contenido
  real, sobre esos tokens. Es lo que mide `evaluate.mjs`.

Reglas de cada candidato:
1. **Tipografía real**, incrustada como `@font-face` woff2 en base64 desde el mismo paquete que usará
   la app (p. ej. `@fontsource/<familia>/files/<familia>-latin-400-normal.woff2`). La fuente de
   marca no es una del sistema salvo que el brief lo pida; se justifica contra lo que el brief pide
   de la letra (legibilidad en el contexto de uso, tono, cifras, idioma).
2. **Pares de contraste:** en "Color" de `c<N>.html`, solo los pares cuyos tokens existen (los demás
   con `data-optional`); ninguno puede salir "no cumple": se corrigen los tokens, no el umbral.
3. **Contenido real:** nombre del producto y textos de la primera feature del roadmap, datos de
   prueba realistas; nunca lorem ipsum ni cifras inventadas. Los recursos de marca que existen
   (logo, fotos) se abren y se usan tal como son.
4. **Pantallas** en cada ancho de `design.widths`; en `c<N>.html`, lo que cambia con el ancho se
   escribe con `@container`, no con `@media`.
5. **Movimiento** con los tokens y reglas de `movimiento.md`, solo el que pida el brief.
6. **Superficies y fondos** del territorio de `nicho.md`; el texto se mide sobre la **zona más
   difícil** del fondo (`--surface-worst`).
7. **Marca en el navegador y al compartir** (sección "Al compartir"): ícono que sale de una marca que
   el candidato ya muestra (sin logo, monograma provisional marcado como tal; el plugin no diseña
   logos), revisado a 16 y 32 px en pestaña clara y oscura; tarjeta para compartir (sitio indexable)
   que **repite una pieza reconocible** del candidato, con datos reales y marca y título en la zona
   segura. Las reglas `c-share` de la plantilla son andamiaje.
8. Antes de medir, repasa el candidato contra `anti-cliches.md` y §6: cada rasgo presente baja la
   nota de `plantilla` y el evaluador lo verá.

Con el plugin `design` habilitado, `design:accessibility-review` sobre el candidato aceptado antes
de presentarlo. **Presenta** el acta del ciclo (candidatos con su resultado y el aceptado con sus
puertas, KPIs y notas) y abre el aceptado; el usuario lo aprueba o ajusta criterios.

### 2.5 Aceptado → sistema
1. `docs/design/system.md` con `source: chosen`, `status: draft`: los tokens del candidato aceptado
   (con modo oscuro, columnas "Claro" y "Oscuro" y el contraste como `13.0:1 · 15.2:1`), contraste
   de cada color de texto (el que calculó la página), componentes con estados, "Marca en el navegador
   y al compartir" (dibujo del ícono y, si el sitio es indexable, la tarjeta con su pieza de origen,
   la composición **con medidas**, los datos y su origen, variantes y modo de generación), pantallas
   principales, los criterios con los que se aceptó y el acta resumida en "Decisiones" (tipo
   `diseño`, fuente `usuario` al aprobar).
   Con el plugin habilitado, redacta componentes y patrones con `design:design-system document`.
2. `docs/design/system.html`: el candidato aceptado, con "sistema de diseño aprobado" en la
   cabecera. Los candidatos se quedan en `candidatos/` (también los descartados).
3. `.ai/project.yaml → design`: `status: draft` (pasa a `approved` cuando el usuario aprueba
   `system.md`), `source: chosen`, `canvas`, `widths`.
4. Constitución: el principio condicional "La interfaz usa solo el sistema de diseño".
5. `AGENTS.md` → Documentación: enlaces a `system.md` y `system.html`.

### 2.6 Proyecto base
En `../../init/references/greenfield.md` §2, los tokens se escriben en un único archivo de tema del stack (variables CSS,
`src/theme/tokens.css` en Ionic, `ThemeData` de Flutter) **conectados al tema de la librería de
componentes** (`spec-mode.md` §9), y la auditoría de §3 compara también con
`system.md`: tamaño de controles, margen lateral de campos y pantallas, colores y radios por
defecto de la librería.

### 2.7 Repetir el ciclo antes de aprobar

`/design-spec system --redo-options` (o `/init --upgrade --redo-options`). Para cuando el ciclo
terminó sin aceptado o el usuario no aprueba el aceptado y aún no hay sistema aprobado. Si
`design.status` es `approved`, detente: cambiar el sistema es un rediseño (spec propia).

1. **Qué falló:** pregunta en una sola ronda qué no convence y tradúcelo a criterios: un KPI nuevo o
   más estricto, un peso distinto en la rúbrica, un rasgo nuevo en `anti-cliches.md`, una referencia
   nueva en `creative-direction.md`. Un "no me gusta" sin traducir no cambia el resultado. Las
   respuestas van a "Decisiones" de `brief.md` (tipo `diseño`, fuente `usuario`).
2. **Archiva** `candidatos/` en `docs/design/candidatos/history/ronda-<N>/` (y un `system.md` en
   `draft` de la ronda anterior, dejando `design.status: none` y `source: null`). Nunca borres una
   ronda.
3. **Repite el ciclo** (§2.4) con los criterios nuevos; el primer candidato parte del mejor de la
   ronda anterior.

En un rediseño (spec propia) se aplica lo mismo desde `/design-spec NNN` (`spec-mode.md` §5).

### 2.8 Ajustar un solo eje del aceptado

`/design-spec system --redo-options --only <eje> --base <cN>`, para cuando el aceptado convence
salvo un aspecto ("la letra no"). Ejes: `tipografia`, `color`, `forma`, `fondo`, `movimiento`; la
composición no es un eje (§2.7). Sin sistema `approved`.

1. **Congela el resto:** solo cambian los tokens del eje (`--font-*` y `--text-*`; `--color-*`;
   `--radius-*`, `--border-*`, `--shadow-*` y `--space-*`; `--surface-*`; `--duration-*` y
   `--ease-*`).
2. **El criterio primero:** escribe qué tiene que lograr el eje (p. ej. "cifras tabulares legibles a
   14 px en exterior") como KPI o como nota mínima de un punto de la rúbrica.
3. **2–3 variantes** como candidatos `c<N>-<eje>-<v>`, medidos con `evaluate.mjs` y comparados en
   una lámina desde `../../init/templates/design/eje.html` (fuentes cargadas, contraste, "Simular luz
   exterior"). Se acepta la variante que pasa puertas y KPIs, cumple el criterio del eje y no baja
   la puntuación del aceptado; con varias, la de mayor puntuación.
4. La variante aceptada se aplica a la base y va a "Decisiones" con el criterio que la decidió; la
   lámina se archiva en `history/ronda-<N>-<eje>/`.

## 3. Brownfield: documentar el diseño existente

**Pregunta en la Fase 0**, al detectar interfaz y antes de explorar: *"¿Documento el diseño que
usa hoy el código? Extraigo colores, tipografía y componentes, audito contraste y valores fijos, y
dejo `docs/design/system.md` y una vista en HTML. No cambio código."* Con un **no**:
`design.status: declined`, no lances el subagente G y no vuelvas a preguntar (tampoco
`--upgrade`).

Con un **sí**, la regla es **fidelidad**: el documento describe la app que ve el usuario, no una
interpretación. Nada se dibuja a mano ni se redacta: lo que no se puede capturar o leer del código
queda marcado como pendiente.

1. **Subagente G** (`../../init/references/explore-agents.md`) en la Fase 1, junto a los demás: tokens, valores fijos,
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
   `../../init/references/brownfield.md` §4; el usuario decide.
9. Constitución: el principio "solo tokens" se propone con la regla de "Código previo": aplica a
   pantallas nuevas o modificadas; el código anterior no bloquea.
10. **Marca en el navegador y al compartir:** documenta los íconos enlazados en el `<head>` y las
   imágenes Open Graph que ya existen (archivo, tamaño, de dónde salen, si son estáticas o
   generadas), incrustados en `system.html#compartir`. Lo que falta o es genérico (favicon de la
   plantilla del framework, imagen para compartir ausente o la misma captura en todas las rutas de
   un sitio indexable) es deuda `DS`. No diseñes una tarjeta nueva: eso es una spec.

No propongas rediseño ni generes candidatos. Si el usuario lo pide, el resumen indica que es una
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

`../../init/references/upgrade.md` paso 9 ejecuta **solo** el §3 (pregunta incluida) sobre un proyecto ya inicializado, sin
re-explorar el resto del código: lanza únicamente el subagente G. Con un sistema extraído por un
procedimiento anterior, ofrece §3b (re-extraer); `--redo-design` lo ejecuta directamente.
`--redo-options` sigue §2.7 (repetir el ciclo de un proyecto nuevo antes de aprobar el sistema);
con `--only <eje> --base <opción>`, §2.8 (afinar un solo eje de una opción). Los tres argumentos son
atajos de `/design-spec system` con el mismo nombre.

## 5. Brief (para la skill `design` y para escribir el HTML)

```
Proyecto: <nombre> — <descripción de AGENTS.md> (<tipo>, <stack de UI>)
Modo: sistema | spec NNN-slug
Objetivo: <de brief.md o de la spec>
Dirección creativa: <resumen de docs/design/creative-direction.md, con sus referencias con nombre>
Concepto firma: <el de creative-direction.md, o "ninguno: cada opción propone el suyo">
Clichés del sector: <los de anti-cliches.md, con su alternativa>
Nicho: <convenciones, materiales y territorio elegido de docs/design/nicho.md>
Movimiento y superficies: <los de creative-direction.md>
Modo de la pantalla principal: <persuadir · operar · leer>
Criterios: <puertas, KPIs con objetivo y pesos de la rúbrica de docs/design/criterios.json>
Recursos de marca disponibles: <logo, fotos, íconos que existen; ninguno se inventa>
Sistema de diseño: <tokens clave de system.md, o "a definir" en modo sistema>
Contenido real: <textos y datos exactos; nunca lorem ipsum>
Artboards:
  - Un candidato completo que cumpla los criterios (el ciclo genera el siguiente si no los cumple)
  - Cada una a <design.widths>
  - Estados: vacío, carga, error, foco, deshabilitado
  - Movimiento como fotogramas anotados (inicio → medio → final), con versión sin movimiento;
    solo el movimiento que piden el brief y movimiento.md
  - Superficies y fondos de cada opción, con el texto sobre la zona más difícil del fondo
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
- la misma animación de entrada, con el mismo tiempo, en cada sección;
- un esqueleto de página de plantilla (hero centrado, fila de tarjetas iguales, pie con columnas de
  enlaces) con solo el color, el radio y la sombra cambiados.

- fondos de moda sin relación con la idea: manchas de color difusas, degradados de malla, vidrio
  esmerilado, grano o ruido en toda la página, rejilla de puntos;
- movimiento genérico (`movimiento.md` §4): parallax o contadores sin datos reales, cursores
  personalizados, pantalla de carga, scroll secuestrado, texto que se escribe solo.

- tarjeta para compartir que no se parece al sitio: el logo centrado sobre un degradado, marca +
  título + descripción en columna sobre fondo liso (la base de la plantilla), o una captura de la
  página reducida hasta que nada se lee; un ícono que es un cuadrado redondeado con iniciales en la
  fuente del sistema.

Cada uno de estos rasgos baja la nota del punto `plantilla` de la rúbrica (`criterios.md` §5): el
evaluador los busca en las capturas.
