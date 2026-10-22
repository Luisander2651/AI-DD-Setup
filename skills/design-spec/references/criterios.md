# Criterios de diseño: qué tiene que lograr una pantalla y cómo se mide

El diseño no se elige por gusto: se acepta cuando **supera un nivel medible**. Este archivo dice de
dónde salen los criterios, cómo se escriben y cuáles se proponen por defecto. El ciclo que los usa
está en `evaluacion.md`.

Hay tres clases, en este orden de peso:

| Clase | Qué es | Quién la mide | Si falla |
|---|---|---|---|
| **Puertas** | Mínimos que ningún diseño puede incumplir | `scripts/evaluate.mjs` | El candidato se descarta sin evaluar la rúbrica |
| **KPIs** | Objetivos con número, sacados de los criterios de aceptación, la constitución y el tipo de pantalla | `scripts/evaluate.mjs` | El candidato se descarta |
| **Rúbrica** | Calidad que no se mide con un script, puntuada con escala anclada | Un subagente evaluador que no diseñó | El candidato se descarta si no llega al umbral |

## 1. Dónde viven

- **En la spec**, sección **"Criterios de diseño"** (`/specify` la escribe en specs con interfaz;
  `/design-spec` la completa con los valores por defecto de §4 si falta y pide aprobación): una
  tabla legible, con el ID de cada KPI, qué mide, el objetivo y de qué criterio de aceptación o
  principio sale.
- **En `docs/specs/NNN-<slug>/design/criterios.json`**, la misma información en el formato que lee
  `evaluate.mjs` (§3). La escribe `/design-spec` desde la tabla de la spec; si cambia la tabla,
  cambia el JSON en el mismo paso. `/review` y `/implement` usan este mismo archivo.
- **Umbral, mínimo por punto y presupuesto** salen de `.ai/project.yaml → design` (`threshold`,
  `floor`, `budget`); la spec puede cambiarlos para sí con una fila en "Decisiones".

Un criterio de aceptación con interfaz que no tenga al menos un KPI o una puerta que lo compruebe es
una brecha: añade el KPI o di en la tabla por qué no se puede medir en el diseño (p. ej. depende de
datos del servidor) y que lo verificará la tarea correspondiente.

## 2. Puertas

Siempre activas; la spec solo puede ajustar su valor con motivo (la constitución manda si es más
estricta):

| ID | Puerta | Valor por defecto |
|---|---|---|
| `G-desborde` | Sin desplazamiento horizontal a ningún ancho | — |
| `G-contraste` | Contraste de cada texto visible contra su fondo real | 4.5:1 · 3:1 en texto grande (≥ 24 px, o ≥ 18.66 px en negrita) |
| `G-toque` | Objetivos de toque por debajo de 1024 px (enlaces dentro de un párrafo, aparte) | 44 px (48 dp en Android) |
| `G-foco` | Foco visible en cada elemento al recorrer con el teclado | — |
| `G-tokens` | Ningún color fuera de los tokens del sistema (lista en `tokens.colors`) | — |
| `G-h1` | Un solo `h1` por página | 1 |
| `G-solapamiento` | Ningún texto tapado: ni otro texto que se cruza con él ni una imagen, un dibujo o una superficie con fondo encima (las barras fijas o sticky no cuentan) | — |
| `G-aparece` | Todo el contenido aparece al recorrer la página (ningún revelado que no se dispara) | — |
| `G-imagenes` | Toda imagen de contenido (y todo fondo con imagen) declara su origen con `data-origen` (§7) | — |
| `G-reducido` | Todo visible con `prefers-reduced-motion: reduce` | — |
| `G-sin-js` | Todo el contenido y los textos de los KPIs presentes sin JavaScript | — |
| `G-red` | Ningún recurso de otro sitio salvo los permitidos (`external_hosts`) | ninguno |
| `G-errores` | Ningún error de JavaScript en la página | — |

## 3. KPIs

Cada KPI tiene un `type` que `evaluate.mjs` sabe medir. Si un objetivo no encaja en ningún tipo,
no lo inventes: conviértelo en un punto de verificación manual de la tarea que lo construye.

