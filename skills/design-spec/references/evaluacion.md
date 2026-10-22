# El ciclo: generar, medir, evaluar, repetir

`/design-spec` no presenta opciones para elegir por gusto. Genera **un candidato tras otro** y solo
acepta el primero que supera los criterios (`criterios.md`): todas las puertas, todos los KPIs y la
rúbrica por encima del umbral. El usuario aprueba el resultado con su acta, no elige entre bocetos.

```
criterios ─► candidato N ─► evaluate.mjs ─┬─ falla puerta o KPI ──────────────► fallos ─┐
                                          └─ pasa ─► evaluador (rúbrica) ─┬─ < umbral ─► fallos ─┤
                                                                          └─ ≥ umbral ─► ACEPTADO │
             ▲                                                                                     │
             └──────────────────────── candidato N+1 (corrige los fallos) ◄─────────────────────────┘
             (hasta `budget` candidatos; sin aceptado → el mejor y lo que le faltó)
```

## 1. Antes del primer candidato

1. Criterios aprobados: la tabla "Criterios de diseño" de la spec y `design/criterios.json`
   (`criterios.md` §1). Sin ellos no se genera nada.
2. Lee el sistema (`system.md` y `system.html`), los `design.md` de las pantallas vecinas y el
   contenido real de la spec.
3. **Abre y mira** los recursos de marca que existen (logo, íconos, fotos, ilustraciones) con la
   herramienta Read: el candidato los usa tal como son. Lista los que no existen; nunca inventes
   testimonios, cifras ni logos. Las fotos que faltan solo se cubren con imágenes de muestra si el
   brief o el usuario lo permiten, con las reglas de `criterios.md` §7.

## 2. Generar un candidato

- **Formato:** una página real a ancho de ventana desde `../../init/templates/design/pagina.html`,
  autocontenida, en `docs/specs/NNN-<slug>/design/candidatos/c<N>.html` (`N` = 1, 2…). Solo tokens
  del sistema y los de "Cambios a incorporar al sistema" que el candidato proponga (cada uno con su
  motivo en la cabecera del archivo); fuentes incrustadas desde los archivos que usará la app;
  contenido real completo de la spec.
- **Primer candidato:** la composición más directa que cumple los criterios con el sistema y el
  contenido: lo que pide cada KPI, en el orden que fijan los criterios, con la jerarquía que pide la
  rúbrica. No es una exploración: es el intento serio de pasar.
- **Siguientes candidatos:** parten del mejor candidato hasta ahora y **corrigen su lista de
  fallos**: cada puerta y KPI fallidos y los tres problemas que señaló el evaluador. Cambia solo lo
  necesario para corregirlos; si el mismo fallo vuelve dos veces con la misma solución, prueba una
  estructura distinta para esa sección.
- **Movimiento y fondos:** los que pidan los criterios (`scenes`, `moving_elements`,
  `custom_background`, peso de `riqueza`), con las reglas de `movimiento.md`; las escenas sobre el
  escenario de `pagina.html`. Sin esos criterios, una animación no suma puntos por sí misma.
- **Imágenes:** cada una con `data-origen` (`criterios.md` §7).

## 3. Medir

```
node <skill>/scripts/evaluate.mjs docs/specs/NNN-<slug>/design/candidatos/c<N>.html \
  --criteria docs/specs/NNN-<slug>/design/criterios.json --out .ai/inspect/NNN-c<N>
```

`<skill>` es la carpeta de esta skill. Deja en `--out` el `report.md` y el `report.json` con cada
puerta y KPI, capturas por ancho (claro, movimiento reducido, sin JavaScript) y la tira del scroll.
`.ai/inspect/` va en `.gitignore`. Código 0: pasan puertas y KPIs → §4. Código 1: el candidato
queda **descartado**; sus fallos son la lista del siguiente (§2). Código 3 (sin Playwright): §6.

## 4. Evaluar la rúbrica

Lanza un **subagente evaluador** (perfil `critical`, contrato → "Modelo de cada subagente") que
**no** ha visto cómo se generó el candidato. Recibe solo:
- las capturas de `--out` (todas: anchos, reducido, sin JavaScript y la tira);
- la rúbrica de `criterios.md` §5 con sus anclas y los pesos de `criterios.json` (con `riqueza`
  solo si tiene peso, juzgada sobre la tira del scroll);
