---
spec: {{NNN}}-{{slug}}
plan: plan.md
status: draft
---

# Tareas · {{NNN}} {{nombre}}

Formato:
`- [ ] T### [P] <verbo + qué> — <archivos> — hecho cuando: <criterio> — cubre: CA# — depende: T###`
- T001–T089: trabajo. T090–T099: reservadas.
- `[P]` = paralelizable con las demás `[P]` de su grupo una vez cumplidas sus dependencias (no
  comparte archivos con otra tarea abierta).
- Lo generado por un comando cuenta como un archivo: `android/ (generado por npx cap add android)`.
- `[-]` = obsoleta (`— obsoleta: <motivo> (AAAA-MM-DD)`): no cuenta como abierta ni como hecha.
- Bajo una tarea: `  - nota: …`, `  - bloqueo: AAAA-MM-DD — <qué falta> — <skill a ejecutar>`.
- La comprobación a mano va en la tarea que construye la pieza:
  `hecho cuando: T010 pasa · verificación manual: <qué, dónde, contra qué>`.

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
- [ ] T091 Actualizar `docs/deployment.md` y `docs/observability.md` si cambiaron variables, entornos, pasos de deploy, logs, eventos de auditoría o métricas
- [ ] T092 Marcar spec como `implemented`

## Despliegue (lo ejecuta `/release`)
- [ ] T095 Desplegar a staging y verificar criterios de aceptación
  <!-- un sub-punto por cada `verificación manual:` del plan que exija staging, dispositivo físico
       o tienda: qué, dónde y resultado esperado; se registra el resultado real al hacerlo -->
- [ ] T096 Aprobación humana para producción
- [ ] T097 Desplegar a producción y vigilar métricas del plan (Rollout)
- [ ] T098 Marcar spec como `released`

## Cobertura
| Criterio | Tarea(s) de test | Tarea(s) de implementación |
|---|---|---|
| CA1 | T010 | T020 |

| Amenaza (TM#) | Tarea(s) de control | Tarea(s) de test |
|---|---|---|
| TM1 | T021 | T011 |

| Cambio del plan (módulo) | Tarea(s) |
|---|---|
| {{módulo}} | T020 |

| Requisito no funcional | Tarea(s) de test o verificación manual (T095) |
|---|---|
| {{RNF de la spec}} | {{T0xx · T095}} |
