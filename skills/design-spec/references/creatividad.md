# Creatividad: de la idea a una pantalla que no podría ser de otro

Motor de las composiciones de `/design-spec` (modo `system` §2.4 y modo `NNN` `spec-mode.md` §2).
Los anti-clichés dicen qué no hacer; este archivo dice **con qué ser audaz**. Las dos cosas van
juntas: quitar adornos sin poner nada en su lugar deja una página delgada, y una página delgada
pierde contra una más rica aunque esa tenga rasgos de plantilla.

## 1. Modo de la pantalla

Antes de componer, decide qué clase de pantalla es; cambia cuánto se inventa y qué movimiento cabe.

| Modo | Qué es | Dónde va la audacia |
|---|---|---|
| **Persuadir** | Se lee y se recorre: landing, sitio de producto o marketing, portafolio, evento, restaurante, página de una sola pieza, la portada de un blog | Composición, escala tipográfica, campos de color, imágenes grandes, 1–3 escenas de scroll, una cosa viva |
| **Experiencia** | Se explora o se juega: un configurador, una historia interactiva, un archivo para curiosear | Igual que Persuadir, con más peso en la cosa viva |
| **Operar** | Se trabaja en ella: panel, administración, ajustes, bandeja, lista con filtros, editor, formulario largo | En **cómo se siente**: continuidad espacial, respuesta inmediata, estados cuidados, deleite en momentos raros |
| **Leer** | Se consulta: documentación, artículo largo, ayuda | Tipografía, ritmo, orientación; movimiento casi nulo |

Un sitio de producto que enseña su app es Persuadir; los fragmentos de interfaz que muestra siguen
las reglas de Operar por dentro y se construyen como piezas reales de esa app (datos que cuadran,
un hallazgo enunciado), nunca barras grises. Una spec que mezcla los dos (la landing y el panel
detrás) declara el modo por pantalla. El modo va en `design.md` → "Dirección elegida".

## 2. Inventario del sujeto

Escribe en tus notas (y resume en el HTML de cada opción, sección "Idea") **8–12 cosas que son de
este proyecto y de ningún competidor**, sacadas del brief, la spec, `nicho.md` y el contenido real:
- su **nombre** y lo que significa; su **lugar** (calle, barrio, ciudad, cómo se ve, su luz);
- los **números** del brief (plazas, minutos, el precio, el año, la tirada);
- la **restricción** con la que vive (una tanda al mes, solo con cita, cerrado en invierno);
- sus **materiales y colores** reales; sus **rituales y horarios**;
- los **objetos impresos** de su mundo (billete, etiqueta, menú, recibo, manual, ficha, plano);
- lo que **produce**: su salida real (un informe, un plato, un despliegue, un recibo);
- su **forma**: cómo se ve en corte, en silueta, de canto.

En software y servicios sin lugar físico, el inventario sale del **mundo del público**: las
tradiciones gráficas y de pantalla que lee a diario (notación, publicaciones, señalética, gráficos
de datos, documentos de su oficio), sus lugares y rituales. Pregúntate también cómo sería como
objeto físico y cómo era su mundo antes de la web.

Reglas del inventario:
- **Tres familias de material como mínimo.** Si más de la mitad de las entradas son de la misma
  familia (todo papelería, todo instrumentos), te quedaste en el artefacto obvio: sigue buscando.
- En pantallas de **Operar o Leer**, las herramientas que el público maneja (terminal, osciloscopio,
  tablero de control) no son material: llevadas a la pantalla salen como disfraz. En Persuadir,
  como mucho una entrada.
- La lectura literal del nombre o de una metáfora que trae el brief cuenta como **una** entrada,
  no como la idea.

## 3. La idea

Escribe esta frase y **no compongas hasta tener los dos huecos llenos desde el inventario**:

> En esta pantalla, **[algo que es del sujeto]** se convierte en **[el recurso que organiza la composición]**.

Dónde buscar el primer hueco: su salida (el producto real puesto como material de la página), su
objeto o su forma (ampliado, recortado, convertido en marco), su nombre (las letras que contienen
una imagen, se apilan o se parten), su lugar (la vista que da ganas de estar), su ritual (una
secuencia que la página interpreta al recorrerla), su artefacto impreso, su opuesto (qué otra
categoría tiene la sensación que a esta le falta).

