---
spec: {{NNN}}-{{slug}}
status: draft   # draft | approved | blocked
constitution_version: {{versión de docs/constitution.md}}
created: {{date}}
---

# Plan · {{NNN}} {{nombre}}

## Enfoque técnico
{{resumen}}

## Constitution Check
| Principio | Resultado | Justificación / ajuste | Cómo se verifica |
|---|---|---|---|
| P1 {{nombre}} | ✅ / ➖ / ❌ | | {{test: … · lint: … · manual: … · — si ➖}} |

Evaluar **todos** los principios. ➖ = no aplica (con motivo). Todo ✅ dice cómo se verifica; un
principio con número, umbral o prohibición comprobable se verifica con test o lint. Un ❌ solo se admite como
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
| TM1 | {{Spoofing / Tampering / Repudiation / Information disclosure / DoS / Elevation}} | {{A0x:año}} {{· MASVS-… en mobile}} | {{…}} | {{…}} | {{…}} |

## Trazabilidad
| Criterio de aceptación | Cambio(s) | Test(s) |
|---|---|---|
| CA1: {{resumen}} | {{módulo}} | {{tipo y nombre del test}} |

Todo criterio de la spec (incluidos los de abuso) y toda amenaza `TM#` deben aparecer; un criterio
o amenaza sin test es un error del plan.

## Observabilidad
<!-- Obligatoria si la spec toca datos sensibles, autenticación o permisos; en otro caso, una
     línea con el motivo. -->
- Logs nuevos: {{evento → nivel → campos}} (sin datos sensibles; con `request_id`)
- Eventos de auditoría: {{evento → dónde se emite → test}}
- Métricas y alertas: {{…}}
- Cómo se verifica tras el deploy: {{consulta o dashboard}}

<!-- if seo.indexable=true -->
## Descubribilidad
<!-- Obligatoria si la spec crea o cambia rutas públicas; en otro caso, `No aplica: <motivo>`.
     Una fila por ruta nueva o modificada, según docs/seo.md y shared/seo-checklist.md. -->
| Ruta | Indexable | Título | Descripción | Canónica | Sitemap | Datos estructurados | Test |
|---|---|---|---|---|---|---|---|
| {{/ruta/}} | {{sí · no (motivo)}} | {{…}} | {{…}} | {{URL absoluta}} | {{sí · no}} | {{tipo de schema.org · —}} | {{test sobre el HTML generado}} |

- Renderizado de las rutas nuevas: {{igual que `seo.rendering` · cambio (→ ADR)}}
- Imagen para compartir: {{general · generada por página desde la tarjeta del sistema (herramienta → ADR) · propia (ruta, 1200×630)}}
- Brechas `SE` que atiende: {{SE1.a dentro · SE1.b fuera → objetivo N · ninguna}}
<!-- endif -->

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
