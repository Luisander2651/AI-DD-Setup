---
spec: {{NNN}}-{{slug}}
status: draft   # draft | approved | blocked
created: {{date}}
---

# Plan · {{NNN}} {{nombre}}

## Enfoque técnico
{{resumen}}

## Constitution Check
| Principio | Resultado | Justificación / ajuste |
|---|---|---|
| P1 {{nombre}} | ✅ / ➖ / ❌ | |

Evaluar **todos** los principios. ➖ = no aplica (con motivo). Un ❌ solo se admite como
`❌ aceptado: <motivo> — aprobado por el usuario el <fecha>`; si no, el plan queda `blocked`.

## Cambios por módulo
| Módulo | Cambio | Riesgo |
|---|---|---|

## Contratos y datos
{{endpoints, esquemas, migraciones, tipos compartidos}}

## Estrategia de pruebas
{{qué se prueba y a qué nivel}}

## Modelo de amenazas
<!-- Obligatorio si la spec toca datos sensibles, autenticación, permisos o entradas externas;
     en otro caso, una línea explicando por qué no aplica. -->
| ID | Amenaza (STRIDE) | Categoría OWASP | Componente | Control | Test |
|---|---|---|---|---|---|
| TM1 | {{Spoofing / Tampering / Repudiation / Information disclosure / DoS / Elevation}} | {{A0x:año}} | {{…}} | {{…}} | {{…}} |

## Trazabilidad
| Criterio de aceptación | Cambio(s) | Test(s) |
|---|---|---|
| CA1: {{resumen}} | {{módulo}} | {{tipo y nombre del test}} |

Todo criterio de la spec (incluidos los de abuso) y toda amenaza `TM#` deben aparecer; un criterio
o amenaza sin test es un error del plan.

## Rollout
- Feature flag: {{nombre o "no aplica"}}
- Orden de despliegue: {{migraciones → backend → frontend, etc.}}
- Compatibilidad: {{¿convive con la versión anterior durante el deploy?}}
- Rollback: {{pasos concretos; si hay migración, cómo se revierte o por qué no hace falta}}
- Métricas a vigilar tras el deploy: {{errores, latencia, conversión…}}

## Decisiones (→ ADR si son arquitectónicas)
- {{…}}

## Impacto en arquitectura
- {{secciones de docs/architecture.md que habrá que actualizar al implementar}}

## Riesgos y mitigaciones
- {{…}}
