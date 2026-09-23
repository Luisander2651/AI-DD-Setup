---
name: "init"
description: "Inicializa un proyecto para desarrollo guiado por IA (spec-driven): usar con /init o al preparar un repo nuevo o existente con AGENTS.md, constitución, arquitectura, despliegue, specs y plantillas."
---

# /init — Inicialización de proyecto AI-Driven

Prepara un repositorio para trabajar con el flujo:

```
/init → /specify → /plan → /tasks → /implement → /review → /release
```

Al terminar, el repositorio tiene una fuente de verdad (constitución, arquitectura, specs) que
todos los comandos posteriores leen y respetan.

**Versión del paquete de skills:** `1.3.1` (se escribe en `.ai/project.yaml → skills_version`).

## Argumentos

| Argumento | Efecto |
|---|---|
| `--type <frontend\|backend\|fullstack\|monorepo\|library>` | Omite la pregunta de tipo de proyecto |
| `--force` | Permite sobrescribir archivos existentes (siempre mostrando diff antes) |
| `--no-explore` | En brownfield, omite los subagentes y solo entrevista |
| `--dry-run` | Muestra qué archivos se crearían sin escribirlos |

## Reglas generales

- **Nunca inventes.** Lo que no se sepa por el código o por el usuario se pregunta o se marca como `TODO(init):`.
- **Nunca sobrescribas en silencio.** Si un archivo existe, sigue la política de la Fase 0.
- **No hagas commit ni push.** El usuario revisa y confirma.
- **Nunca despliegues.** `/init` documenta cómo se despliega; desplegar es trabajo de `/release`,
  y a producción solo con aprobación humana explícita.
- `AGENTS.md` es un **índice corto** (objetivo: < 150 líneas). El detalle vive en `docs/`.
- Todo contenido inferido de código lleva `status: inferred` y requiere revisión humana.
- Escribe los documentos en el idioma que use el usuario.
---

## Fase 0 — Detección

1. **¿Ya inicializado?** Busca `.ai/project.yaml`, `AGENTS.md`, `docs/constitution.md`.
   - Si existe `.ai/project.yaml`: el proyecto ya fue inicializado. Pregunta si quiere
     **(a)** re-sincronizar (actualizar arquitectura, specs, inventario y `docs/templates/` si
     `skills_version` es anterior, mostrando diff; sin tocar la constitución),
     **(b)** reiniciar con `--force`, o **(c)** cancelar.
   - Si existe `AGENTS.md` o `CLAUDE.md` sin `.ai/project.yaml`: léelos y trátalos como **insumo**
     de la entrevista; al final propone un merge con diff, no un reemplazo.
2. **¿Greenfield o brownfield?** Es brownfield si se cumple **al menos una**:
   - Existe un manifiesto: `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`,
     `Cargo.toml`, `pom.xml`, `build.gradle*`, `composer.json`, `Gemfile`, `*.csproj`, `pubspec.yaml`.
   - Hay más de ~10 archivos de código fuente fuera de carpetas de configuración.
   - `git rev-list --count HEAD` > 5.
   Si las señales son contradictorias (p. ej. manifiesto vacío, repo con solo un README), pregunta.
