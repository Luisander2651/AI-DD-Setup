# Movimiento: capa completa, escenas y fichas `M-n`

Lo leen `/design-spec` (modo `system` §2.4 paso 8 y modo `NNN` `spec-mode.md` §4), `/implement`
y `/review`. Una página que no se mueve se lee como maqueta; una en la que todo se mueve igual dice
que nadie decidió nada. La meta es **movimiento coreografiado con un momento protegido**.

## 1. El filtro (antes de cada animación)

| Pregunta | Respuesta que la deja pasar |
|---|---|
| **Frecuencia:** ¿cuántas veces la ve una persona? | Una vez por visita (carga, entrada de sección): puede tomarse su tiempo. Varias por visita (hover, menú, acordeón): rápida y pequeña. Cientos al día (atajos de teclado, paleta de comandos, escribir, navegación principal de una app): **ninguna animación** |
| **Propósito:** ¿para qué? | Muestra de dónde viene algo · confirma una acción · evita un cambio brusco · explica cómo funciona el producto · es la jugada firma o una escena. "Se ve bonito" solo vale para la jugada firma |
| **Velocidad:** ¿cabe en el presupuesto? | Tabla de §3. Si solo "funciona" lenta y vistosa, no pasa |
| **Función:** ¿ayuda o estorba? | Datos que la persona lee o sobre los que actúa no se mueven por estilo |

Registra en la ficha `M-n` (§8) la respuesta a cada pregunta. En una revisión de animaciones, lista
también 2–5 candidatas **rechazadas** con la pregunta que las descartó.

## 2. La capa según el modo de la pantalla

**Persuadir / Experiencia** — cinco partes; el inspector (`inspeccion.md`) cuenta lo que se mueve:
1. **Escenas de scroll** (§4): 1–3 por página según el registro (`creatividad.md` §4), donde la
   página es audaz; todo lo demás queda tranquilo para que se noten.
2. **Una jugada firma** (§5): lo que alguien describiría una hora después. Una, bien hecha; puede
   ser una escena.
3. **Entradas coreografiadas por sección:** las partes llegan en orden de lectura (titular, texto,
   imagen, detalles), escalonadas 60–90 ms, subiendo 12–32 px con opacidad o desde una máscara de
   línea, **una sola vez**. La manera **cambia con el contenido**: una lista llega fila a fila, una
   imagen se abre desde una máscara o se asienta desde una escala leve, una cifra sube una vez, una
   frase sube línea a línea. Nunca el mismo fundido con el mismo tiempo en cada bloque.
4. **Respuesta bajo la mano:** botones que ceden al pulsar, enlaces que responden al puntero,
   tarjetas e imágenes con hover, un menú que se abre desde donde se pulsó.
5. **Una imagen en movimiento:** un clip real en bucle silenciado con su fotograma de póster, una
   deriva o escala lenta sobre una fotografía grande, o un movimiento ligado al scroll en la imagen
   del hero.

**Operar / Leer** — la audacia está en la sensación, no en el espectáculo:
- **Respuesta** en cada control (pulsar 100–160 ms, `scale(0.97)`), con su versión táctil.
- **Continuidad espacial:** lo que aparece crece desde su disparador (`transform-origin` en el
  botón; los diálogos modales se quedan centrados); lo que se descarta sale por donde entró; una
  fila que se abre en detalle viaja hasta él (View Transitions).
- **Estados legibles:** acordeones, filas que se añaden o quitan, datos que cambian de estado se
  transforman en lugar de saltar.
- **Deleite** solo en momentos raros y con carga emocional: primer uso, estado vacío, éxito,
  recuperación de un error. Proporcional al esfuerzo (un hito puede expandirse; un guardado
  rutinario solo debe sentirse seguro). Nunca retrasa ni bloquea la tarea, nunca finge trabajo.
- **Cero animación** en lo de alta frecuencia (filtro de §1).

## 3. Tokens de movimiento

