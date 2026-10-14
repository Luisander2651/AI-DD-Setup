---
lane: {{fix|hotfix|refactor|chore}}
status: open                 # open → done → released · escalated (→ escalated_to)
base: {{commit}}             # commit de partida; lo registra la skill al empezar (lo usa lane-check)
relates: [{{NNN}}]           # specs cuyo comportamiento toca ([] si ninguna)
covers: [{{CA1}}]            # fix: criterios de esas specs que el arreglo vuelve a cumplir
escalated_to: null           # NNN de la spec si el cambio se escaló al flujo completo
---

# {{Carril}}: {{título corto}}

<!-- Ficha de un carril ligero (shared/contract.md → "Carriles", shared/lanes.md). Se llama
     docs/changes/AAAA-MM-DD-<carril>-<slug>.md. Borra las secciones que no son de tu carril:
     Reproducción y Causa raíz → fix/hotfix · Tests de caracterización → refactor. -->

## Problema
{{síntoma: qué se ve, dónde y desde cuándo · deuda: qué cuesta hoy · chore: qué hay que poner al día}}

## Reproducción
{{test que falla: ruta y nombre, y su salida en rojo antes del arreglo}}

## Tests de caracterización
{{qué comportamiento fijan, ruta de los tests y su salida en verde antes del cambio}}

## Causa raíz
{{por qué pasa, no solo dónde}}

## Cambio
{{qué se cambió y en qué archivos; commits `<tipo>(<carril>-<slug>): <qué>` con `Ficha: <ruta>`}}

## Escalado
{{salida resumida de `aidd.py lane-check` al empezar y al cerrar, y qué se decidió}}

## Verificación
{{test en verde, suite, lint/SAST/SCA según el carril, resultado de la review ligera}}

## Decisiones
| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |
|---|---|---|---|---|
