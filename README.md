# ai-dd — AI-Driven Development

Plugin de skills para desarrollar software con agentes de IA de forma **guiada por
especificaciones**: cada cambio pasa por una spec aprobada, un plan que respeta la constitución
del proyecto, tareas verificables, revisión independiente y un release con aprobación humana.

```
/init → /specify → /plan → /tasks → /analyze → /implement → /review → /release
```

Para lo que no añade comportamiento hay **carriles ligeros** (`/fix`, `/refactor`, `/chore`) con
una ficha en `docs/changes/` en lugar de spec, plan y tareas (ver "Carriles").

## Skills

| Skill | Qué hace | Produce |
|---|---|---|
| `init` | Inicializa un proyecto nuevo o existente: detecta stack y metodologías de agentes en competencia, explora el código con 6 subagentes (uno más si documenta el diseño existente y otro si el sitio es público e indexable) o crea el proyecto base y audita los valores por defecto de la plantilla (nuevo), entrevista y genera la documentación base. Con interfaz: sistema de diseño aceptado por criterios (nuevo) o el actual documentado, si el usuario lo acepta (existente). `--upgrade` pone al día un proyecto con la versión instalada del plugin; `--upgrade --redo-design` vuelve a documentar el diseño existente (todas las vistas con capturas reales) sin perder la deuda ya citada; `--upgrade --redo-options` repite el ciclo de diseño con criterios nuevos cuando aún no hay sistema aprobado, archivando la ronda anterior; con `--only <eje> --base <cN>` ajusta solo la tipografía, el color, la forma, el fondo o el movimiento del aceptado (ver "Diseño"). | `AGENTS.md`, `.ai/project.yaml`, `docs/constitution.md`, `architecture.md`, `deployment.md`, `security.md`, `observability.md`, `roadmap.md`, `docs/design/` (con interfaz), `seo.md` (sitio indexable), plantillas |
| `specify` | Convierte una idea en spec: qué y por qué, sin tecnología, con casos de abuso. | `docs/specs/NNN-slug/spec.md` |
| `design-spec` | Diseño de interfaz por criterios: puertas, KPIs y rúbrica; genera un candidato tras otro, los mide en el navegador (`evaluate.mjs`), los puntúa un evaluador que no los diseñó y acepta el primero que supera el umbral. `system`: el sistema de diseño (o el existente documentado); lo llama `init`. `NNN`: cada spec con pantallas, antes de planear. `--fix`: refinado tras la revisión manual. | `docs/design/`, `docs/specs/NNN-slug/design.md` (acta) + `criterios.json` + candidatos en HTML |
| `seo` | SEO técnico de sitios públicos. `setup`: reglas del sitio; `audit`: auditoría sobre la build (y, con permiso, el sitio publicado) con brechas `SE` y propuestas para el roadmap; `verify`: comprobaciones en producción tras un despliegue. La llaman `init` y `release`. | `docs/seo.md` |
| `clarify` | Encuentra las ambigüedades de mayor impacto en una spec en borrador y las resuelve con preguntas. | `spec.md` actualizada |
| `plan` | Diseña el cómo: contratos, modelo de amenazas, trazabilidad, rollout y Constitution Check. | `plan.md`, ADRs |
| `tasks` | Divide el plan en tareas pequeñas y verificables, con cobertura de criterios y amenazas. | `tasks.md` |
| `analyze` | Verificación independiente de consistencia entre spec, plan, tareas y constitución; puerta antes de implementar. | `analysis.md` (pass/fail) |
| `implement` | Ejecuta las tareas una a una, con tests primero y escaneo de seguridad. | código, `tasks.md` marcado |
| `review` | Revisión independiente con subagentes: spec, plan, constitución, seguridad OWASP, calidad y, si aplica, accesibilidad y SEO técnico. | `review.md` con veredicto |
| `release` | Versión, changelog, staging y producción **solo con aprobación explícita**; rollback guiado. Incluye las fichas `done` de los carriles (`--changes` para liberar solo fichas). | tag/PR, `CHANGELOG.md` |
| `fix` | Carril para un bug de algo ya especificado o un defecto evidente: test que falla, causa raíz, arreglo mínimo y review ligera. `--hotfix`: incidente en producción, con release inmediato y la misma aprobación humana. | ficha `docs/changes/…-fix-….md` |
| `refactor` | Carril para deuda técnica sin cambio de comportamiento: tests de caracterización en verde antes y después, sin tocarlos. | ficha `…-refactor-….md` |
| `chore` | Carril para dependencias que ya existen, configuración, docs y CI, con validación (tests, lint, SCA). | ficha `…-chore-….md` |
| `sync` | Detecta lo hecho fuera del flujo (commits sin spec ni ficha, specs liberadas tocadas después, `architecture.md` desactualizado, specs inferidas, fichas olvidadas) y propone conciliarlo. | `docs/sync.md` |