**Prueba del competidor:** pon al competidor más cercano en la frase (la otra panadería de la
calle, otra app de reservas, otro portafolio de desarrollador). Si la frase sigue funcionando, la
idea es de la categoría: rehazla. "Limpio y moderno" no es una idea. Una idea que no cambia la
estructura es solo un nombre.

**La idea llega a todas las secciones:** precios, preguntas, formulario y pie incluidos. El fallo
más común, también en sitios buenos, es una primera pantalla distinta seguida de bloques de
plantilla.

## 4. Registro y reparto

Cada composición declara un **registro**:

| Registro | Qué cambia |
|---|---|
| **sobrio** | Composición propia con movimiento de respuesta y entradas; sin escenas; color contenido |
| **firme** | Una pieza firma clara, color comprometido, una escena en Persuadir |
| **audaz** | Composición que rompe la expectativa del sector, color empapado o paleta completa, 2–3 escenas en Persuadir, la cosa viva en primer plano |

- Las 2–3 composiciones cubren **registros distintos** y **al menos una es `audaz`**. Lo que limite
  `creative-direction.md` → "Movimiento" (intensidad) o la constitución manda: dilo en la opción.
- **Reparto contra el sesgo.** Antes de componer, ejecuta
  `python .ai/bin/aidd.py deal --mode <persuadir|operar>` (sin `.ai/bin`, el script del plugin): reparte
  jugadas firma y escenas del catálogo (`movimiento.md` §5) con una semilla. Asigna jugadas
  **distintas** a cada composición y elige, para cada una, la que el inventario puede llenar.
  Repetir el reparto (`--seed <otra>`) solo con un motivo que puedas escribir (choca con una
  restricción de marca, necesita imágenes que no existen), nunca para ir a lo cómodo; registra la
  semilla y cada repetición en "Decisiones" (tipo `diseño`). Una jugada que no dice nada del sujeto
  es decoración: la composición queda mejor sin ella.
- **Salida estándar.** Además de las composiciones, ofrece siempre en una línea "la convención del
  sector, bien hecha". Nunca la recomiendes ni dejes que suavice las demás. Si el usuario la elige,
  pide 2–3 productos con los que debe convivir, su nivel de acabado es el listón y se ejecuta sin
  ironía; queda en "Decisiones".
- **Otra ronda más audaz o más segura.** Si el usuario lo pide al elegir: *más audaz* = formas
  ajenas al sector y registro `audaz` en todas; *más segura* = las candidatas convencionales que
  quedaron fuera y la salida estándar contra competidores con nombre. Se archiva la ronda anterior
  (`system-mode.md` §2.7).

## 5. La cosa viva

Cada pantalla de **Persuadir o Experiencia** tiene **una** cosa que el visitante puede hacer, o que
es distinta en cada visita, hecha con la idea y con contenido real: elegir la madera y ver la silla
en ella; escribir tu nombre y verlo en las letras de la fundición; mover el préstamo y leer la cuota
real; ver si la estufa del refugio está encendida y cuánto falta para el último ferri; elegir una
talla y verla contra la habitación; filtrar el archivo por año y ver cómo cambia el mapa.

Reglas: usa contenido real del proyecto; funciona en el teléfono con el pulgar; tiene una versión
sin JavaScript que se lee entera; nunca bloquea la lectura ni la acción principal; es **una**, no un
parque de juegos; vive en la sección donde prueba lo que dice la página (a menudo el hero o la
reserva). Se diseña como composición (Paso 2), no se añade al final como efecto. En Operar no es
obligatoria: su lugar lo ocupa la ambición de sensación (`movimiento.md` §6).

## 6. Plenitud

Contrapeso de los anti-clichés: el espacio que dejan los adornos se llena con sustancia.

- **Escala.** Dos o tres tamaños hacen el trabajo visible: uno muy grande y uno pequeño. En
  Persuadir, el titular mide al menos ~4 veces el cuerpo (los mejores sitios estudiados llegan a
  ~8vw); interletrado del titular −0.02 a −0.05em, interlineado 0.85–1.05; cinco tamaños por página
  como techo. Titulares en dos líneas o menos a todo ancho (≈ 32 caracteres es seguro).
