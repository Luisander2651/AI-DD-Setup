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
| `init` | Inicializa un proyecto nuevo o existente: detecta stack y metodologías de agentes en competencia, explora el código con 6 subagentes (7 si documenta el diseño existente) o crea el proyecto base y audita los valores por defecto de la plantilla (nuevo), entrevista y genera la documentación base. Con interfaz: opciones de diseño en HTML (nuevo) o el sistema de diseño actual documentado, si el usuario lo acepta (existente). `--upgrade` pone al día un proyecto con la versión instalada del plugin; `--upgrade --redo-design` vuelve a documentar el diseño existente (todas las vistas con capturas reales) sin perder la deuda ya citada. | `AGENTS.md`, `.ai/project.yaml`, `docs/constitution.md`, `architecture.md`, `deployment.md`, `security.md`, `observability.md`, `roadmap.md`, `docs/design/` (con interfaz), plantillas |
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
- **Probar antes de planear.** Lo que el plan da por hecho de una herramienta o framework nuevo se
  comprueba con una prueba de concepto; los valores por defecto de una plantilla se auditan contra
  la constitución.

## Validador y guardia

- `python .ai/bin/aidd.py validate [docs/specs/NNN-slug]` — revisa formato y consistencia de
  spec, plan, tareas, análisis y review (estados, criterios, trazabilidad, cobertura, ciclos).
  Los avisos de specs ya cerradas salen resumidos como heredados; `--all` los muestra.
- `python .ai/bin/aidd.py status` — estado de cada spec y siguiente paso (con las rondas de `/analyze` y `/review`).
- `snapshot` / `changes [--since REF]` — copia y diff para `/analyze` delta.
- `templates [--yaml]` — huellas de `docs/templates/`: `--upgrade` sabe cuáles personalizó el usuario.
- `rotate` / `history [--write] [--migrate]` — archivan e indexan rondas y versiones en
  `docs/specs/NNN/history/` (nunca se borran).
- `review-pack` — paquete compartido de `/review`: diff de código filtrado desde `impl_base`,
  alcance frente a las tareas y contexto mínimo para cada revisor.
- **Hook `PreToolUse`** (`hooks/hooks.json`): en proyectos con `.ai/project.yaml`, según
  `workflow.enforcement`:
  - `warn` (por defecto): pide aprobación antes de editar código sin spec activa, tocar rutas
    protegidas, añadir dependencias (por comando o editando el manifiesto) o ejecutar comandos
    peligrosos. `AGENTS.md` y `CLAUDE.md` siempre piden aprobación.
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
scripts/aidd.py        # validate · status · hash · templates · snapshot · changes · rotate · history · review-pack · hook (se copia a .ai/bin/ en cada proyecto)
shared/
  contract.md          # reglas comunes: estados, numeración, puertas de aprobación
  security-checklist.md  # seguridad del código (OWASP por temas)
  agent-security.md    # seguridad del proceso con agentes
skills/
  init/                # SKILL.md + references/ + templates/
  specify/ clarify/ plan/ tasks/ analyze/ implement/ review/ release/