Orden: `init` → `specify` → `design-spec NNN` (solo si la spec tiene pantallas) → `plan` → `tasks` →
`analyze` → `implement` → `review` → `release`.

Dentro de un plugin las skills se invocan con el prefijo del plugin (por ejemplo `/ai-dd:init`),
así que no chocan con comandos integrados como `/init`.

## Carriles

Spec, plan, tareas, análisis y review son proporcionales a una feature, no a un bug de una línea.
Para el trabajo que **no añade comportamiento** hay carriles con un proceso a su medida:

| Carril | Cuándo | Proceso | Release |
|---|---|---|---|
| `/fix` | Bug: lo correcto ya está en una spec, o es un defecto evidente | test que falla → causa raíz → arreglo → review ligera | con la siguiente `/release` (patch) |
| `/fix --hotfix` | Incidente en producción | igual, desde el tag de producción | inmediato, **misma aprobación humana** |
| `/refactor` | Deuda técnica | tests de caracterización en verde → cambio → los mismos tests en verde | sin entrada en el changelog |
| `/chore` | Dependencias existentes, configuración, docs, CI | cambio → validación (tests, lint, SCA) | solo si corrige una vulnerabilidad |

Cada carril deja una **ficha** `docs/changes/AAAA-MM-DD-<carril>-<slug>.md` (problema,
reproducción, causa, cambio, escalado, verificación). Con una ficha abierta el hook deja editar
código. `aidd.py lane-check` revisa el diff al empezar y al cerrar: si el cambio toca contrato,
datos, seguridad, el sistema de diseño, añade una dependencia o pasa de `workflow.lanes.max_files`
archivos de código (5 por defecto), **escala** a `/specify` salvo que lo aceptes explícitamente.
`/sync` (con `aidd.py drift`) encuentra lo que se hizo sin spec ni ficha.

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
- **SEO técnico sobre el resultado.** En un sitio público, `docs/seo.md` fija la URL canónica, qué
  se indexa y las brechas `SE`; `/plan`, `/review` y `/release` comprueban el HTML generado y la
  respuesta del servidor, no el código fuente. Solo lo técnico y comprobable: sin palabras clave
  ni promesas de posicionamiento. Los íconos y la imagen al compartir salen del sistema de diseño:
  la tarjeta es un componente más y la imagen de cada página se genera con su contenido real.
- **Probar antes de planear.** Lo que el plan da por hecho de una herramienta o framework nuevo se
  comprueba con una prueba de concepto; los valores por defecto de una plantilla se auditan contra
  la constitución.
- **El modelo según el riesgo.** Cada subagente tiene un perfil (`critical`, `standard`,
  `mechanical`, `implementation`) y `.ai/project.yaml → models` le asigna el modelo: Opus donde un
  error llega a producción (seguridad, cobertura de la spec, análisis completo), Sonnet para el
  juicio acotado y Haiku para localizar y comprobar. La sesión principal conserva su modelo.

## Diseño

Solo en proyectos con interfaz (`frontend`, `fullstack`, `mobile`). Lo hace la skill
`design-spec`: el sistema en `skills/design-spec/references/system-mode.md`, el diseño de cada spec
en `spec-mode.md`, los criterios en `criterios.md`, el ciclo en `evaluacion.md` y el movimiento en
`movimiento.md`.

### El diseño se acepta por criterios, no por gusto

El diseño sigue la misma lógica que el código: criterios antes de construir y verificación al
final. `/design-spec` no presenta opciones para elegir; genera **un candidato tras otro** y solo
acepta el que supera un nivel medible.

1. **Criterios** (sección "Criterios de diseño" de la spec y `design/criterios.json`):
   - **Puertas**, obligatorias: sin desplazamiento horizontal, contraste de cada texto contra su
     fondo real, ningún texto tapado por otro elemento, toques ≥ 44 px, foco visible, solo colores
     del sistema, un `h1`, todo visible sin
     JavaScript y con movimiento reducido, nada que no aparezca al recorrer la página, sin recursos
     de otros sitios.
   - **KPIs** con objetivo, sacados de los criterios de aceptación, la constitución y el modo de la
     pantalla (persuadir, operar, leer): la acción principal en la primera pantalla, los textos
     exactos de los criterios, el orden de las secciones, peso, JavaScript, LCP y CLS, líneas de
     los titulares, fuentes cargadas. Cada criterio de aceptación con interfaz tiene al menos uno.
   - **Rúbrica** de cinco puntos con escala anclada (jerarquía, primera pantalla en cinco segundos,
     coherencia con el sistema y la marca, lectura y ritmo, diferencia frente a una plantilla).