- el modo de la pantalla y los criterios de aceptación de la spec (para juzgar la primera pantalla);
- si existe, las capturas del **mejor candidato aceptado o con mejor puntuación** hasta ahora.

Instrucciones para el evaluador:

```
Eres el evaluador de diseño. No diseñaste esto y no lo vas a mejorar: lo puntúas.
1. Por cada punto de la rúbrica, elige la nota 0–5 cuya descripción encaja mejor y cita la captura
   (archivo y zona) que lo muestra. Sin captura que lo muestre, la nota no puede pasar de 3.
2. Si recibes un candidato anterior, compara los dos punto por punto y di cuál es mejor en cada uno
   (o "igual"); tu nota debe ser coherente con esa comparación.
3. Lista los tres problemas que más bajan la nota, cada uno con la captura y qué tendría que pasar
   en la pantalla para corregirlo (sin proponer estilos nuevos fuera del sistema).
Responde solo con JSON:
{"scores":{"jerarquia":n,"primera_pantalla":n,"sistema":n,"lectura":n,"plantilla":n[,"riqueza":n][,"tipografia":n]},
 "evidence":{"<punto>":"<archivo · zona · por qué>"},
 "vs_best":{"<punto>":"mejor|peor|igual"},"problems":["…","…","…"]}
```

Calcula la puntuación (`Σ peso × nota / 5`). **Aceptado** si la puntuación ≥ `threshold` y ningún
punto está por debajo de `floor`. Si no, los tres problemas se suman a la lista del siguiente
candidato. Si el evaluador dice "peor" en la mayoría de puntos frente al mejor anterior, el nuevo no
sustituye al mejor aunque su nota sea parecida.

## 5. Parar

- **Aceptado:** termina el ciclo; no se gastan los candidatos restantes.
- **Presupuesto agotado** (`budget` candidatos sin aceptado): para. Presenta el de mejor puntuación
  entre los que pasaron puertas y KPIs (o, si ninguno pasó, el que menos falló), con lo que le falta.
  Si el mismo KPI o el mismo punto de la rúbrica falló en todos, dilo: el problema probablemente es
  el criterio (inalcanzable, contradictorio o mal medido). El usuario decide entre ajustar el
  criterio y repetir el ciclo, aceptar el mejor por debajo del umbral (decisión en "Decisiones"
  con su motivo, fuente `usuario`) o dar otro presupuesto.
- Un candidato descartado no se borra: queda en `candidatos/` con su resultado en el acta.

## 6. Sin Playwright

Si `evaluate.mjs` no encuentra Playwright (código 3), mide con la herramienta de navegador de la
sesión a los mismos anchos: desbordamiento, contraste de los pares principales, toques, textos de los
KPIs y orden, con movimiento reducido y sin JavaScript. Marca en el acta cada puerta y KPI como
`medido a mano` o `no medido`. Un KPI `no medido` no cuenta como superado: el candidato no puede
aceptarse hasta medirlo (o hasta que el usuario lo acepte así en "Decisiones").

## 7. El acta (`design.md`)

`design.md` (plantilla `../../init/templates/design/spec-design.md`) registra el ciclo:
- frontmatter: `exploration: loop`, `threshold`, `floor`, `budget`, `accepted` (`c<N>` o `none`) y
  `score` del aceptado;
- una fila por candidato: puertas, KPIs, puntuación, resultado (`descartado: <motivo>` ·
  `aceptado`) y la ruta de su informe;
- del aceptado: la tabla de puertas y KPIs con lo medido, las notas de la rúbrica con su evidencia,
  los componentes que usa, los cambios al sistema, las fichas de movimiento si las hay y las
  **imágenes de muestra** con su fuente y licencia (el informe las lista), que se sustituyen antes
  de publicar.

Presenta al usuario el acta y el candidato aceptado (abre la página o pasa sus capturas). El usuario
no elige entre opciones: aprueba el resultado (`status: approved`) o ajusta criterios.
