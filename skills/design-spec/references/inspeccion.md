# Inspección: mirar lo que hiciste antes de enseñarlo

Pasa el diseño por el inspector antes de enseñar cualquier opción o composición
(`system-mode.md` §2.4 y `spec-mode.md` §2); también lo usa `/review` para el movimiento. Pasar el
inspector solo significa que no se midió nada prohibido; **no** significa que la página sea buena:
para eso está la crítica (§3).

## 1. Qué se inspecciona

- **Opciones y composiciones** (`opcion-<x>.html`, la página de visor): capturas en claro, oscuro y
  "Sin movimiento", y que no pida nada a la red.
- **Página de prueba** (`opcion-<x>-pagina.html`), obligatoria en pantallas de **Persuadir o
  Experiencia** (`creatividad.md` §1): la pantalla principal como **página real a ancho de
  ventana**, con los mismos bloques `fonts`, `tokens` y `components` que su opción, su contenido
  completo, sus escenas, sus entradas y su cosa viva funcionando. Autocontenida, sin red (un script
  propio, nunca un CDN). `opcion-<x>.html` la enlaza en la sección "Movimiento". Es donde se ven el
  ritmo del scroll y las escenas: el visor escala los marcos y no se recorre como una página.
- En `/review`, la build de producción servida en local (nunca el servidor de desarrollo).

## 2. El inspector

```
node <skill>/scripts/inspect.mjs <archivo.html | URL> --mode <persuadir|experiencia|operar|leer> \
  [--widths <design.widths con el intermedio>] [--out .ai/inspect/<nombre>]
```

`<skill>` es la carpeta de esta skill. Usa Playwright si ya está (en el proyecto, global o en
`PLAYWRIGHT_PATH`; `CHROMIUM_PATH` para un Chromium propio) y no instala nada; si no lo encuentra
(código 3), captura con la herramienta de navegador de la sesión a los mismos anchos y dilo en la
crítica. `.ai/inspect/` va en `.gitignore` (añádelo si falta): las capturas no se versionan.

Deja en `--out` capturas por ancho (claro, oscuro, movimiento reducido, sin JavaScript), una **tira
del scroll** (`film-<ancho>-NN.png`, un fotograma cada ~⅓ de pantalla, al menor y al mayor ancho),
`report.md` y `report.json`. Mide:

| Código | Nivel | Qué |
|---|---|---|
| `desborde-horizontal` | FAIL | La página es más ancha que la ventana |
| `contenido-que-no-aparece` | FAIL | Tras recorrer la página y esperar, un texto o imagen sigue invisible (un revelado que no se dispara) |
| `oculto-con-movimiento-reducido` · `oculto-sin-javascript` | FAIL | Contenido escondido esperando un script |
| `error-js` | FAIL | Error de JavaScript en la página |
| `peticiones-externas` | FAIL en opciones · WARN en páginas | Algo se pide a la red |
| `pagina-quieta` · `poco-movimiento` | FAIL < 8 · WARN < 16 | Elementos que se mueven al cargar y recorrer (solo `persuadir`/`experiencia`); es un suelo, no una meta |
| `tramo-vacio` | WARN | Fotogramas de la tira sin contenido visible (más de un descanso deliberado es un fallo de plenitud) |
| `muchas-escenas` | WARN | Más de 3 escenas |
| `titular-largo` · `h1` | WARN | Titulares de más de dos líneas; un `h1` por página |
| `fuente-no-cargada` · `consola` | WARN | La fuente de marca no cargó; errores en consola |

Corrige todo FAIL. Trata cada WARN como un error salvo que puedas defenderlo ante un diseñador en
una frase, escrita en la crítica. No discutas con el medidor ni le escondas cosas.

## 3. Crítica (mirar las capturas)

Abre **todas** las capturas y la tira del último pase (con la herramienta Read o un visor), no solo
la primera pantalla. Juzga solo lo que se ve: si un problema aparece en una captura, es real, diga
lo que diga el código. Escribe la crítica en `docs/specs/NNN-<slug>/design/critica-<x>.md` (o
`docs/design/opciones/critica-<x>.md` en modo sistema) con esta forma:

```
# Crítica · opción <x> · ronda <n>
Inspector: <n> FAIL · <n> WARN (avisos defendidos: …)
| Pase | Nota 0–10 | Qué se ve (captura) |
|---|---|---|
| Idea: se reconoce el sujeto en la primera pantalla; pasa la prueba del competidor | | |
| Cinco segundos: qué es y qué hacer, sin leer el resto | | |
| Jerarquía y escala: una cosa dominante por pantalla; titular ≥ ~4× el cuerpo | | |
| Plenitud: contenido completo; sin tramos vacíos ni secciones delgadas | | |
| Composición: ninguna sección vecina repite esqueleto; la idea llega al pie | | |
| Color: la estrategia declarada se ve a escala de página | | |
| Imágenes: reales o dibujadas desde el sujeto, grandes, de una familia | | |
| Movimiento: la jugada firma y las escenas se leen en la tira; entradas variadas, no un solo fundido | | |
| Cosa viva: se entiende y se usa con el pulgar al ancho menor | | |
| Teléfono: el ancho menor es su propia composición, no la de escritorio apretada | | |
| Reducido y sin JS: la composición terminada está diseñada y completa | | |
| Accesibilidad: contraste, foco visible, orden de lectura | | |
Tres problemas que más mueven la página: 1. … 2. … 3. …
```

Arregla los tres primeros, vuelve a pasar el inspector y vuelve a mirar. **Tres rondas como
máximo**; lo que quede va a "Riesgo asumido" de la opción. Una nota por debajo de 6 en Idea,
Plenitud o Movimiento (en Persuadir) no se enseña: rehaz la composición.

## 4. Sin navegador

Si no hay Playwright ni herramienta de navegador, pide al usuario que abra la página de prueba a
los anchos de `design.widths`, con "Sin movimiento" y en oscuro, y que te pase las capturas. Nunca
digas que se inspeccionó algo que no se inspeccionó: en la crítica, `inspector: no ejecutado
(<motivo>)`.