- **Estrategia de color**, declarada por opción antes de elegir colores:
  `contenida` (neutros teñidos del territorio y un acento; normal en Operar y Leer) ·
  `comprometida` (un color saturado ocupa 30–60 % de la superficie) ·
  `paleta completa` (3–4 papeles con nombre) · `empapada` (la superficie es el color). El color se
  decide a escala de página: campos que ocupan regiones enteras, no acentos sueltos sobre gris.
  Claro u oscuro no es un valor por defecto: escribe una frase de la escena física (quién lo usa,
  dónde, con qué luz) y que decida ella.
- **Imágenes**, en este orden: las del proyecto → generadas, si la sesión tiene una herramienta de
  imagen → imágenes reales del mundo del sujeto en colecciones abiertas con licencia que permita uso
  comercial (archivo, mapas, grabados, láminas), descargadas al repo y **acreditadas** → dibujadas en
  código desde el propio sujeto (sus objetos, su interfaz, sus azulejos) con un lenguaje gráfico
  único en los colores reales de la paleta → solo tipo y color. Una imagen encontrada muestra el
  mundo alrededor del cliente y **nunca** se presenta como su producto, su local o su equipo. Si el
  proyecto tiene una imagen o vídeo real de su producto o su proceso, la primera pantalla la enseña
  grande (≈ 40 % o más). Una imagen dominante gana a seis pequeñas; mismos recortes y tratamiento.
  Sin red, dibuja y dilo.
- **Contenido completo.** Cada sección entrega su información entera (el menú con precios, cada
  habitación con sus datos, cada ponente). Las secciones delgadas son la razón más común por la que
  una página limpia pierde contra una más cargada. Prueba social nunca inventada.
- **Cada pantalla de escritorio es un cartel:** una cosa dominante y el contenido que lleva. Un
  descanso deliberado (un campo de color o una imagen) por página como máximo; ningún tramo de más
  de media pantalla vacío; márgenes exteriores iguales y la asimetría dentro de la rejilla, nunca en
  el marco (un vacío se cierra con algo al otro lado).
- **El pie es un cierre diseñado,** no un mapa del sitio: en la mayoría de los sitios fuertes el
  nombre vuelve a todo el ancho.

## 7. Pruebas antes de enseñar

Responde cada una por composición en su HTML (sección "Idea"):
1. **Competidor:** la frase de la idea con el competidor ya no funciona.
2. **Esqueleto:** quita los textos; la estructura sola dice qué es la sección y por qué importa.
3. **Retirada:** quita la jugada firma o la escena; si nadie lo nota, sobra o está mal llenada.
4. **Vecino:** se diferencia de la pantalla más parecida del producto (`spec-mode.md` §2).
5. **Cinco segundos:** alguien que ve la primera pantalla cinco segundos sabe qué es y qué hacer.
6. **Inspección:** `inspeccion.md` sin fallos y con su crítica escrita.

## 8. Ajustes después de elegir (`--bolder` · `--quieter`)

`/design-spec NNN --bolder <sección>` o `--quieter <sección>`, cuando una sección elegida se lee
plana o grita. Aplican a lo que ya está diseñado; durante una ronda abierta, "más audaz" es §4.
- **El alcance manda.** Solo se toca la sección nombrada; nada de colores, fuentes, radios ni
  sombras nuevos que el sistema no tenga. Si el sistema no puede expresarlo, pregunta qué añadir y
  para qué.
- **Más audaz:** una sección plana suele ser la que no usa los recursos fuertes que sus vecinas ya
  usan. Sube esta sección al nivel de las demás con su propio vocabulario: tipo display a toda
  fuerza, la pieza firma, un cambio de densidad o de ritmo que la convierta en un pico del
  recorrido. Un solo movimiento decidido, y lo de alrededor más quieto para que se lea: si todo sube,
  la sección queda más plana. Nunca "más efectos".
- **Más tranquila:** quita lo que compite con la jugada principal; conserva la idea y el contenido.
- Registra el cambio con la decisión `refinado` en `design.md`; si toca el sistema, "Cambios a
  incorporar al sistema". Vuelve a pasar `inspeccion.md` sobre la sección.
