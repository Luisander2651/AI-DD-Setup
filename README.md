# ai-dd — AI-Driven Development

Plugin de skills para desarrollar software con agentes de IA de forma **guiada por
especificaciones**: cada cambio pasa por una spec aprobada, un plan que respeta la constitución
del proyecto, tareas verificables, revisión independiente y un release con aprobación humana.

```
/init → /specify → /plan → /tasks → /implement → /review → /release
```

## Skills

| Skill | Qué hace | Produce |
|---|---|---|
| `init` | Inicializa un proyecto nuevo o existente: detecta stack, entrevista y genera la documentación base. En proyectos existentes explora el código con subagentes. | `AGENTS.md`, `.ai/project.yaml`, `docs/constitution.md`, `architecture.md`, `deployment.md`, `security.md`, `roadmap.md`, plantillas |
| `specify` | Convierte una idea en spec: qué y por qué, sin tecnología, con casos de abuso. | `docs/specs/NNN-slug/spec.md` |
| `plan` | Diseña el cómo: contratos, modelo de amenazas, trazabilidad, rollout y Constitution Check. | `plan.md`, ADRs |
| `tasks` | Divide el plan en tareas pequeñas y verificables, con cobertura de criterios y amenazas. | `tasks.md` |
| `implement` | Ejecuta las tareas una a una, con tests primero y escaneo de seguridad. | código, `tasks.md` marcado |
| `review` | Revisión independiente con subagentes: spec, plan, constitución, seguridad OWASP y calidad. | `review.md` con veredicto |
| `release` | Versión, changelog, staging y producción **solo con aprobación explícita**; rollback guiado. | tag/PR, `CHANGELOG.md` |

Dentro de un plugin las skills se invocan con el prefijo del plugin (por ejemplo `/ai-dd:init`),
así que no chocan con comandos integrados como `/init`.

## Principios del flujo

- **La constitución manda.** Principios verificables; cada plan y cada review los evalúa uno a uno.
- **Nada se aprueba solo.** Specs, planes y tareas nacen en `draft`; pasa a `approved` solo con
  confirmación humana.
- **Trazabilidad completa.** Criterio de aceptación → cambio → test → tarea; lo mismo para cada
  amenaza del modelo de seguridad.
- **Seguridad desde el diseño.** Casos de abuso en la spec, STRIDE + OWASP en el plan, escaneo en
  la implementación, auditoría en la review y puerta de vulnerabilidades en el release.
- **Producción es humana.** Ningún deploy a producción sin confirmación explícita.

## Estructura del repositorio

```
.claude-plugin/
  plugin.json          # manifiesto (la versión aquí = skills_version de los proyectos)
  marketplace.json     # permite instalar el plugin desde este repo
shared/
  contract.md          # reglas comunes: estados, numeración, puertas de aprobación
  security-checklist.md
skills/
  init/                # SKILL.md + references/ + templates/
  specify/ plan/ tasks/ implement/ review/ release/
```

## Instalación

Opciones habituales (revisa la documentación de tu cliente, los comandos pueden cambiar):

- **Claude Code, para probar en local:** arrancar con el directorio del plugin, p. ej.
  `claude --plugin-dir E:\AI-DD-Setup`.
- **Claude Code, desde el repo:** añadir este repo como marketplace con `/plugin marketplace add`
  e instalar `ai-dd`.
- **Claude (app de escritorio):** empaquetar el directorio como archivo `.plugin` e instalarlo.

## Mantenimiento

1. Toda regla que afecte a más de una skill va en `shared/contract.md`, no duplicada.
2. Al cambiar una plantilla o el contrato, sube la versión en `plugin.json` **y** en
   `skills/init/SKILL.md` (`Versión del paquete de skills`), y registra el cambio en `CHANGELOG.md`.
3. Prueba el flujo completo en un proyecto nuevo y en uno existente antes de publicar.
4. Los proyectos inicializados con una versión anterior se actualizan con `/ai-dd:init` en modo
   re-sincronizar.
