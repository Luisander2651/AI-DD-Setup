---
spec: {{NNN}}-{{slug}}
plan: plan.md
status: draft
---

# Tareas · {{NNN}} {{nombre}}

Formato:
`- [ ] T### [P] <verbo + qué> — <archivos> — hecho cuando: <criterio> — cubre: CA# — depende: T###`
- T001–T089: trabajo. T090–T099: reservadas.
- `[P]` = paralelizable (no comparte archivos con otra tarea abierta ni depende de una pendiente).

## Constitution Check
{{confirmar que las tareas no violan ningún principio; referenciar plan.md}}

## Preparación
- [ ] T001 {{…}} — {{archivos}} — hecho cuando: {{…}}

## Tests (antes de implementar)
- [ ] T010 {{test que falla}} — {{archivos}} — hecho cuando: falla por la razón esperada — cubre: CA1

## Implementación
<!-- con varias historias entregables por separado: agrupar Tests + Implementación por historia -->
- [ ] T020 {{…}} — {{archivos}} — hecho cuando: T010 pasa — cubre: CA1 — depende: T010

## Integración y documentación
- [ ] T090 Actualizar `docs/architecture.md` si cambió la estructura
- [ ] T091 Actualizar `docs/deployment.md` si cambió variables, entornos o pasos de deploy
- [ ] T092 Marcar spec como `implemented`

## Despliegue (lo ejecuta `/release`)
- [ ] T095 Desplegar a staging y verificar criterios de aceptación
- [ ] T096 Aprobación humana para producción
- [ ] T097 Desplegar a producción y vigilar métricas del plan (Rollout)
- [ ] T098 Marcar spec como `released`

## Cobertura
| Criterio | Tarea(s) de test | Tarea(s) de implementación |
|---|---|---|
| CA1 | T010 | T020 |

| Cambio del plan (módulo) | Tarea(s) |
|---|---|
| {{módulo}} | T020 |
