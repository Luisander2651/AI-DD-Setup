# ai-dd — AI-Driven Development

Plugin de skills para desarrollar software con agentes de IA de forma **guiada por
especificaciones**: cada cambio pasa por una spec aprobada, un plan que respeta la constitución
del proyecto, tareas verificables, revisión independiente y un release con aprobación humana.

```
/init → /specify → /plan → /tasks → /analyze → /implement → /review → /release
```

## Skills

| Skill | Qué hace | Produce |
|---|---|---|
| `init` | Inicializa un proyecto nuevo o existente: detecta stack y metodologías de agentes en competencia, explora el código con 6 subagentes, entrevista y genera la documentación base. `--upgrade` pone al día un proyecto con la versión instalada del plugin. | `AGENTS.md`, `.ai/project.yaml`, `docs/constitution.md`, `architecture.md`, `deployment.md`, `security.md`, `observability.md`, `roadmap.md`, plantillas |
| `specify` | Convierte una idea en spec: qué y por qué, sin tecnología, con casos de abuso. | `docs/specs/NNN-slug/spec.md` |
| `clarify` | Encuentra las ambigüedades de mayor impacto en una spec en borrador y las resuelve con preguntas. | `spec.md` actualizada |
| `plan` | Diseña el cómo: contratos, modelo de amenazas, trazabilidad, rollout y Constitution Check. | `plan.md`, ADRs |
| `tasks` | Divide el plan en tareas pequeñas y verificables, con cobertura de criterios y amenazas. | `tasks.md` |
| `analyze` | Verificación independiente de consistencia entre spec, plan, tareas y constitución; puerta antes de implementar. | `analysis.md` (pass/fail) |
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
- **Reglas ejecutables.** Un validador determinista revisa los artefactos y un hook del plugin
  hace cumplir el flujo mientras el agente trabaja.
- **Presente no es lo mismo que en uso.** Una herramienta instalada (logs, escáneres, métricas)
  no cuenta como capacidad cubierta hasta que el código o el pipeline la ejercitan.
- **Trazabilidad operativa.** Registro de auditoría de accesos a datos sensibles, correlación por
  petición y logs sin datos personales, desde la spec hasta la verificación post-deploy.
- **El agente también es una superficie de ataque.** Contenido de terceros como dato,
  verificación de dependencias nuevas (slopsquatting), rutas y comandos protegidos.

## Validador y guardia

- `python .ai/bin/aidd.py validate [docs/specs/NNN-slug]` — revisa formato y consistencia de
  spec, plan, tareas, análisis y review (estados, criterios, trazabilidad, cobertura, ciclos).
- `python .ai/bin/aidd.py status` — estado de cada spec y siguiente paso.
- **Hook `PreToolUse`** (`hooks/hooks.json`): en proyectos con `.ai/project.yaml`, según
  `workflow.enforcement`:
  - `warn` (por defecto): pide aprobación antes de editar código sin spec activa, tocar rutas
    protegidas, añadir dependencias o ejecutar comandos peligrosos.
  - `block`: bloquea las ediciones; los comandos peligrosos siguen pidiendo aprobación.
  - `off`: desactivado. `AIDD_ALLOW=1` en el entorno lo desactiva puntualmente.
  - Si el cliente no soporta la decisión "preguntar" de los hooks, usa `block`.
  - Un error interno del hook nunca bloquea: se ignora y se informa.

**Requisito:** Python 3.8+ disponible como `python3`, `python` o `py` (solo biblioteca estándar).
El hook prueba cada uno y usa el primero que realmente ejecute Python, así que el acceso directo
de Microsoft Store en Windows no lo rompe. Sin ningún Python válido, el hook no hace nada.

## Estructura del repositorio

```
.claude-plugin/
  plugin.json          # manifiesto (la versión aquí = skills_version de los proyectos)
  marketplace.json     # permite instalar el plugin desde este repo
hooks/hooks.json       # guardia PreToolUse
scripts/aidd.py        # validate · status · hash · hook (se copia a .ai/bin/ en cada proyecto)
shared/
  contract.md          # reglas comunes: estados, numeración, puertas de aprobación
  security-checklist.md  # seguridad del código (OWASP por temas)
  agent-security.md    # seguridad del proceso con agentes
skills/
  init/                # SKILL.md + references/ + templates/
  specify/ clarify/ plan/ tasks/ analyze/ implement/ review/ release/
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
3. Si cambias `scripts/aidd.py`, sube su `VERSION` y pruébalo con specs válidas e inválidas.
4. Prueba el flujo completo en un proyecto nuevo y en uno existente antes de publicar.
5. Los proyectos inicializados con una versión anterior se actualizan con `/ai-dd:init --upgrade`:
   reemplaza el validador y las plantillas cambiadas, añade claves y documentos nuevos y propone
   (sin aplicar) enmiendas a la constitución.
