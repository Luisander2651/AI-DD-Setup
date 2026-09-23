---
status: {{proposed|inferred|approved}}
updated: {{date}}
---

# Arquitectura de {{project_name}}

## Resumen
{{estilo arquitectónico y justificación en 3–5 frases}}

## Diagrama de componentes
```mermaid
flowchart LR
  {{componentes}}
```

## Módulos
| Módulo | Ruta | Responsabilidad | Depende de |
|---|---|---|---|

## Flujo principal
{{petición/interacción típica de punta a punta}}

## Datos
{{motor, ORM, entidades principales, migraciones}}

## Integraciones externas
{{servicios, APIs, auth}}

<!-- if type=frontend|fullstack -->
## Frontend
- Componentes y organización: {{…}}
- Estado: {{…}}
- Routing: {{…}}
- Design tokens / sistema de diseño: {{…}}
- Accesibilidad: {{objetivo, p. ej. WCAG 2.1 AA}}
<!-- endif -->

<!-- if type=backend|fullstack -->
## Backend
- Contratos de API: {{ruta al OpenAPI/GraphQL schema}}
- Autenticación y autorización: {{…}}
- Observabilidad: {{logs, métricas, trazas}}
- Seguridad: {{…}}
<!-- endif -->

<!-- if type=fullstack|monorepo -->
## Contrato entre capas
- Fuente de verdad: {{schema/tipos compartidos y su ubicación}}
- Versionado: {{…}}
- Cómo se regenera: {{comando}}
<!-- endif -->

<!-- if type=library -->
## API pública
- Superficie exportada: {{…}}
- Política de compatibilidad: SemVer; {{…}}
<!-- endif -->

## Despliegue
Resumen en 2–3 frases; el detalle vive en [deployment.md](deployment.md).

## Evidencia (solo si status=inferred)
| Afirmación | Archivos | Confianza |
|---|---|---|

## Deuda técnica y riesgos observados
- {{…}}
