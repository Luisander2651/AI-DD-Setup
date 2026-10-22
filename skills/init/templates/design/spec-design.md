---
spec: {{NNN}}-{{slug}}
status: draft            # draft | approved (solo el usuario aprueba)
exploration: {{loop|none}}      # loop: ciclo por criterios · none: sin diseño nuevo (motivo en "Resultado")
threshold: {{80}}        # puntuación mínima de la rúbrica (de .ai/project.yaml → design, o la de la spec)
floor: {{3}}             # nota mínima de cada punto de la rúbrica
budget: {{5}}            # candidatos como máximo
accepted: {{cN|none}}    # candidato aceptado; none si ninguno superó el umbral
score: {{n}}             # puntuación del aceptado (o del mejor, si accepted: none)
system_version: {{versión de docs/design/system.md}}
created: {{date}}
updated: {{date}}
---

# Diseño · {{NNN}} {{nombre}}

Hecho con `/design-spec {{NNN}}` sobre `docs/design/system.md`. Criterios en la spec ("Criterios de
diseño") y en `design/criterios.json`; candidatos en `design/candidatos/` (los descartados se
conservan).

## Candidatos

| Candidato | Puertas | KPIs | Rúbrica | Resultado | Informe |
|---|---|---|---|---|---|
| `c1` | {{9/10}} | {{7/8}} | — | descartado: {{G-contraste en 390 px; K1 fuera de la primera pantalla}} | `.ai/inspect/{{NNN}}-c1/report.md` |
| `c2` | {{10/10}} | {{8/8}} | {{84}} | aceptado | `.ai/inspect/{{NNN}}-c2/report.md` |

## Resultado

**{{c2}}**, {{aceptado con 84/100 (umbral 80, ningún punto bajo 3) · aceptado por el usuario bajo el
umbral: ver Decisiones · sin diseño nuevo: motivo}}. Página: `design/candidatos/{{c2}}.html`.

| Puerta o KPI | Objetivo | Medido | |
|---|---|---|---|
| {{G-contraste}} | {{4.5:1 · 3:1 texto grande}} | {{sin fallos a 390, 900 y 1440}} | ✅ |
| {{K1 · Acción principal en la primera pantalla (CA1)}} | {{"…" a la vista}} | {{a la vista en 390 y 1440}} | ✅ |

| Rúbrica | Peso | Nota | Evidencia |
|---|---|---|---|
| Jerarquía | {{25}} | {{4}} | {{captura · zona · por qué}} |
| Primera pantalla | {{25}} | {{5}} | {{…}} |
| Coherencia con el sistema y la marca | {{20}} | {{4}} | {{…}} |
| Lectura y ritmo | {{15}} | {{4}} | {{…}} |
| Diferencia frente a una plantilla | {{15}} | {{3}} | {{…}} |

## Pantallas

| Pantalla y estado | Ancho menor | Intermedio | Ancho mayor | Criterios |
|---|---|---|---|---|
| {{Nombre · reposo}} | `candidatos/{{c2}}.html` a {{390}} | {{900 · no aplica}} | a {{1440}} | {{CA1, CA2}} |

## Componentes

- **Del sistema:** {{componente → variante y estados}}.
- **Exclusivos de esta pantalla:** {{componente → anatomía con tokens; no se reutiliza en otra
  sección}}.

## Cambios a incorporar al sistema

<!-- Los aplica la primera tarea de /tasks en system.md y system.html, en el mismo commit que el
     código que los necesita, y añade sus colores a criterios.json → tokens.colors. Vacío: "Ninguno". -->
| Token, componente o regla | Modo | Valor (menor) | Valor (mayor) | Motivo |
|---|---|---|---|---|
| {{--token}} | {{fijo · fluido · corte N px}} | {{…}} | {{— si fijo}} | {{…}} |

## Movimiento

<!-- Solo si el aceptado tiene animaciones; si no: "Ninguno". Fichas de design-spec/references/movimiento.md §5. -->
### M-1 — {{nombre}}
- **Propósito y frecuencia:** {{…}}.
- **Disparador:** {{carga · entrada en pantalla · puntero fino · foco · toque}}; {{una sola vez · se repite}}.
- **Elementos y propiedades:** {{…}} · **Duración y curva:** {{--ease-… / ms}} · **inicial → final:** {{…}}.
- **Reducido:** {{…}} · **Sin JavaScript:** {{contenido completo y visible}} · **Táctil:** {{… · sin efecto}}.
- **Coste:** {{bytes de JS}} de {{presupuesto de la constitución}}.

## Accesibilidad

- **Contraste, toque y foco:** medidos por `evaluate.mjs` (puertas `G-contraste`, `G-toque`, `G-foco`).
- **Encabezados y estructura:** {{…}} · **Teclado:** {{orden}} · **Decorativos ocultos:** {{…}}.

## Decisiones

| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |
|---|---|---|---|---|
| {{date}} | {{diseño · brecha · implícita · contradicción · supuesto · refinado}} | {{…}} | {{…}} | {{usuario · ruta}} |
