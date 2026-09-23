# Análisis de brechas — ai-dd v1.3.0

Fecha: 2026-09-22. Objetivo: un flujo completo de desarrollo asistido por IA que produzca software
**seguro, escalable y mantenible**. Se contrasta el plugin con prácticas actuales de
spec-driven development (GitHub Spec Kit, guías de SDD 2026) y con los modelos de amenazas
publicados para agentes de código.

Prioridades: **P0** defecto del plugin, corregir ya · **P1** necesario para un flujo completo ·
**P2** necesario para escalar a equipos o repos grandes · **P3** mejora.

---

## 1. Defectos e inconsistencias del plugin actual

| # | Prioridad | Hallazgo | Corrección propuesta |
|---|---|---|---|
| 1.1 | P0 | En `release`, con `deploy.strategy: none` se ejecutan "Pasos 1–3 y 8": se salta el Paso 7 (cierre), así que la spec **nunca pasa a `released`**. | Ejecutar Pasos 1–3, 7 y 8. |
| 1.2 | P0 | `init` Fase 4 ejecuta el comando de **instalar** en repos existentes. En un repo no confiable eso corre scripts de ciclo de vida (`postinstall`, etc.) con permisos del usuario. | Pedir confirmación antes de instalar; preferir modos sin scripts (`--ignore-scripts` o equivalente) y avisar si el repo no es del usuario. |
| 1.3 | P1 | Numeración de specs "siguiente número libre" es local: dos ramas o dos personas crean la misma `NNN` en paralelo. | Reservar el número en la rama principal (fila en `docs/specs/README.md` mergeada antes) o usar un ID sin colisión (fecha + slug) y numerar al aprobar. |
| 1.4 | P1 | **Auto-evaluación**: el mismo agente que escribe el plan hace su Constitution Check, y no hay verificación independiente hasta `/review` (cuando corregir es caro). | Nuevo paso `/analyze` con subagente de contexto limpio antes de `/implement` (ver 3.2). |
| 1.5 | P1 | Las reglas viven solo en prosa: nada **impide** editar código sin spec aprobada, saltar estados o dejar tablas de cobertura incompletas. Un agente distraído o con contexto comprimido puede saltárselas. | Validaciones deterministas (scripts) + hooks del plugin + chequeo en CI (ver 3.1). |
| 1.6 | P2 | El contrato dice "todas leen `project.yaml` y la constitución", pero no `docs/security.md`, que ahora es fuente de verdad. | Añadirlo a la lista de lecturas obligatorias. |
| 1.7 | P3 | `review` añade tareas "≤ T089"; si una spec ya usó muchas, no hay regla de desborde. | Si no quedan números, sugerir dividir la spec o crear una spec de seguimiento. |

---

## 2. Seguro

### 2.1 Seguridad del propio agente — P1 (la brecha más importante)
El flujo protege el **código que se produce**, pero no el **proceso** que lo produce. Los riesgos
propios del desarrollo con agentes no están cubiertos:

- **Inyección de prompt indirecta:** el agente lee contenido no controlado (issues, README de
  dependencias, mensajes de error, archivos vendoreados, páginas web) que puede contener
  instrucciones. Regla: todo contenido de terceros es dato, nunca instrucción; las skills que
  leen issues o la web deben decirlo explícitamente.
- **Dependencias alucinadas (slopsquatting / "HalluSquatting"):** el modelo sugiere paquetes que
  no existen y un atacante los registra. Regla en `plan` e `implement`: toda dependencia nueva se
  verifica (existe en el registro oficial, antigüedad mínima, mantenedores, descargas, licencia)
  antes de instalarse, y se instala con lockfile y versión fijada; considerar una antigüedad
  mínima de publicación (p. ej. `minimumReleaseAge` en pnpm).
- **Permisos y sandbox:** documentar en `docs/security.md` qué puede hacer el agente: comandos
  permitidos, red restringida, prohibido escribir en `.git/hooks`, en workflows de CI o en
  archivos de configuración de herramientas sin aprobación, prohibido leer `.env` reales.
- **Código del agente como contribución no confiable:** CI obligatorio como segundo revisor y
  revisión humana en PR para todo cambio generado.

