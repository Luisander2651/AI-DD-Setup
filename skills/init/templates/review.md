---
spec: {{NNN}}-{{slug}}
verdict: {{approved|changes_requested|blocked}}
round: {{1}}
date: {{date}}
base: {{commit o rama base}}
head: {{commit revisado}}
human_signoff: {{pending|<nombre> <fecha>|no requerido}}
---

# Review · {{NNN}} {{nombre}}

## Resumen
{{veredicto y motivo en 2–3 frases}}

## Verificación automática
| Comando | Resultado |
|---|---|
| {{test}} | ✅ / ❌ ({{n}} fallos; línea base: {{n}}) |
| {{lint}} | |
| {{build}} | |

## Criterios de aceptación
| CA | Test | Estado | Nota |
|---|---|---|---|
| CA1 | {{ruta::nombre}} | ✅ / ❌ / ⚠ | |

## Conformidad con el plan
- Cambios fuera del plan: {{archivos o "ninguno"}}
- Partes del plan sin implementar: {{…}}

## Constitution Check (sobre el código)
| Principio | Resultado | Evidencia |
|---|---|---|

## Seguridad
| Herramienta | Resultado |
|---|---|
| {{secretos}} | ✅ / ❌ ({{n}} hallazgos) |
| {{SAST}} | |
| {{SCA}} | {{crít: n · alta: n · media: n}} |
| {{contenedores}} | |

| Tema OWASP | Resultado | Evidencia |
|---|---|---|
| {{A01:año Control de acceso}} | ✅ / ➖ / ❌ | |

## Hallazgos
| ID | Severidad | Archivo:línea | Hallazgo | Sugerencia |
|---|---|---|---|---|
| R1 | bloqueante / importante / menor | | | |

## Preparación para release
- Rollback factible: {{sí/no + motivo}}
- Migraciones compatibles con la versión anterior: {{…}}
- Docs actualizadas (architecture, deployment): {{…}}

## Tareas añadidas
- {{T0xx ← R1}}
