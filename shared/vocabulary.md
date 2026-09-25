# Vocabulario canónico de los artefactos

Los documentos del flujo se escriben en el idioma del proyecto (`.ai/project.yaml → language`).
Los **títulos de sección, IDs y marcadores** que lee el validador (`aidd.py`) tienen una forma
canónica en español y otra en inglés; usa exactamente una de ellas. Si el proyecto usa otro idioma,
escribe el contenido en ese idioma y conserva los títulos y marcadores en inglés.

## Títulos de sección (`## …`)

| Español | English | Dónde |
|---|---|---|
| Problema | Problem | spec |
| Criterios de aceptación | Acceptance criteria | spec |
| Fuera de alcance | Out of scope | spec |
| Seguridad y privacidad | Security and privacy | spec |
| Auditoría | Audit | spec |
| Cobertura de riesgos | Risk coverage | spec |
| Historial | History | spec |
| Constitution Check | Constitution Check | plan, tasks |
| Trazabilidad | Traceability | plan |
| Modelo de amenazas | Threat model | plan |
| Rollout | Rollout | plan |
| Observabilidad | Observability | plan |
| Aceptados | Accepted | analysis |
| Aceptados sin tarea | Accepted without task | review |

## IDs y marcadores

| Español | English | Uso |
|---|---|---|
| `CA1` | `AC1` | criterio de aceptación |
| `(abuso)` | `(abuse)` | criterio de caso de abuso |
| `[NECESITA ACLARACIÓN]` | `[NEEDS CLARIFICATION]` | duda abierta en la spec |
| `HOY NO SE CUMPLE` | `NOT MET TODAY` | criterio de spec inferida que el código no cumple |
| `No aplica` | `Not applicable` | sección de seguridad sin datos sensibles |
| `hecho cuando:` | `done when:` | tarea |
| `cubre:` | `covers:` | tarea |
| `depende:` | `depends on:` | tarea |
| `- nota:` | `- note:` | nota bajo una tarea |
| `dentro` / `fuera` | `in` / `out` | columna Alcance de "Cobertura de riesgos" |
| `parcialmente` | `partially` | Problema que atiende un riesgo en parte |
| `mitigado` | `mitigated` | estado de un riesgo |
| `❌ aceptado` | `❌ accepted` | excepción de la constitución |
| `- **A3** → nota de T012: …` | `- **A3** → note on T012: …` | aceptado de `/analyze` |

Los IDs de tarea (`T001`), riesgo (`RS1.a`, `OB2`, `RD3`), amenaza (`TM1`), principio (`P1`),
hallazgo (`A1`, `R1`) y las claves del frontmatter (`status`, `round`, `verdict`…) no se traducen.