3. **Tipo de proyecto** (si no vino `--type`): en brownfield infiérelo y pide confirmación; en
   greenfield pregúntalo. Señales:
   - Frontend: `react`, `vue`, `svelte`, `angular`, `next`, `vite`, carpetas `components/`, `pages/`.
   - Backend: `express`, `fastapi`, `django`, `spring`, `gin`, `nestjs`, carpetas `routes/`, `controllers/`, `migrations/`.
   - Fullstack: señales de ambos en un mismo paquete, o meta-frameworks con servidor (Next con API routes, Remix, Nuxt server, Laravel con vistas).
   - Monorepo: `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, `workspaces` en `package.json`, varios manifiestos. En monorepo, registra el tipo **por paquete**.
   - Library: sin punto de entrada de app, con `exports`/`main` publicable o `[project]` sin servidor.
Informa en una línea qué detectaste antes de continuar.

---

## Fase 1 — Exploración (solo brownfield)

Omitir con `--no-explore` o en greenfield.

Lanza **en paralelo** cinco subagentes de solo lectura (tipo `Explore` si existe). Los prompts
exactos están en `references/explore-agents.md`:

| Subagente | Produce |
|---|---|
| A. Arquitectura | Capas, módulos, dependencias, flujo de datos, integraciones externas, despliegue |
| B. Dominio y features | Inventario de features con evidencia (rutas, archivos, tests) |
| C. Convenciones | Estilo, naming, estructura, patrones, lint/format, commits |
| D. Tooling, calidad y despliegue | Comandos build/test/lint/dev, CI, cobertura, variables de entorno, pipelines de deploy, entornos, rollback |
| E. Seguridad | Autenticación y autorización, datos sensibles, puntos de entrada, manejo de secretos, herramientas de seguridad existentes, riesgos evidentes |

Cada subagente devuelve un informe estructurado con **evidencia** (rutas de archivo) y un nivel de
confianza (`alta`/`media`/`baja`) por hallazgo. No generan documentos: solo informan.
Si el entorno no permite subagentes, ejecuta las cinco exploraciones tú mismo en secuencia con
los mismos prompts.

Después, **consolida**:
- Unifica el inventario de features (subagente B) y deduplica.
- Lista contradicciones entre informes y lo que no se pudo determinar → pasa a la entrevista.
- Si el inventario tiene más de 15 features, agrúpalas por dominio y pregunta al usuario cuáles
  documentar ahora; el resto queda listado en `docs/specs/README.md` como pendiente.
---

## Fase 2 — Entrevista

Sigue `references/interview.md`. Principios:
- Pregunta solo lo que **no** sepas. En brownfield, presenta lo inferido y pide confirmación.
- Usa preguntas de opción múltiple cuando sea posible, máximo 4 por ronda, máximo 4 rondas.
- Si el usuario no está disponible (sesión desatendida), toma la opción más conservadora,
  márcala como `TODO(init): confirmar` y continúa.
Bloques obligatorios:
1. Propósito del proyecto y usuarios objetivo.
2. Tipo de proyecto y stack (confirmar o definir).
3. Principios innegociables (proponer un borrador según el tipo; el usuario edita).
4. Estrategia de testing y definición de "terminado".
5. Etapa actual y próximos objetivos (→ roadmap).
6. Despliegue: entornos, plataforma, quién aprueba producción y cómo se revierte
   (→ `docs/deployment.md`). En prototipos sin despliegue aún, registra `deploy.strategy: none`
   y marca la sección como `TODO(init)`.
7. Seguridad: clasificación de datos, modelo de autenticación y autorización, nivel ASVS
   objetivo y herramientas de seguridad (→ `docs/security.md`).
---

## Fase 3 — Generación

Genera en este orden, usando las plantillas de `templates/` (carpeta junto a este `SKILL.md`). Sustituye cada `{{placeholder}}`; lo que quede sin dato se convierte
en `TODO(init): …`. Elimina las secciones marcadas `<!-- if type=… -->` que no apliquen al tipo.

1. `.ai/project.yaml` ← `templates/project.yaml`
2. `docs/constitution.md` ← `templates/constitution.md`
3. `docs/architecture.md` ← `templates/architecture.md`
   - Greenfield: arquitectura **propuesta**, marcada `status: proposed`.
   - Brownfield: arquitectura **observada**, `status: inferred`, con evidencia.
4. `docs/adr/0001-registro-de-decisiones.md` ← `templates/adr.md` (ADR inicial *"Registrar decisiones arquitectónicas mediante ADRs"*, `status: accepted`).
   En brownfield, crea ADRs adicionales solo para decisiones evidentes (framework, base de datos).
5. `docs/specs/` (solo brownfield):
   - `docs/specs/README.md` con el inventario completo y estado de cada spec.
   - Por cada feature seleccionada: `docs/specs/NNN-<slug>/spec.md` ← `templates/spec.md`,
     con `status: inferred`. Documenta lo que el código **hace**, no lo que debería hacer.
     Discrepancias, bugs aparentes y deuda van en la sección "Observaciones".
6. `docs/deployment.md` ← `templates/deployment.md`
   - Greenfield: `status: proposed` con la estrategia acordada en la entrevista.
   - Brownfield: `status: inferred`, a partir de pipelines, Dockerfiles, IaC y scripts reales.
   - Si no hay procedimiento de rollback conocido, déjalo como `TODO(init)` y repórtalo como
     riesgo en el resumen: es el hueco más peligroso del documento.
7. `docs/security.md` ← `templates/security.md`
   - Greenfield: `status: proposed`; propone herramientas según el stack (secretos, SAST, SCA,
     contenedores) sin instalarlas.
   - Brownfield: `status: inferred`, a partir del subagente E.
   - Registra la edición vigente del OWASP Top 10 en "Referencias".
8. `docs/roadmap.md` ← `templates/roadmap.md`
9. `docs/templates/` ← copia `templates/spec.md`, `templates/plan.md`, `templates/tasks.md`,
   `templates/review.md` y `templates/adr.md` para que los usen las demás skills.
10. `.ai/bin/aidd.py` ← copia de `../../scripts/aidd.py` (validadores; así CI no depende del
    plugin). En re-sincronización, reemplázalo si su `--version` es anterior.
11. **CI (opcional, pregunta):** si el proyecto usa GitHub, propone
    `.github/workflows/ai-dd.yml` ← `templates/ci/github-actions-aidd.yml`, rellenado con los
    comandos de `AGENTS.md` y `security.tools`; quita los pasos de herramientas no configuradas.
    Es una ruta protegida: créala solo con confirmación explícita. Si usa otra plataforma de CI,
    describe los pasos equivalentes en `docs/deployment.md` en lugar de crear el archivo.
12. `CHANGELOG.md` ← `templates/CHANGELOG.md` (solo si no existe; si existe, respeta su formato).
13. `AGENTS.md` ← `templates/AGENTS.md` (se escribe al final porque enlaza todo lo anterior).
14. `CLAUDE.md` ← `templates/CLAUDE.md` (si no existe; si existe, añade `@AGENTS.md` al inicio).
### Secciones condicionales por tipo

Aplica según `project.type` (en monorepo, por paquete):

| Tipo | Arquitectura incluye | Constitución propone | Skills habilitadas |
|---|---|---|---|
| frontend | Componentes, estado, routing, design tokens, accesibilidad | WCAG AA, componentes con tests, sin lógica de negocio en vistas, preview por PR | `design` |
| backend | API (contratos), modelo de datos, migraciones, observabilidad, seguridad | Contrato de API antes de implementar, migraciones reversibles y compatibles con la versión anterior, logs estructurados, health check | — |
| fullstack | Ambas + **contrato entre capas** (tipos compartidos, versionado de API) | Unión de ambas + el contrato es la fuente de verdad entre capas | `design` |
| library | API pública, compatibilidad, versionado semántico | SemVer estricto, API pública documentada y testeada, publicación solo desde CI con tag | — |

Las skills no se cargan ni descargan desde aquí: se registran en `.ai/project.yaml → skills.enabled`.
Cada skill condicional debe comprobar ese archivo al activarse (ver `../../shared/contract.md`).

---

## Fase 4 — Verificación

1. **Instalación:** antes de instalar dependencias, pide confirmación al usuario. En brownfield,
   pregunta si el repositorio es suyo o de confianza: instalar ejecuta scripts de ciclo de vida
   de las dependencias (`postinstall`, etc.) con los permisos del usuario. Si no es de confianza,
   usa el modo sin scripts del gestor (p. ej. `npm ci --ignore-scripts`, `pnpm install
   --ignore-scripts`) o no instales, y registra la limitación.
   Después ejecuta los comandos declarados en `AGENTS.md` (lint, test, build) con timeout
   razonable. **No** ejecutes comandos de despliegue, migraciones sobre bases reales ni nada que
   escriba fuera del repo. Registra el resultado en `.ai/project.yaml → verification`.
   Si un comando falla, no lo borres: márcalo con `# ⚠ falló en /init: <motivo breve>`.