Curvas (las palabras clave de CSS son débiles; usa tokens):

| Token | Valor | Uso |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | Todo lo que entra o sale por debajo de 600 ms |
| `--ease-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | Revelados de 800 ms o más |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | Barridos y cosas que viajan de un sitio a otro |
| `--ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | Solo lo que se va para siempre, corto |
| `linear` | — | Movimiento ligado al scroll y bucles |
| `ease` | — | Cambios de color y opacidad en hover |

Sin rebote ni elástico en elementos de interfaz; los resortes solo en gestos (arrastrar, soltar)
con rebote 0.1–0.3. `ease-in` para entrar hace que la interfaz se sienta lenta: no se usa.

| Elemento | Duración |
|---|---|
| Pulsar | 100–160 ms |
| Hover de color | 150–200 ms · hover que mueve 300–400 ms |
| Tooltips y popovers | 125–200 ms · menús 150–250 ms |
| Diálogos y cajones | 200–450 ms |
| Revelados de sección y de hero | 600–900 ms |
| Aperturas de imagen y barridos | 1 100–1 300 ms |
| Salida | 60–70 % de su entrada |

Escalonados: líneas 80–110 ms · elementos de lista 50–90 ms · caracteres 20–40 ms, solo en un
titular de una a tres palabras · cuatro pasos como máximo en una secuencia. Revelados: se disparan
una vez cuando la parte superior del elemento llega al 85–90 % del alto de la ventana; nada visible
espera más de 900 ms; nada por encima del primer pantallazo espera al scroll. La carga termina en
1,2 s con cuatro elementos como máximo y empieza sin esperar al evento `load`.

## 4. Escenas de scroll

Tramos donde la página deja de ser una columna de secciones y se convierte en escena: una cámara
que atraviesa un campo de imágenes, una imagen que pasa de ventana a pantalla completa, una palabra
que la página empuja, fotografías que orbitan y aterrizan en una rejilla. No es un fundido, un
parallax pequeño ni una marquesina: eso es la capa tranquila. Una escena cambia la pantalla entera.

**Estructura.** Una sección alta (`(hold + 1) × 100svh`) con un **escenario `position: sticky`**
que se queda quieto `hold` pantallas mientras la página pasa; el progreso 0→1 sale de la posición
del scroll. Técnica, en orden: CSS `animation-timeline: view()` / `scroll()` dentro de
`@supports` → un único script común del proyecto que calcula el progreso de todas las escenas en un
`requestAnimationFrame` → una librería (GSAP ScrollTrigger, Motion) con ADR y la verificación de
`../../../shared/agent-security.md` §2. Suavizado del scroll (Lenis o similar) solo con ADR, nunca
en táctil ni con movimiento reducido.

**Reglas:**
1. **1–3 por página** según el registro, de familias distintas, con **una sección tranquila entre
   dos escenas**; nunca más de ~60 % de la página en escenas.
2. Cada una retiene **1–4 pantallas**, una por paso de la historia; un tramo sin nada nuevo se
   corta, no se rellena.
3. **Scroll nativo:** nada captura la rueda, nada bloquea la página, la barra dice la verdad, el
   teclado y el trackpad funcionan, la escena termina.
4. **Legible en sus puntos de reposo:** la frase en pantalla se lee entera; nada pasa por encima de
   un texto mientras se lee; texto sobre imagen con una zona tranquila o un velo plano debajo.
5. **La escena dice algo del sujeto:** la ruta que de verdad hace el envío, las cuatro salas de la
   casa, el cambio de estado del producto. Imágenes de una misma familia (misma luz, mismo
   tratamiento). Si necesita ocho imágenes y hay tres, cambia de escena; nunca la rellenes.
6. **`transform`, `opacity` y `clip-path`**; imágenes decodificadas antes de moverse.
7. **La composición terminada está diseñada:** es lo que ven el movimiento reducido, un script que
   falla y algunos teléfonos. Escríbela primero en CSS; la versión viva va bajo una clase que pone
   el script (`.is-live`). Cada escena tiene un **plan de teléfono**: la misma con otros números,
   una más simple o la composición terminada.
