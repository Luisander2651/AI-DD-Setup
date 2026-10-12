---
spec: {{NNN}}-{{slug}}
status: draft            # draft | approved (solo el usuario aprueba)
exploration: {{options|none}}   # none: sin composiciones (motivo en "Dirección elegida")
system_version: {{versión de docs/design/system.md}}
created: {{date}}
updated: {{date}}
---

# Diseño · {{NNN}} {{nombre}}

Hecho con `/design-spec {{NNN}}` sobre el sistema `docs/design/system.md`. Composiciones en
`design/opcion-<a|b|c>.html` (las descartadas se conservan).

## Dirección elegida

**{{Composición A · "Nombre"}}**, elegida entre {{A · …, B · …, C · …}}{{; combinada con … de B}}.

{{Metáfora en una o dos frases: qué cuenta la composición y con qué dato real de la spec.}}

- **Motivo:** {{por qué esta, ligado al brief o al contenido}}.
- **Vecino más parecido:** {{pantalla o sección}} → se diferencia en {{estructura, ritmo, componente firma}}.
- **Riesgo asumido:** {{qué se sacrifica}} → {{cómo se compensa}}.

## Pantallas

| Pantalla y estado | Ancho menor | Intermedio | Ancho mayor | Criterios |
|---|---|---|---|---|
| {{Nombre · reposo}} | `opcion-a.html#{{id}}-m` | {{`#{{id}}-i` · no aplica (sin filas)}} | `opcion-a.html#{{id}}-d` | {{CA1, CA2}} |

## Composición y jerarquía

- **Orden de lectura:** {{1. … 2. …}} (igual en todos los anchos salvo {{…}}).
- **Proporciones:** {{destacado 7:5, mosaico 5:7, alturas igualadas… o "rejilla de iguales: motivo"}}.
- **Puntos de corte:** {{los del sistema · propio de esta composición: N px, porque …}}.
- **Momento protagonista:** {{ninguno · M-1}} (según "Reglas de uso" del sistema).

## Componentes

- **Del sistema:** {{componente → variante y estados}}.
- **Exclusivos de esta pantalla:** {{componente firma → anatomía con tokens; no se reutiliza en otra
  sección}}.
- **Adornos generados desde datos:** {{índice desde `order`, ruta desde el ancla…; ocultos a
  lectores de pantalla}}.

## Cambios a incorporar al sistema

<!-- Los aplica la primera tarea de /tasks en system.md y system.html, en el mismo commit que el
     código que los necesita. Vacío: "Ninguno". -->
| Token, componente o regla | Modo | Valor (menor) | Valor (mayor) | Motivo |
|---|---|---|---|---|
| {{--token}} | {{fijo · fluido · corte N px}} | {{…}} | {{— si fijo}} | {{…}} |

## Movimiento

### M-1 — {{nombre}}
- **Disparador:** {{carga · entrada en pantalla · puntero fino · foco · toque}}; {{una sola vez · se repite}}.
- **Elementos y propiedades:** {{…}} (`transform`, `opacity`{{, `filter`: justificación}}).
- **Duración y curva:** {{--duration-… / --ease-…}}; **inicial → final:** {{…}}; **secuencia:** {{…}}.
- **Técnica:** {{CSS · transición entre vistas · Web Animations API · librería (ADR)}}.
- **Reducido:** {{…}} · **Sin JavaScript:** {{contenido completo y visible}} · **Táctil:** {{… · sin efecto}}.
- **Coste:** {{bytes de JS}} de {{presupuesto de la constitución}}; comparte propiedades con: {{ninguna}}.
- **Fotogramas:** `opcion-a.html#movimiento`.

## Accesibilidad

- **Contraste** (calculado): {{par → n.n:1}}.
- **Encabezados y estructura:** {{…}} · **Teclado:** {{orden y foco}} · **Decorativos ocultos:** {{…}}.
- **Sin animación:** todo el contenido en el HTML, visible sin JavaScript y con movimiento reducido.

## Anti-clichés

| Cliché que esta pantalla podría caer | Alternativa usada |
|---|---|
| {{tarjetas idénticas en rejilla}} | {{destacado 7:5 delante del resto}} |

## Decisiones

| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |
|---|---|---|---|---|
| {{date}} | {{diseño · brecha · implícita · contradicción · supuesto · refinado}} | {{…}} | {{…}} | {{usuario · ruta}} |