### 2.2 Cadena de suministro en el release — P1
- **SBOM** (CycloneDX o SPDX) generado en `release` y adjunto a la versión.
- **Licencias:** verificación de compatibilidad de licencias de dependencias nuevas.
- **Procedencia/firmas** de artefactos cuando la plataforma lo permita (SLSA como referencia).

### 2.3 Operación segura — P2
- `/security-audit` periódico del repo completo (no solo del diff), útil también en brownfield.
- Carril de **actualización de dependencias** (Renovate/Dependabot + `/review` ligero).
- **Respuesta a incidentes de seguridad**: cómo se reporta, quién decide, cómo se corrige
  (carril `hotfix`, ver 4.1) y registro en `docs/security.md`.
- **Privacidad:** retención y borrado de datos personales en `docs/security.md`.

---

## 3. Verificación y control del flujo

### 3.1 Reglas ejecutables ("gates as code") — P1
Añadir al plugin `scripts/` con validadores deterministas, invocables por las skills, por hooks
y por CI:
- `validate-spec`: frontmatter, estados válidos y transiciones permitidas, `CA` numerados, máximo
  3 `[NECESITA ACLARACIÓN]`, sección de seguridad presente.
- `validate-plan`: todos los principios en el Constitution Check, todos los `CA` y `TM#` en
  Trazabilidad.
- `validate-tasks`: formato de tarea, rangos T001–T089/T090–T099, `[P]` sin archivos compartidos,
  sin ciclos, tablas de cobertura completas.
- `status`: índice legible por máquina del estado de todas las specs (base para `/next`).
- **Hooks del plugin:** p. ej. advertir o bloquear ediciones de código fuente cuando no hay una
  spec en `approved` con `tasks.md` aprobado para la rama actual.
- **Plantilla de CI** que `init` puede proponer: validadores + tests + escáneres en cada PR.

### 3.2 `/analyze` — consistencia entre artefactos — P1
Antes de `/implement`, un subagente de contexto limpio verifica spec ↔ plan ↔ tasks ↔
constitución: requisitos sin tarea, tareas sin requisito, contradicciones, terminología
inconsistente, amenazas sin control. Equivale a `/speckit.analyze`.

### 3.3 `/clarify` — P1
Detectar ambigüedades de la spec con preguntas dirigidas antes de planear.

### 3.4 Calidad de tests — P2
- Umbral de cobertura en la constitución (por módulo cambiado, no global).
- **Mutation testing** opcional en `review` para módulos críticos: detecta tests que pasan con
  cualquier implementación.
- Política de tests inestables (flaky): cuarentena con tarea de corrección, nunca `skip` silencioso.

---

## 4. Mantenible

### 4.1 Carriles para trabajo que no es feature — P1
Hoy todo cambio exige spec + plan + tasks. Es excesivo para trabajo pequeño (limitación conocida de
SDD) y empuja a saltarse el flujo. Faltan carriles con proceso proporcional:

| Carril | Proceso | Cuándo |
|---|---|---|
| `/fix` (bug) | reproducir con test que falla → causa raíz → fix → review ligera | Bug con comportamiento esperado ya especificado |
| `/hotfix` | igual que `/fix` + release acelerado, con la misma puerta humana a producción | Incidente en producción |
| `/refactor` | tests de caracterización primero → cambio sin alterar comportamiento → review | Deuda técnica, sin cambio funcional |
| `/chore` | tarea directa + validación | Dependencias, configuración, docs |

Criterio explícito de cuándo un cambio **debe** ir por el flujo completo (toca contratos, datos,
seguridad o más de N archivos).

### 4.2 Deriva entre documentos y código — P1
- `/sync`: detecta cambios hechos fuera del flujo (commits sin spec), specs `released` que ya no
  describen el código, `architecture.md` desactualizado, specs `inferred` envejecidas; propone
  actualizaciones o specs nuevas.
- Recomendación de ejecutarlo antes de cada `/plan` en zonas tocadas y de forma periódica.

