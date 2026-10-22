# Movimiento: reglas y fichas `M-n`

Lo leen `/design-spec`, `/implement` y `/review`. El movimiento es una restricción, no un adorno que
sume puntos: una animación existe solo si cumple un propósito del filtro (§1) y no rompe ninguna
puerta (`criterios.md` §2: todo visible con movimiento reducido y sin JavaScript, nada que no
aparezca).

## 1. Filtro (antes de cada animación)

| Pregunta | Respuesta que la deja pasar |
|---|---|
| **Frecuencia** | Una vez por visita (carga, entrada de sección): puede tomarse su tiempo. Varias por visita (hover, menú, acordeón): rápida y pequeña. Cientos al día (atajos, navegación principal de una app, escribir): **ninguna** |
| **Propósito** | Muestra de dónde viene algo · confirma una acción · evita un cambio brusco · explica cómo funciona el producto. "Se ve bonito" no pasa |
| **Velocidad** | Cabe en la tabla de §2 |
| **Función** | No mueve datos que la persona lee o sobre los que actúa |

## 2. Tokens

| Token | Valor | Uso |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | Entrar y salir por debajo de 600 ms |
| `--ease-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | Revelados de 800 ms o más |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | Cosas que viajan de un sitio a otro |
| `--ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | Lo que se va para siempre, corto |

Duraciones: pulsar 100–160 ms · hover 150–200 ms · menús 150–250 ms · diálogos 200–450 ms ·
revelados 600–900 ms · salida 60–70 % de su entrada. Escalonados: 50–110 ms, cuatro pasos como
máximo. Sin rebote ni elástico en interfaz; resortes solo en gestos de arrastre.
Momento firma al cargar (uno por página, si la dirección lo pide): una secuencia de fases que
termina en menos de 5 s (WCAG 2.2.2), sin bloquear nada: el titular y la acción principal se ven
desde el primer fotograma. `evaluate.mjs` espera esos 5 s antes de juzgar la primera pantalla.

## 3. Lo que se permite y cómo

- **Respuesta en controles:** pulsar (`scale(0.97)`), hover, foco; con versión táctil.
- **Continuidad espacial:** lo que aparece crece desde su disparador; lo que se descarta sale por
  donde entró; una fila que se abre en detalle viaja hasta él (View Transitions).
- **Entradas de sección:** una vez, al entrar el elemento en el 85–90 % de la ventana, subiendo
  12–32 px con opacidad; nunca contenido por encima del primer pantallazo esperando al scroll.
- **Escenas ligadas al scroll** (un escenario `position: sticky` cuyo progreso sale del scroll):
  solo si un criterio o la idea de la pantalla las necesitan, una o dos por página, con scroll
  nativo, la composición terminada diseñada para movimiento reducido y sin JavaScript, y un plan
  de teléfono. `pagina.html` trae el escenario común.
- Técnica, en orden: CSS → transiciones entre vistas del framework → Web Animations API → librería
  (con ADR y la verificación de `../../../shared/agent-security.md` §2).

## 4. Lo que no se usa

Pantalla o contador de carga, puertas antes del contenido, secuestro del scroll, cursores propios,
texto que se escribe solo, contenido retenido invisible más de 900 ms, movimiento que cruza un texto
que se lee, bucles que no se pausan fuera de pantalla o con movimiento reducido, sonido sin que la
persona lo active, el mismo fundido con el mismo tiempo en cada bloque.

## 5. Ficha `M-n`

Cada animación de la pantalla, en `design.md` → "Movimiento":
- propósito y frecuencia (§1);
- disparador y si ocurre una vez o se repite; elementos y propiedades (`transform`, `opacity`,
  `clip-path`; otras con justificación);
- duración y curva con tokens; estado inicial → final; escalonado;
- versión **reducida** (menos y más suave: se quitan desplazamiento, escala y reproducción
  automática), **sin JavaScript** (contenido completo) y **táctil**;
- coste en JavaScript contra el presupuesto de la constitución.

## 6. Rendimiento

Sin `filter` animado sobre superficies grandes ni `backdrop-filter` en elementos fijos; el
movimiento ligado al scroll solo en escenas o con `animation-timeline`, con un único script común
por proyecto; no se animan `width`, `height`, `top`, `left`, `margin` ni `padding`; `will-change`
solo justo antes de animar.