2. **Ciclo:** candidato (una página real a ancho de ventana) → `scripts/evaluate.mjs` mide puertas y
   KPIs en Chromium a cada ancho → si pasan, un **subagente evaluador que no lo diseñó** puntúa la
   rúbrica solo con las capturas y lo compara con el mejor anterior → si no llega, sus fallos son la
   lista del siguiente candidato.
3. **Aceptación:** todas las puertas, todos los KPIs y la rúbrica ≥ `threshold` (80) sin ningún
   punto bajo `floor` (3). Como mucho `budget` (5) candidatos; al agotarlos, el ciclo para y
   presenta el mejor con lo que le falta: casi siempre es un criterio mal planteado.
4. **Acta** (`design.md`): una fila por candidato con su resultado y, del aceptado, lo medido y las
   notas con su evidencia. El usuario aprueba el acta o ajusta criterios; no elige entre bocetos.
5. **Después:** `/implement` construye la pantalla como el candidato aceptado y no da la tarea por
   hecha si `evaluate.mjs` falla sobre la build; `/review` vuelve a medir con los mismos criterios
   (una puerta que falla es bloqueante).

Los KPIs de negocio (registros, citas) no se miden antes de publicar: van a
`docs/observability.md` y se revisan tras `/release`; en el diseño se miden sus aproximaciones.

### Cuándo se diseña
| Situación | Qué pasa |
|---|---|
| Proyecto nuevo | `/init` (con `/design-spec system`) investiga el nicho (`nicho.md`), hace la entrevista de diseño (Ronda 4b, con los criterios), escribe `brief.md`, `creative-direction.md`, `anti-cliches.md` y `criterios.json`, y hace el ciclo; el candidato aceptado pasa a ser el sistema (`docs/design/system.md` + `system.html`). |
| Proyecto existente | `/init` solo **documenta** el diseño actual si lo aceptas (capturas reales, deuda `DS`); nunca rediseña. `/design-spec system --redo-design` (o `/init --upgrade --redo-design`) lo vuelve a documentar. |
| Cada spec con pantallas | `/design-spec NNN` entre `/specify` y `/plan`: criterios, ciclo y `design.md` aprobado, que `/plan` sigue. Se omite (`exploration: none`) si la spec no crea ni recompone pantallas. |
| Rediseño | Siempre una spec propia: `/specify` hace la entrevista; `/design-spec NNN` añade puertas para los problemas del diseño anterior y hace el ciclo; la primera tarea aplica los cambios al sistema y luego se migra pantalla por pantalla. |

### Qué alimenta los candidatos
- **Investigación del nicho** (`skills/design-spec/references/nicho.md` → `docs/design/nicho.md`):
  convenciones del sector, materiales del oficio, referentes reales y lo que todos repiten (pasa a
  clichés). Se estudia el patrón, nunca se copia a un competidor.
- **Recursos reales:** el candidato abre y usa el logo, las fotos y los íconos que existen; nunca
  inventa fotos, testimonios, cifras ni logos.
- **Clichés** (`anti-cliches.md` y los rasgos por defecto de las interfaces generadas): cada uno
  presente baja la nota de "diferencia frente a una plantilla".
- **Tipografía real** incrustada en woff2 desde el paquete que usará la app; nada de fuentes del
  sistema como marca salvo que el brief lo pida.
- **Movimiento** solo el que pasa el filtro de `movimiento.md` (frecuencia, propósito, velocidad,
  función), con versión reducida y sin JavaScript; una animación no suma puntos.
- **Marca fuera de la pantalla:** ícono que sale de una marca de la interfaz (texto convertido a
  trazos, legible a 16 px en pestaña clara y oscura) y tarjeta para compartir que repite una pieza
  reconocible del sitio, con sus propios KPIs.