### 4.3 Gobierno de decisiones — P2
- `/amend` para la constitución: versionado, impacto en specs y planes abiertos.
- Registro de **deuda técnica** propio (`docs/tech-debt.md` con impacto, esfuerzo y prioridad) en
  lugar de la lista "Pendientes" del roadmap.
- Ciclo de vida de **feature flags**: fecha de expiración y tarea de limpieza obligatoria.
- Documentación para humanos: API docs y guías de usuario en las tareas T090–T091.

### 4.4 Orquestación — P2
- `/next`: lee el índice de estado (3.1) y propone o ejecuta el siguiente paso.
- `design` condicional para frontend y fullstack.

---

## 5. Escalable

### 5.1 Escalabilidad del software — P1
- **Requisitos no funcionales cuantificados** en la constitución y la spec: presupuestos de
  latencia, throughput esperado, tamaño de datos, SLO/SLI.
- En `plan`: sección de **capacidad y rendimiento** (consultas N+1, índices, caché, paginación,
  límites) y **observabilidad** (logs, métricas, trazas de la feature).
- En `release`: prueba de carga o de humo de rendimiento en staging cuando la spec tenga
  requisitos de rendimiento.
- **Funciones de aptitud arquitectónica:** reglas de dependencias entre capas verificadas por
  herramienta (p. ej. dependency-cruiser, ArchUnit, import-linter) en CI, para que la
  arquitectura documentada no sea solo prosa.

### 5.2 Escalar a equipos y agentes en paralelo — P2
- Una rama por spec; dueño de la spec en el frontmatter.
- Specs y planes revisados vía **PR** (el aprobado humano queda en el historial).
- Exportar tareas a issues del tracker (equivalente a `taskstoissues`).
- Resolución de conflictos cuando dos specs tocan los mismos módulos (detección en `/analyze`).

### 5.3 Escalar a repos grandes (context engineering) — P2
- `AGENTS.md` jerárquicos por paquete o módulo en monorepos, con el raíz como índice.
- Glosario de dominio en `docs/` referenciado desde las specs.
- Guía de presupuesto de contexto: qué leer siempre, qué leer bajo demanda.

---

## 6. Mantenimiento del plugin — P2
- **Evals del plugin:** 2 proyectos de referencia (uno nuevo, uno existente) y un conjunto de
  escenarios con resultado esperado; correrlos antes de cada versión (skill-creator permite
  ejecutar evals).
- Pruebas de los validadores de `scripts/`.
- Guía de modelo/esfuerzo por paso (p. ej. razonamiento alto en `plan` y `review`, menor en
  `tasks`) para controlar costo.

---

## 7. Hoja de ruta sugerida

| Versión | Contenido |
|---|---|
| 1.3.1 | Defectos 1.1, 1.2, 1.6, 1.7 |
| 1.4.0 | Seguridad del agente (2.1), validadores + hooks + plantilla de CI (3.1), `/analyze`, `/clarify` |
| 1.5.0 | Carriles `/fix`, `/hotfix`, `/refactor`, `/chore` (4.1) y `/sync` (4.2) |
| 1.6.0 | Escalabilidad (5.1): NFR cuantificados, capacidad y observabilidad en `plan`, carga en `release`, fitness functions |
| 1.7.0 | SBOM y licencias (2.2), `/amend`, deuda técnica, flags, `/next`, `design` |
| 2.0.0 | Equipos y repos grandes (5.2, 5.3), `/security-audit`, evals del plugin |

## Fuentes
- GitHub Spec Kit — https://github.com/github/spec-kit
- Allegro Tech, "Spec-Driven Development — best practices (so far)", 2026 —
  https://blog.allegro.tech/2026/06/spec-driven-development-best-practices.html
- Developers Digest, "Securing AI Coding Agents: A Practical Threat Model for 2026" —
  https://www.developersdigest.tech/blog/securing-ai-coding-agents
- The Hacker News, "New HalluSquatting Attack…", 2026 —
  https://thehackernews.com/2026/07/new-hallusquatting-attack-could-trick.html
- Cloud Security Alliance, nota de investigación sobre slopsquatting, 2026 —
  https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/04/CSA_research_note_slopsquatting-ai-supply-chain_20260419-csa-styled-1.pdf
