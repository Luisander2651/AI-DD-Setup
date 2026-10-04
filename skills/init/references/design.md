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
- `docs/design/creative-direction.md`.
- `docs/design/anti-cliches.md`: conserva las filas de "todos los tipos" y las del tipo del
  proyecto, borra las demás, añade los clichés que el usuario rechazó en "Referencias".

Muéstralos y pide aprobación antes de generar nada: las opciones cuestan tokens.

### 2.3 Número de opciones
**3 por defecto. 2 si el usuario ya trae marca y paleta cerradas** (las opciones cambian
tipografía, forma, densidad y composición, no el color). Regístralo en `brief.md` (`options:`).

### 2.4 Generar las opciones
Por cada opción, `docs/design/opciones/opcion-<a|b|c>.html` desde `option.html`:

1. Tokens completos en el bloque de estilos `tokens` (si hay modo oscuro, **todos** los colores
   redefinidos). Para rellenar los bloques, busca la etiqueta **después** del comentario de
   instrucciones de la plantilla (el comentario los nombra).
2. Componentes ajustados a la dirección en el bloque `components`, solo con tokens.
3. Tipografía real: si la fuente no es del sistema, incrusta en el bloque `fonts` cada peso que
   uses como `@font-face` con el subconjunto latino en woff2 y base64, tomado del mismo paquete o
   archivo que usará la app (p. ej. `@fontsource/<familia>/files/<familia>-latin-400-normal.woff2`);
   sin él, el usuario elegiría sobre la fuente de reemplazo. Comprueba que carga
   (`[...document.fonts].some(f => f.family === '<familia>' && f.status === 'loaded')`;
   `document.fonts.check()` da `true` aunque la fuente no exista).
4. Pares de contraste: deja en "Color" solo los pares cuyos tokens existen en la opción (marca los
   demás con `data-optional`, que la página oculta si falta un token).
5. Contenido **real**: nombre del producto y textos de la primera feature del roadmap, datos de
   prueba realistas; nunca lorem ipsum ni cifras inventadas.
6. Pantallas: 1–2 principales en cada ancho de `design.widths`.
7. "Por qué" en una o dos frases ligadas al brief, y el riesgo asumido.

Las opciones deben ser **distintas de verdad**: cambian al menos dos de familia de color,
pareja tipográfica, forma y densidad, y composición de la pantalla principal. No tres tonos de lo
mismo. Evita los clichés de `anti-cliches.md` y, salvo que el brief lo pida, los rasgos por
defecto de las interfaces generadas (§6).

**Antes de enseñarlas:**
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

## 3. Brownfield: documentar el diseño existente

**Pregunta en la Fase 0**, al detectar interfaz y antes de explorar: *"¿Documento el diseño que
usa hoy el código? Extraigo colores, tipografía y componentes, audito contraste y valores fijos, y
dejo `docs/design/system.md` y una vista en HTML. No cambio código."* Con un **no**:
`design.status: declined`, no lances el subagente G y no vuelvas a preguntar (tampoco
`--upgrade`).

Con un **sí**:
1. **Subagente G** (`explore-agents.md`) en la Fase 1, junto a los demás.
2. **Capturas y medidas** de las pantallas principales (lista, vacío, error, formulario con error)
   en `design.widths`, solo si la app arranca con los comandos verificados y **solo con datos de
   prueba**, nunca con datos reales. Para inyectarlos, en este orden: helpers o fixtures de los
   tests de pantalla del proyecto (p. ej. un almacén simulado), un comando de semilla documentado,
   o pregunta; si no hay forma sin datos reales, no captures y dilo. Van a
   `docs/design/capturas/`. En cada pantalla **mide** los estilos calculados en el navegador
   (`getComputedStyle`): fondo y texto de pantalla, barra y filas, familia de fuente, margen lateral
   del contenido y de los campos, alto de botones y campos; con `prefers-color-scheme: dark`
   emulado, si el código declara modo oscuro. `system.md` documenta **lo medido**: si difiere de lo
   que declara el código (G), lo medido manda y la diferencia es deuda `DS`.
3. **Auditoría:** con el plugin, `design:design-system audit` sobre el informe de G y
   `design:accessibility-review` sobre las capturas; sin él, la misma revisión con el checklist de
   `system.md` (contraste, valores fijos, estados, toque mínimo).
4. `system.md` con `source: extracted`, `status: draft`: el sistema **tal como está**, sin
   mejoras. Lo no determinado se marca y se pregunta. La deuda va a "Deuda de diseño" con IDs
   (`DS1`, `DS2`…) y evidencia.
5. `system.html` desde `option.html` con los valores reales: los pares que no cumplen se ven en
   rojo (es deuda, no se corrige aquí). En "Pantallas", las capturas como `<img
   src="capturas/<pantalla>-<ancho>.png" alt="…">` dentro de cada marco. En "Componentes", recortes
   de las capturas (botón, campo, fila, aviso) en lugar de los componentes sintéticos de la
   plantilla: los sintéticos no reproducen los detalles de la librería (mayúsculas de Material,
   superficies internas) y harían creer que el sistema es otro.
6. **Roadmap:** las `DS` prioritarias se proponen como objetivos con la conciliación de
   `brownfield.md` §4; el usuario decide.
7. Constitución: el principio "solo tokens" se propone con la regla de "Código previo": aplica a
   pantallas nuevas o modificadas; el código anterior no bloquea.

No propongas rediseño ni generes opciones. Si el usuario lo pide, el resumen indica que es una
spec propia (`/specify "rediseño de …"`).

## 4. `/init --upgrade`

`upgrade.md` paso 9 ejecuta **solo** el §3 (pregunta incluida) sobre un proyecto ya inicializado, sin
re-explorar el resto del código: lanza únicamente el subagente G.

## 5. Brief (para la skill `design` y para escribir el HTML)

```
Proyecto: <nombre> — <descripción de AGENTS.md> (<tipo>, <stack de UI>)
Modo: sistema | spec NNN-slug
Objetivo: <de brief.md o de la spec>
Dirección creativa: <resumen de docs/design/creative-direction.md>
Sistema de diseño: <tokens clave de system.md, o "a definir" en modo sistema>
Contenido real: <textos y datos exactos; nunca lorem ipsum>
Artboards:
  - Opciones A, B (y C), claramente distintas entre sí
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
  como decoración;
- etiquetas en mayúsculas espaciadas sobre cada título, metadatos unidos con puntos medios,
  monoespaciada para cualquier dato pequeño, flechas añadidas a todos los botones;
- numeración decorativa (01, 02, 03) en contenido que no es una secuencia;
- animaciones de entrada en cada sección en lugar de un único momento con sentido.

Gasta la audacia en un solo elemento reconocible y mantén el resto sobrio.