8. Una escena en la primera pantalla se lee en el progreso 0: titular, frase y acción están en el
   primer fotograma; solo se mueve cuando la persona hace scroll.
9. La sección lleva encabezado (visible o `aria-label` más un encabezado real en la composición).

## 5. Catálogo de jugadas firma y escenas

Los IDs son los que reparte `aidd.py deal` (`creatividad.md` §4). Elige por sujeto: si la jugada
no dice nada del sujeto, es decoración.

**Escenas** (Persuadir / Experiencia):

| ID | Qué pasa | Le conviene a | Técnica |
|---|---|---|---|
| `ventana` | Una ventana en el centro de un escenario retenido se abre hasta la imagen a sangre en ~1 pantalla | Un producto o un lugar con una gran fotografía | `clip-path: inset()` por progreso |
| `historia-fijada` | Un titular se queda mientras sus elementos pasan por delante | Un proceso, un método, capítulos | `position: sticky` sin script |
| `galeria-lateral` | Una fila corta de imágenes se desplaza de lado mientras el scroll vertical retiene el escenario | Pocas salas, platos, piezas | `translateX` por progreso |
| `hoja-sobre-imagen` | Una fotografía a sangre se queda una pantalla y el capítulo siguiente sube encima como hoja opaca | Capítulos que tienen cada uno su imagen | Figura `sticky` 100svh y sección con fondo y `z-index` mayor, sin script |
| `vuelo` | La cámara atraviesa un campo de imágenes o títulos del propio trabajo | Un estudio, un archivo, un portafolio con mucha obra | `translateZ`/`scale` por progreso, perspectiva |
| `reparto` | Tarjetas reales se reparten y se apilan o aterrizan en una rejilla | Una colección, un menú, un catálogo corto | `transform` por progreso |
| `palabra-empujada` | Una línea de tipo enorme se desplaza de lado con el scroll y se lee entera a mitad de su recorrido | Una marca cuyo argumento es una palabra | `animation-timeline: view()`, `translateX` 12 % → −12 % |
| `cambio-de-estado` | El objeto del producto pasa por sus estados (crudo → hecho, borrador → publicado) | Un producto que transforma algo | Capas apiladas con `opacity`/`clip-path` |

**Jugadas firma** (Persuadir / Experiencia):

| ID | Qué pasa | Le conviene a | Técnica |
|---|---|---|---|
| `titular-enmascarado` | Las líneas del titular suben desde detrás de su línea base al cargar | Un nombre o un argumento corto | Máscara por línea, `translateY` |
| `persiana` | La imagen del hero se abre desde un borde y se asienta desde escala 1.12 | Un producto con su objeto | `clip-path` + `scale` |
| `marca-que-escala` | Una marca gigante crece o se encoge unos puntos mientras el hero sale | Una marca con nombre corto y fuerte | `scale` ligado al scroll |
| `indice-con-vista` | Filas de texto; la fila con el puntero muestra su imagen anclada a la fila | Un portafolio, una lista de obras o proyectos | Imagen por fila, `opacity`/`clip-path`; en táctil la imagen va en la fila |
| `fundido-lento` | El hero cruza 3–4 fotografías, 5–6 s cada una | Un restaurante, un hotel, un lugar | Imágenes apiladas, keyframes de opacidad, pausa con la pestaña oculta |
| `marquesina` | Una línea de tipo muy grande viaja de lado, despacio | Un evento, una agenda, un manifiesto | Contenido duplicado, `translateX(-50%)` lineal, pausa al pasar y con movimiento reducido |
| `tinta` | Una frase se llena de 45 % a tinta completa mientras sube por la pantalla | Un manifiesto, una declaración | `animation-timeline: view()` sobre el color o una máscara |
| `cifras-que-ruedan` | Las pocas cifras **reales** que sostienen el argumento ruedan hasta su valor, una vez | Un informe, un fondo, una práctica que se apoya en números | Contador con `tabular-nums`; el valor final está en el HTML |
| `telon-final` | La última sección aparece desde debajo de la página al llegar al final | Un cierre con el nombre a todo el ancho | Pie `position: sticky; bottom: 0` bajo un `main` con fondo |
| `imagen-que-viaja` | La imagen pulsada en una lista viaja hasta ser el hero de la página siguiente | Un portafolio o catálogo con índice y fichas | View Transitions (`view-transition-name`) |
| `color-por-capitulo` | Cada capítulo es su propio campo de color a sangre; la barra fija toma la tinta del capítulo de debajo | Una historia con partes claras | Fondos por sección; nunca recolorear la página entera desde un observador |
| `fila-arrastrable` | Una fila horizontal de imágenes grandes con imán | Galerías, productos, habitaciones | `overflow-x: auto; scroll-snap-type: x mandatory`, sin librería |

