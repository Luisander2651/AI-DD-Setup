---
status: {{proposed|inferred|approved}}
updated: {{date}}
---

# Seguridad de {{project_name}}

## Referencias
- OWASP Top 10: edición {{año}} (la vigente al inicializar; actualizar al cambiar de edición)
- Nivel ASVS objetivo: {{1|2|3}}
- Adicionales: {{API Security Top 10 · Top 10 para LLM · MASVS · ninguno}}
- Compliance: {{GDPR · HIPAA · PCI DSS · ninguno}}

## Clasificación de datos
| Dato | Clasificación | Dónde vive | Protección |
|---|---|---|---|
| {{correo de usuario}} | {{pública · interna · confidencial · restringida}} | {{…}} | {{cifrado, acceso}} |

## Autenticación y autorización
- Mecanismo de autenticación: {{sesión, JWT, OAuth/OIDC, proveedor}}
- Modelo de autorización: {{roles, permisos, por recurso}}
- Dónde se aplica: {{middleware, guardas, políticas}}

## Superficie de ataque
| Punto de entrada | Tipo | Autenticado | Notas |
|---|---|---|---|
| {{/api/*}} | {{HTTP público}} | {{sí/no}} | |

## Manejo de secretos
- Dónde se guardan: {{gestor de secretos por entorno}}
- Rotación: {{…}}

## Herramientas
| Tipo | Herramienta | Comando | Cuándo corre |
|---|---|---|---|
| Secretos | {{gitleaks}} | {{gitleaks detect --no-banner}} | /implement, CI |
| SAST | {{semgrep}} | {{semgrep scan --config auto --error}} | /implement (archivos tocados), /review |
| SCA (dependencias) | {{npm audit / pip-audit / osv-scanner}} | {{…}} | /review, /release |
| Contenedores / IaC | {{trivy}} | {{trivy fs .}} | /review, /release |
| DAST | {{OWASP ZAP baseline}} | {{…}} | /release, solo contra staging |

## Permisos del agente
Reglas base en `shared/agent-security.md` del plugin. Específicas de este proyecto:
- Antigüedad mínima de paquetes nuevos: {{7}} días
- Rutas protegidas adicionales: {{…}}
- Servicios externos aprobados para enviar código o datos: {{ninguno}}
- Dominios de red que el agente necesita: {{registros de paquetes, …}}

## Excepciones aceptadas
| ID | Hallazgo | Severidad | Motivo | Aprobado por | Vence |
|---|---|---|---|---|---|

## Riesgos conocidos
<!-- Cada riesgo con ID `RS<n>` y cada corrección con ID `RS<n>.<letra>`. Los objetivos del
     roadmap y las specs citan estos IDs y declaran cada corrección como dentro o fuera de su
     alcance (ver shared/contract.md, "Cobertura de riesgos"). Estados de una corrección:
     pendiente · en curso (spec NNN) · mitigada (vX.Y.Z) · aceptada (excepción EX<n>).
     Un riesgo solo está mitigado cuando todas sus correcciones están mitigadas o aceptadas. -->

### RS1 · {{Alta}} — {{título}} ({{categoría OWASP}})
{{descripción e impacto}}

Correcciones:
- RS1.a {{corrección}} — estado: pendiente
- RS1.b {{corrección}} — estado: pendiente