```

## Instalación

Tres caminos (revisa la documentación de tu cliente: los comandos pueden cambiar). El marketplace
de este repo se llama `ai-dd` y el plugin también, así que su identificador es `ai-dd@ai-dd`.

- **Claude Code, desde el repo (recomendado):** dentro de una sesión,
  `/plugin marketplace add Luisander2651/AI-DD-Setup` y después `/plugin install ai-dd@ai-dd`
  (elige el alcance: usuario, proyecto o local). Desde la terminal:
  `claude plugin marketplace add Luisander2651/AI-DD-Setup` y `claude plugin install ai-dd@ai-dd`.
- **Claude Code, para probar en local:** arrancar con el directorio del plugin, p. ej.
  `claude --plugin-dir E:\AI-DD-Setup`. Solo dura esa sesión y no se instala.
- **Claude (app de escritorio, chat y Cowork):** en **Customize > Plugins**, **Add > Add marketplace**
  con `Luisander2651/AI-DD-Setup` (recomendado: así recibe actualizaciones), o **Add > Upload plugin**
  con la carpeta empaquetada como `.zip` o `.plugin` (debe contener un solo `.claude-plugin/plugin.json`).

## Actualización

Cada versión sube `version` en `.claude-plugin/plugin.json` y se publica con push a `main`; después,
según cómo se instaló:

- **Claude Code, desde el repo:**
  - En una sesión: `/plugin` → pestaña **Marketplaces** → `ai-dd` → **Update marketplace** (refresca el
    catálogo y actualiza el plugin), o pestaña **Installed** → `ai-dd` → **Update now**.
  - Desde la terminal: `claude plugin marketplace update ai-dd` y `claude plugin update ai-dd@ai-dd`.
    Ojo: `claude plugin marketplace update` **sin nombre** solo refresca los catálogos y deja los
    plugins en su versión actual.
  - Activa la versión nueva con `/reload-plugins` o abriendo una sesión nueva, y compruébala con
    `claude plugin list` (línea `Version`).
  - Actualización automática: `/plugin` → **Marketplaces** → `ai-dd` → **Enable auto-update**. En un
    marketplace propio viene desactivada; con ella, Claude Code actualiza al iniciar sesión y avisa
    con `Plugin updated … Run /reload-plugins to apply`.
- **Claude Code, en local (`--plugin-dir`):** `git pull` en la carpeta del plugin y abre una sesión nueva.
- **Claude (app de escritorio), como marketplace:** **Customize > Plugins** → el marketplace → **Check for
  updates** trae la última versión del repo; activa **Sync automatically** para que lleguen solas. Las sesiones de Claude Code con la misma cuenta lo reciben como plugin sincronizado
  (`/reload-plugins` para cargarlo).
- **Claude (app de escritorio), subido como archivo:** no se actualiza solo. Empaqueta la versión nueva y
  súbela otra vez con **Add > Upload plugin**; si queda la anterior, quítala desde su menú → **Remove**.
  Para no repetir esto en cada versión, cámbialo a la opción de marketplace.

**Después, en cada proyecto** inicializado con una versión anterior: `/ai-dd:init --upgrade` (pone al
día el validador, las plantillas y `.ai/project.yaml`; ver "Mantenimiento" → 6).

## Dependencias

- **Python 3.8+** para el validador (`.ai/bin/aidd.py`) y el hook.
- **Skill `design`** (opcional; crea un canvas Design a partir de un brief): si la sesión la
  ofrece, `/init` y `/plan` generan con ella las opciones de diseño y enlazan el canvas. Sin ella,
  las opciones se generan igual en HTML con `skills/init/templates/design/option.html`. El HTML es
  siempre el entregable: queda en el repo y se abre sin red.
- **Plugin oficial `design` de Anthropic** (opcional, recomendado en proyectos con interfaz:
  `frontend`, `fullstack`, `mobile`). Por ahora el flujo **depende de él** para la parte de diseño:
  `/init` lo registra en `skills.enabled` si está instalado, `/plan` deja la nota de revisarlo con
  `design:design-handoff` y `/review` añade `design:accessibility-review` y `design:design-critique`.
  Si no está instalado, el flujo sigue con su revisión propia de accesibilidad. En una versión
  posterior este plugin tendrá su propia skill de diseño, construida a partir de cómo se usa esta
  (ver `docs/analisis-brechas.md` → hoja de ruta).

## Mantenimiento

1. Toda regla que afecte a más de una skill va en `shared/contract.md`, no duplicada.
2. Al cambiar una plantilla o el contrato, sube la versión en `plugin.json` **y** en
   `skills/init/SKILL.md` (`Versión del paquete de skills`), y registra el cambio en `CHANGELOG.md`.
3. Si cambias `scripts/aidd.py`, sube su `VERSION` y ejecuta `python tests/run.py` (también corre en
   CI, en Linux y Windows). Los proyectos de `tests/fixtures/` son a propósito distintos entre sí:
   librería Python en inglés, app Ionic en español, CLI en Go, monorepo.
4. **Contra el sobreajuste:** un hallazgo de un proyecto real se generaliza solo si se puede
   formular sin su stack y queda cubierto por un caso en `tests/fixtures/` de **otro** tipo o
   idioma. Si no, se queda como ejemplo en la documentación, no como regla.
5. Prueba el flujo completo en un proyecto nuevo y en uno existente antes de publicar.
6. Los proyectos inicializados con una versión anterior se actualizan con `/ai-dd:init --upgrade`:
   reemplaza el validador y las plantillas cambiadas, añade claves y documentos nuevos y propone
   (sin aplicar) enmiendas a la constitución.