**Ambición de sensación** (Operar / Leer):

| ID | Qué pasa | Técnica |
|---|---|---|
| `nace-del-disparador` | El menú, el popover o el panel crece desde el botón que lo abrió | `transform-origin` en el disparador; `@starting-style` para entrar sin JS |
| `fila-a-detalle` | La fila pulsada se transforma en la vista de detalle | View Transitions entre estados |
| `guardado-optimista` | El cambio se ve aplicado al instante; si falla, vuelve con el aviso | Estado local + reversión, sin spinner para lo que tarda menos de ~300 ms |
| `arrastre-con-resortes` | Arrastrar y soltar con física, descarte por velocidad, resistencia en los bordes | Resorte (duración 0.5, rebote 0.2); descarte si `distancia/ms > ~0.11` |
| `lista-que-reordena` | Las filas que se añaden, quitan u ordenan se desplazan a su sitio | FLIP o View Transitions; transiciones (no keyframes) para que se reorienten |
| `datos-que-transicionan` | Un gráfico pasa de un estado a otro en lugar de redibujarse | Interpolar valores; nunca animar decoración sobre datos que se leen |
| `mantener-para-confirmar` | Una acción destructiva se confirma manteniendo pulsado con un relleno | `clip-path` 2 s lineal al pulsar, 200 ms de vuelta al soltar |
| `vacio-que-orienta` | El estado vacío o el primer uso muestra la siguiente acción con carácter del producto | Una sola entrada; ilustración o texto del mundo del producto |
| `exito-proporcional` | El éxito responde en proporción al esfuerzo: un hito se expande, un guardado solo asiente | Una entrada corta; nada que retrase |

## 6. Ambición técnica

Para cuando la opción es `audaz` o el usuario pide más: hacer que la interfaz haga algo que la
persona no creía que una web podía hacer. Siempre **mejora progresiva**: sin la mejora, la
experiencia sigue siendo buena.
- Transiciones de cine: View Transitions (un elemento compartido que se transforma entre estados),
  `@starting-style` para animar desde `display: none`, resortes en gestos.
- Ligado al scroll sin JS: `animation-timeline: scroll()` / `view()` dentro de `@supports`, con
  versión estática.
- Más allá de CSS (solo Persuadir/Experiencia, con ADR): WebGL o Canvas para lo que CSS no expresa,
  inicializado solo cerca de la ventana, pausado fuera de ella, con respaldo estático.
- Datos que se sienten vivos (Operar): listas virtuales para decenas de miles de filas, búsqueda que
  filtra sin parpadeo, trabajo pesado en un Worker.
- Nunca varios momentos extraordinarios compitiendo: el foco crea impacto, el exceso crea ruido.
- Prueba de retirada (quitarla se nota) y prueba de dispositivo (fluido en un teléfono de gama media,
  60 fps; por debajo de 50, simplifica).