| `type` | Mide | Campos |
|---|---|---|
| `above_fold` | Un texto (la acción principal) visible entero en la primera pantalla | `text`, `widths` opcional |
| `above_fold_all` | Varios textos en la primera pantalla | `texts`, `widths` opcional |
| `visible` | Textos exactos presentes en la página (los literales de los criterios de aceptación) | `texts` |
| `order` | Textos que aparecen en este orden en el contenido (las secciones que un criterio ordena) | `texts` |
| `max_bytes` | Peso de la primera visita | `value` (bytes) |
| `max_js_bytes` | JavaScript de la ruta (archivos e inline) | `value` (bytes) |
| `max_lcp_ms` | Pintado del contenido principal, en local | `value` (ms) |
| `max_cls` | Estabilidad visual | `value` |
| `max_heading_lines` | Líneas de cada `h1`–`h3` | `value` |
| `max_page_screens` | Largo de la página en pantallas al mayor ancho | `value` |
| `fonts_loaded` | Las familias de marca cargan de verdad (no la de reemplazo) | `families` |
| `scenes` | Escenas de scroll (`data-scene`) que de verdad se mueven al bajar, a cada ancho | `value` (mínimo) |
| `moving_elements` | Elementos que se mueven al cargar y al recorrer la página (en el ancho que menos tenga) | `value` (mínimo) |
| `custom_background` | Regiones (secciones, cabecera, pie) con fondo propio: imagen, degradado o un dibujo o imagen decorativa que cubre al menos un cuarto de la región | `value` (mínimo) |
| `max_samples` | Imágenes de muestra que quedan en la página (`data-origen="muestra"`) | `value` (máximo; 0 antes de publicar) |

Los textos de los KPIs se buscan primero en el contenido y después en la barra, el menú y el pie.

```json
{
  "spec": "038-pagina-inicio",
  "mode": "persuadir",
  "widths": [390, 900, 1440],
  "threshold": 80, "floor": 3, "budget": 5,
  "tokens": { "colors": ["#d75078", "#0b1120", "#f8fafc", "#ffffff"] },
  "gates": { "contrast": 4.5, "touch": 44, "external_hosts": [] },
  "kpis": [
    { "id": "K1", "name": "Acción principal en la primera pantalla", "type": "above_fold", "text": "Agendar mi primera cita", "ca": "CA1" },
    { "id": "K2", "name": "Contacto exacto", "type": "visible", "texts": ["753 000 0000"], "ca": "CA5" },
    { "id": "K3", "name": "JavaScript por ruta", "type": "max_js_bytes", "value": 102400, "ca": "P10" }
  ],
  "rubric": { "weights": { "jerarquia": 25, "primera_pantalla": 25, "sistema": 20, "lectura": 15, "plantilla": 15 } }
}
```