2. Comprueba que cada enlace relativo en `AGENTS.md` apunta a un archivo existente.
3. Comprueba que `AGENTS.md` no supera ~150 líneas; si lo hace, mueve detalle a `docs/`.
4. Comprueba que no quedan `{{placeholders}}` sin sustituir (excepto en `docs/templates/`, que
   los conserva a propósito).
5. En brownfield, ejecuta `python .ai/bin/aidd.py validate` (o `python3`) sobre las specs
   inferidas y corrige los errores de formato. Si Python no está disponible, avisa: los hooks y
   validadores del plugin lo necesitan (3.8+).
6. Explica al usuario el modo `workflow.enforcement` (por defecto `warn`: el hook pide aprobación
   antes de editar código sin spec activa, tocar rutas protegidas o añadir dependencias).
---

## Fase 5 — Resumen

Entrega al usuario, sin recapitular los pasos:
- Lista de archivos creados/modificados.
- Qué requiere revisión humana (todo lo `inferred`, `proposed` y cada `TODO(init)`), con conteo.
- Resultado de la verificación de comandos.
- Estado de `docs/deployment.md`, destacando si falta el procedimiento de rollback.
- Estado de `docs/security.md`: herramientas configuradas o pendientes, y riesgos evidentes
  detectados en brownfield (sin detallar vectores de explotación).
- Siguiente paso sugerido: revisar y aprobar `docs/constitution.md`, luego `/specify` para la
  primera feature.

---

## Contrato con las demás skills

Las reglas que comparten todas las skills del flujo (estados, numeración, puertas de
aprobación) viven en `../../shared/contract.md`. Léelo antes de generar y respétalo.