## 7. Lo que no se usa

Delatan movimiento generado o cuestan usabilidad. Prohibido salvo petición explícita del brief, que
se registra:
- el mismo fundido y subida, con el mismo tiempo, en cada bloque; una docena de entradas
  escalonadas en el hero; hover que levanta o amplía **todas** las tarjetas;
- **pantalla de carga, contador de carga o puerta** (entrar, sonido, edad) antes del contenido;
- **secuestro del scroll** (la rueda mueve otra cosa, pantallas donde la rueda no hace nada) y
  **cursores propios**;
- texto que se escribe solo o se desordena; contenido retenido invisible más de 900 ms; elementos
  inactivos atenuados por debajo del 40 %; movimiento que cruza un texto que se está leyendo;
- rebote y elástico en interfaz; bucles sin sentido (puntos que laten, formas flotantes, insignias
  que giran) y cualquier bucle que no se pause fuera de pantalla, con la pestaña oculta y con
  movimiento reducido;
- sonido sin que la persona lo active (un control en la página, apagado por defecto);
- un revelado que nunca se dispara y deja una franja en blanco (lo encuentra `inspeccion.md`).

## 8. Ficha `M-n`

Cada animación de la pantalla es una ficha en `design.md` → "Movimiento":
- **tipo:** `escena` · `firma` · `entrada` · `respuesta` · `imagen en movimiento` · `deleite` ·
  `sensación` (Operar), y el ID del catálogo si sale de él;
- **filtro:** frecuencia y propósito (§1);
- disparador (carga, entrada en pantalla, progreso de scroll, puntero fino, foco, toque) y si ocurre
  **una sola vez** o se repite;
- elementos y propiedades (`transform`, `opacity`, `clip-path`; `filter` solo con justificación);
- duración y curva con tokens (§3); estado inicial → final; secuencia o escalonado; en una escena,
  `hold` y qué muestra cada paso;
- técnica, en el orden de §4 (o CSS → transiciones entre vistas del framework → Web Animations API →
  librería con ADR, fuera de escenas);
- versión **reducida** (`prefers-reduced-motion: reduce` = menos y más suave, no nada: se conservan
  opacidad y color, se quitan desplazamiento, escala, parallax y reproducción automática), **sin
  JavaScript** (contenido completo y visible; en escenas, la composición terminada), **táctil**
  (`hover: none`: qué se ve, o nada si el elemento no es interactivo) y **plan de teléfono** en
  escenas;
- **coste** en JavaScript contra el presupuesto de la constitución, y qué propiedades comparte con
  otras animaciones del mismo elemento (dos animaciones no animan la misma propiedad);
- fotogramas en el HTML de la composición (`#movimiento`) y, en escenas, la tira de `inspeccion.md`.

## 9. Rendimiento

Salvo prueba en contra registrada:
- sin `filter` animado sobre superficies grandes ni `backdrop-filter` en elementos fijos;
- el movimiento ligado al scroll vive **solo** en escenas o en `animation-timeline`; fuera de ellas,
  revelados disparados una vez al entrar en pantalla;
- ningún trabajo por fotograma salvo el cálculo de progreso del script común (uno por proyecto, no
  uno por sección); nada de leer el layout dentro de ese bucle;
- no muevas muchos hijos desde una variable CSS del padre: pon el `transform` en el elemento que se
  mueve; `will-change` solo justo antes de animar y se quita después;
- se animan `transform`, `opacity` y `clip-path`; `width`, `height`, `top`, `left`, `margin` o
  `padding` fuerzan layout en cada fotograma (`grid-template-rows` en acordeones es la excepción
  aceptada).

**Racionar el efecto firma:** respeta las "Reglas de uso" de `system.md` (cuántas escenas y momentos
protagonistas por página, dónde se permite la jugada firma, cuántos por pantalla en reposo). Una
composición que las rompe lo dice como riesgo y la regla se cambia en el sistema, no en silencio.