### Iterar
| Si… | Usa | Qué hace |
|---|---|---|
| El ciclo agotó el presupuesto o el aceptado no convence | `/design-spec NNN` (repetir) o `/design-spec system --redo-options` | Traduce lo que no convence a criterios (un KPI, un peso, un cliché nuevo), archiva la ronda en `history/ronda-<N>/` y repite el ciclo desde el mejor candidato. |
| El aceptado convence salvo un aspecto | `/design-spec system --redo-options --only <tipografia\|color\|forma\|fondo\|movimiento> --base <cN>` | Congela el resto, escribe el criterio del eje, mide 2–3 variantes y las compara en una lámina (`templates/design/eje.html`); se acepta la que cumple el criterio sin bajar la puntuación. |
| La revisión manual pide otro valor | `/design-spec NNN --fix <qué>` | Aplica el cambio al aceptado, vuelve a medirlo y lo registra como `refinado`. |
| Ya hay sistema aprobado | `/specify "rediseño de …"` | Spec de rediseño (ver arriba). |

## SEO técnico

Solo en sitios públicos (`seo.indexable: true` en `.ai/project.yaml`); lo hace la skill `seo`
(`skills/seo/`) con el checklist `shared/seo-checklist.md`. Cubre lo técnico y comprobable; no elige
palabras clave ni promete posiciones.

| Momento | Qué pasa |
|---|---|
| `/init` proyecto nuevo | Pregunta si el sitio debe aparecer en buscadores; `/seo setup` fija URL canónica, idiomas, qué no se indexa, renderizado y exclusiones deliberadas en `docs/seo.md`. |
| `/init` proyecto existente | El subagente H lee el código; `/seo audit` compila y audita el HTML generado (y, con permiso, solo `GET` al sitio publicado). Lo verificado son brechas `SE` con severidad; lo no comprobable, "por confirmar". Las brechas se concilian con el roadmap. |
| `/init --upgrade` | Ofrece la auditoría a proyectos web que no la tenían (paso 9b). |
| `/specify` y `/plan` | Requisitos de descubribilidad y sección "Descubribilidad" del plan: una fila y un test sobre el HTML generado por ruta, con valores exactos y exclusiones. |
| `/review` | Revisor de SEO sobre el HTML generado de las rutas del diff; una brecha alta bloquea. |
| `/release` | `/seo verify`: robots, sitemap, 404 propia, rutas privadas, `noindex` solo donde toca y staging protegido; lo que exige herramientas externas lo confirma el usuario. |

El checklist incluye páginas de error propias (404 que responde 404, rutas privadas que redirigen o
responden 401/403 sin indexarse), íconos del sitio, imagen para compartir por página generada desde
la tarjeta del sistema de diseño y sitios en varios idiomas (`hreflang`, `og:locale`, sitemap y 404
por idioma, sin redirecciones automáticas).

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
scripts/aidd.py        # validate · status · hash · templates · snapshot · changes · rotate · history · review-pack · lane-check · drift · hook (se copia a .ai/bin/ en cada proyecto)
shared/
  contract.md          # reglas comunes: estados, numeración, puertas de aprobación
  security-checklist.md  # seguridad del código (OWASP por temas)
  seo-checklist.md     # SEO técnico por temas, con dónde se comprueba cada uno
  vocabulary.md        # títulos y marcadores que lee el validador, en español e inglés
  agent-security.md    # seguridad del proceso con agentes
skills/
  init/                # SKILL.md + references/ + templates/
  design-spec/         # SKILL.md + references/ (system-mode, spec-mode, criterios, evaluacion, movimiento, nicho) + scripts/evaluate.mjs
  seo/                 # SKILL.md + references/audit.md
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
  ofrece, `/design-spec` puede usarla para el primer candidato y enlaza el canvas. Sin ella, los
  candidatos se generan igual en HTML con `skills/init/templates/design/pagina.html`. El HTML es
  siempre lo que se mide: queda en el repo y se abre sin red.
- **Playwright** (recomendado en proyectos con interfaz): el evaluador de diseño
  (`skills/design-spec/scripts/evaluate.mjs`, Node 18+) lo usa si ya está en el proyecto, global o
  en `PLAYWRIGHT_PATH`, y no instala nada. Sin él, las puertas y KPIs se miden a mano con la
  herramienta de navegador de la sesión y quedan marcados así en el acta; un KPI sin medir no
  cuenta como superado.
- **Plugin oficial `design` de Anthropic** (opcional, recomendado en proyectos con interfaz:
  `frontend`, `fullstack`, `mobile`). Por ahora el flujo **depende de él** para la parte de diseño:
  `/init` lo registra en `skills.enabled` si está instalado, `/design-spec` deja la nota de revisarlo con
  `design:design-handoff` y `/review` añade `design:accessibility-review` y `design:design-critique`.
  Si no está instalado, el flujo sigue con su revisión propia de accesibilidad y con la skill
  propia `/design-spec` (que no depende de él).

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