`tokens.colors` son los valores en hexadecimal de la tabla Color de `system.md` (y de "Cambios a
incorporar al sistema" si la spec los propone). Los anchos son `design.widths` más el intermedio
(≈ 900 px) si hay filas de elementos.

## 4. Valores por defecto según el modo de la pantalla

El **modo** dice qué tiene que lograr la pantalla; va en la tabla de la spec.

| Modo | Pantallas | KPIs que se proponen siempre |
|---|---|---|
| `persuadir` | Página de inicio, producto, servicios, portafolio, evento | Acción principal en la primera pantalla a todos los anchos; qué es y cómo contactar o actuar en la primera pantalla; los literales de los criterios presentes; orden de secciones si un criterio lo fija; peso y JavaScript de la constitución; CLS ≤ 0.1; titulares ≤ 3 líneas |
| `operar` | Panel, lista con filtros, formulario, ajustes, bandeja | La acción principal de la pantalla visible sin desplazarse; los literales y estados de los criterios presentes; JavaScript de la constitución; CLS ≤ 0.1; titulares ≤ 2 líneas |
| `leer` | Documentación, artículo, ayuda | Título y primer párrafo en la primera pantalla; los literales presentes; CLS ≤ 0.1 |

Los KPIs de negocio (cuánta gente se registra, cuántas citas salen de la página) **no** se miden
antes de publicar: se escriben como métricas en `docs/observability.md` y se revisan tras
`/release`. Lo que se mide aquí son sus aproximaciones (la acción a la vista, los pasos hasta ella).

## 5. Rúbrica

Cinco puntos con escala 0–5 **anclada**: la nota se da por la descripción que mejor encaja, con la
captura que lo muestra. La puntuación es la suma de `peso × nota / 5`, sobre 100.

| Punto | Peso | 1 | 3 | 5 |
|---|---|---|---|---|
| `jerarquia` · Jerarquía | 25 | Nada domina; todo pesa igual o compiten varias cosas | Hay un elemento principal pero el orden de lectura se pierde en alguna sección | En cada pantalla hay una cosa dominante y el orden de lectura es evidente sin leer |
| `primera_pantalla` · Primera pantalla en cinco segundos | 25 | No se sabe qué es ni qué hacer | Se entiende qué es; la acción o el dato clave cuesta encontrarlos | Qué es, para quién y qué hacer se entienden en cinco segundos, al menor y al mayor ancho |
| `sistema` · Coherencia con el sistema y la marca | 20 | Parece otro producto; la marca no aparece o se contradice | Usa el sistema pero con piezas sueltas que no encajan | Se reconoce la marca (logo, color, forma) y todo encaja en el sistema |
| `lectura` · Lectura y ritmo | 15 | Texto apretado, líneas largas, saltos de tamaño sin orden | Se lee bien con alguna sección densa o algún hueco sin motivo | Medida, interlineado y espacios dan un ritmo claro en todos los anchos |
| `plantilla` · Diferencia frente a una plantilla | 15 | Intercambiable con cualquier plantilla del sector (hero centrado, fila de tarjetas iguales) | Tiene algún recurso propio, pero el resto es de plantilla | Usa el contenido y los recursos de la marca de forma que, con otro logo, la composición dejaría de tener sentido |

| `riqueza` · Riqueza visual y movimiento (opcional, peso 0 por defecto) | 0 | Fondos planos y nada se mueve, o efectos sueltos sin relación con el contenido | Algún fondo propio o movimiento, pero aislado o genérico | Fondos, imágenes y movimiento forman un recorrido con el contenido (se ve en la tira del scroll) y la página se lee completa sin ellos |

Las notas 2 y 4 son intermedias. `riqueza` solo cuenta si la spec le da peso (y entonces los demás
pesos bajan para sumar 100); el evaluador la juzga con la tira del scroll (`film-*.png`), no solo
con la captura completa. **Umbral de aceptación**: puntuación ≥ `threshold` (80 por
defecto) **y** ningún punto por debajo de `floor` (3 por defecto). Los pesos pueden cambiar por
spec con motivo (p. ej. `plantilla` 0 en una pantalla de ajustes), registrado en "Decisiones".

## 6. Pedir una página más elaborada

Fondos propios, escenas de scroll o fotos se piden como criterios, no como gusto: así el ciclo no
puede saltárselos y la rúbrica los valora.
- **KPIs:** `scenes` (p. ej. ≥ 1), `moving_elements` (p. ej. ≥ 12), `custom_background` (p. ej. ≥ 2).
- **Rúbrica:** peso a `riqueza` (p. ej. 15, restándolo de los otros puntos) con su motivo en
  "Decisiones".
- Las puertas siguen mandando: todo visible con movimiento reducido y sin JavaScript, nada tapado.

## 7. Imágenes y su origen

Toda imagen de contenido declara `data-origen` en la etiqueta (o en el elemento que la lleva de
fondo): `propia` (del proyecto), `generada` (con una herramienta de imagen), `archivo` (colección
abierta con licencia que permita uso comercial y crédito), `muestra` o `dibujada`.
- **Muestra:** foto de banco con licencia libre (Unsplash, Pexels…) para ver la composición con una
  imagen real mientras no hay propias. Solo si el brief no la rechaza o el usuario lo decide (fila
  en "Decisiones"). Nunca representa al negocio (su local, su equipo, su producto, sus clientes):
  solo el mundo alrededor (una calle, un material, un objeto genérico). Va al repo con su licencia y
  su fuente, se lista en el acta ("Imágenes de muestra") y `/review` y `/release` exigen
  `max_samples: 0` salvo decisión del usuario.
- Si la sesión no puede descargar imágenes (red restringida), pide al usuario las fotos o que
  permita el dominio; mientras tanto, dibuja desde el sujeto (`dibujada`). Nunca un hueco gris.

## 8. Lo que no es un criterio

- Gustos sin forma de medir o de anclar ("que se vea moderno", "más premium"): pide el ejemplo
  concreto y conviértelo en un punto de la rúbrica o en un KPI, o déjalo fuera.
- Un umbral que ningún candidato razonable puede cumplir: si dos ciclos seguidos fallan en el mismo
  KPI, el problema es el criterio; propón ajustarlo (`evaluacion.md` §5).
