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
| `init` | Inicializa un proyecto nuevo o existente: detecta stack y metodologías de agentes en competencia, explora el código con 6 subagentes (uno más si documenta el diseño existente y otro si el sitio es público e indexable) o crea el proyecto base y audita los valores por defecto de la plantilla (nuevo), entrevista y genera la documentación base. Con interfaz: opciones de diseño en HTML (nuevo) o el sistema de diseño actual documentado, si el usuario lo acepta (existente). `--upgrade` pone al día un proyecto con la versión instalada del plugin; `--upgrade --redo-design` vuelve a documentar el diseño existente (todas las vistas con capturas reales) sin perder la deuda ya citada; `--upgrade --redo-options` rehace las opciones de diseño cuando ninguna convenció y aún no hay sistema aprobado, archivando la ronda anterior; con `--only <eje> --base <opción>` afina solo la tipografía, el color, la forma, el fondo o el movimiento de una opción (ver "Diseño"). | `AGENTS.md`, `.ai/project.yaml`, `docs/constitution.md`, `architecture.md`, `deployment.md`, `security.md`, `observability.md`, `roadmap.md`, `docs/design/` (con interfaz), `seo.md` (sitio indexable), plantillas |
| `specify` | Convierte una idea en spec: qué y por qué, sin tecnología, con casos de abuso. | `docs/specs/NNN-slug/spec.md` |
| `design-spec` | Diseño de interfaz. `system`: opciones en HTML y sistema de diseño (o el diseño existente documentado); lo llama `init`. `NNN`: en cada spec con pantallas, 2–3 composiciones sobre el sistema, cada una con metáfora del contenido real y distinta de las pantallas vecinas, antes de planear. `--fix`: refinado tras la revisión manual. | `docs/design/`, `docs/specs/NNN-slug/design.md` + composiciones en HTML |
| `seo` | SEO técnico de sitios públicos. `setup`: reglas del sitio; `audit`: auditoría sobre la build (y, con permiso, el sitio publicado) con brechas `SE` y propuestas para el roadmap; `verify`: comprobaciones en producción tras un despliegue. La llaman `init` y `release`. | `docs/seo.md` |
| `clarify` | Encuentra las ambigüedades de mayor impacto en una spec en borrador y las resuelve con preguntas. | `spec.md` actualizada |
| `plan` | Diseña el cómo: contratos, modelo de amenazas, trazabilidad, rollout y Constitution Check. | `plan.md`, ADRs |
| `tasks` | Divide el plan en tareas pequeñas y verificables, con cobertura de criterios y amenazas. | `tasks.md` |
| `analyze` | Verificación independiente de consistencia entre spec, plan, tareas y constitución; puerta antes de implementar. | `analysis.md` (pass/fail) |
| `implement` | Ejecuta las tareas una a una, con tests primero y escaneo de seguridad. | código, `tasks.md` marcado |
| `review` | Revisión independiente con subagentes: spec, plan, constitución, seguridad OWASP, calidad y, si aplica, accesibilidad y SEO técnico. | `review.md` con veredicto |
| `release` | Versión, changelog, staging y producción **solo con aprobación explícita**; rollback guiado. | tag/PR, `CHANGELOG.md` |

Orden: `init` → `specify` → `design-spec NNN` (solo si la spec tiene pantallas) → `plan` → `tasks` →
`analyze` → `implement` → `review` → `release`.

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
- **SEO técnico sobre el resultado.** En un sitio público, `docs/seo.md` fija la URL canónica, qué
  se indexa y las brechas `SE`; `/plan`, `/review` y `/release` comprueban el HTML generado y la
  respuesta del servidor, no el código fuente. Solo lo técnico y comprobable: sin palabras clave
  ni promesas de posicionamiento. Los íconos y la imagen al compartir salen del sistema de diseño:
  la tarjeta es un componente más y la imagen de cada página se genera con su contenido real.
- **Probar antes de planear.** Lo que el plan da por hecho de una herramienta o framework nuevo se
  comprueba con una prueba de concepto; los valores por defecto de una plantilla se auditan contra
  la constitución.

## Diseño

Solo en proyectos con interfaz (`frontend`, `fullstack`, `mobile`). Lo hace la skill
`design-spec`: el sistema en `skills/design-spec/references/system-mode.md` y el diseño de cada spec
en `skills/design-spec/references/spec-mode.md`.

### Cuándo se diseña
| Situación | Qué pasa |
|---|---|
| Proyecto nuevo | `/init` (con `/design-spec system`) investiga el nicho (`nicho.md`), hace la entrevista de diseño (Ronda 4b) con territorios de identidad propuestos, escribe `brief.md`, `creative-direction.md` y `anti-cliches.md`, genera 3 opciones en HTML (2 si la marca ya está cerrada) y la elegida pasa a ser el sistema (`docs/design/system.md` + `system.html`). |
| Proyecto existente | `/init` solo **documenta** el diseño actual si lo aceptas (capturas reales, deuda `DS`); nunca rediseña. `/design-spec system --redo-design` (o `/init --upgrade --redo-design`) lo vuelve a documentar. |
| Cada spec con pantallas | `/design-spec NNN` entre `/specify` y `/plan`: 2–3 composiciones en HTML sobre el sistema y `design.md` aprobado, que `/plan` sigue. Se omite (`exploration: none`) si la spec no crea ni recompone pantallas. |
| Rediseño | Siempre una spec propia: `/specify` hace la entrevista y `/design-spec NNN` genera las opciones en la carpeta de la spec; la primera tarea aplica los cambios al sistema y luego se migra pantalla por pantalla. |

### Cómo se generan opciones que no parezcan de plantilla
- **Investigación del nicho** (`skills/design-spec/references/nicho.md` → `docs/design/nicho.md`): antes
  de la entrevista se estudian las convenciones del sector, los materiales propios del oficio
  (documentos, envases, espacios, herramientas), 4–6 referentes reales con enlace, lo que todos
  repiten (pasa a clichés) y el contexto de uso. Profundidad según el producto: completa en sitios
  y apps públicas, ligera en herramientas internas, omitida si hay manual de marca. Se estudia el
  patrón, nunca se copia a un competidor; sin estereotipos ni creación de logo o nombre.
- **Territorios de identidad.** Con esa investigación, la entrevista propone 2–3 formas de ser
  reconocible en el sector, cada una con concepto firma, tono, movimiento y superficies. El
  elegido va a `creative-direction.md` y las opciones lo componen.
- **Concepto firma.** La entrevista pregunta si ya hay una idea que deba reconocerse (p. ej. "el
  código se escribe y se compila en la tarjeta"). Con ella, las opciones son **composiciones** de
  esa idea; sin ella, cada opción es una **dirección** con su propia idea y su momento firma.
- **Referencias con nombre** (productos, sitios o apps), no adjetivos.
- **Distintas de verdad.** Entre opciones cambia siempre la composición de la pantalla principal y
  al menos otro eje. Mismo esqueleto con otra piel = rehacer.
- **Idea anclada en el brief.** Cada opción declara su idea en una frase, ligada a un dato real
  (público, contexto de uso, producto, lugar), y las 2–3 decisiones de estructura que la
  materializan; un solo momento firma, dibujado en fotogramas.
- **Clichés del sector.** Además de la lista por tipo de proyecto, la entrevista añade los del
  dominio del producto, cada uno con su alternativa.
- **Tipografía justificada.** Nada de fuentes del sistema como marca ni de fuentes de moda elegidas
  por estética: cada familia se justifica contra el brief y se incrusta en woff2.
- **Movimiento con jerarquía.** Cada opción trae su paleta de movimiento (momento firma,
  microinteracciones, entradas, transiciones) derivada del territorio, con versión sin movimiento
  y demo en vivo en el HTML. Un protagonista; el resto sobrio.
- **Superficies y fondos.** Más allá del color sólido: texturas, patrones, cambios entre secciones
  y tratamiento de imagen, salidos del territorio y en CSS o SVG ligero. El contraste se mide sobre
  la zona más difícil del fondo (`--surface-worst`).
- **Repaso antes de enseñar** cada opción contra los rasgos por defecto de las interfaces generadas
  (`system-mode.md` §6) y contra `anti-cliches.md`, con o sin el plugin `design`.
- **Marca fuera de la pantalla.** Íconos que salen de una marca de la interfaz (texto convertido a
  trazos, revisados a 16 px en pestaña clara y oscura) y una tarjeta para compartir que repite la
  pieza firma del sitio, con medidas y datos reales.

### Cada pantalla, su propia composición

Lo que evita que todas las pantallas parezcan la misma plantilla (`spec-mode.md` §1–§4):
- **2–3 composiciones por spec** sobre el sistema aprobado, cada una con **nombre y metáfora**
  sacada del contenido real ("la ficha del paciente como expediente con pestañas").
- **Vecino más parecido:** cada composición dice a qué otra pantalla del producto se parece más y
  en qué se diferencia; los componentes firma son **exclusivos** de su pantalla.
- **Jerarquía declarada** con proporciones (destacado 7:5, mosaico 5:7) en lugar de rejillas de
  iguales sin motivo; **ancho intermedio** revisado cuando hay filas.
- **Riesgo marcado:** una composición puede llevar a propósito un elemento que roza el cliché, y
  el usuario decide si se queda.
- **Adornos desde datos reales** (índices, rutas, código decorativo), ocultos a lectores de pantalla.
- **Fichas de movimiento** con versión reducida, sin JavaScript y táctil, su coste en JS y reglas
  de rendimiento (sin `filter` animado en superficies grandes ni `backdrop-filter` en elementos
  fijos; revelados por disparo, no ligados al scroll).
- **Reglas de uso contables** del sistema (cuántos momentos protagonistas, dónde se permite el
  efecto firma) y **anti-clichés por pantalla** con la alternativa usada.
- **Refinado registrado:** lo que cambia tras la revisión manual queda como decisión `refinado`
  con su motivo (`/design-spec NNN --fix`).

### Iterar antes de elegir
| Si… | Usa | Qué hace |
|---|---|---|
| Ninguna opción convence | `/design-spec system --redo-options` (o "rehacer" en `/design-spec NNN`) | Pregunta qué falló y qué se conserva, actualiza brief, dirección y clichés, archiva la ronda en `history/ronda-<N>/` y genera otra con "qué cambia respecto a la ronda anterior". |
| Una opción convence salvo un aspecto | `/design-spec system --redo-options --only <tipografia\|color\|forma\|fondo\|movimiento> --base <opción>` (o "afinar un eje" en `/design-spec NNN`) | Congela la base, escribe los criterios del eje desde el brief, propone 2–3 variantes justificadas y las compara en una lámina (`templates/design/eje.html`) que comprueba fuentes y contraste y simula luz exterior. |
| Ya hay sistema aprobado | `/specify "rediseño de …"` | Spec de rediseño (ver arriba). |

En `/plan`, la tipografía o el color se afinan **antes** de "Cambios a incorporar al sistema";
cambiarlos después obliga a `/plan NNN --fix`.

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
scripts/aidd.py        # validate · status · hash · templates · snapshot · changes · rotate · history · review-pack · hook (se copia a .ai/bin/ en cada proyecto)
shared/
  contract.md          # reglas comunes: estados, numeración, puertas de aprobación
  security-checklist.md  # seguridad del código (OWASP por temas)
  seo-checklist.md     # SEO técnico por temas, con dónde se comprueba cada uno
  vocabulary.md        # títulos y marcadores que lee el validador, en español e inglés
  agent-security.md    # seguridad del proceso con agentes
skills/
  init/                # SKILL.md + references/ + templates/
  design-spec/         # SKILL.md + references/ (system-mode, spec-mode, nicho)
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
  ofrece, `/init` y `/plan` generan con ella las opciones de diseño (y las láminas de una ronda
  acotada a un eje) y enlazan el canvas. Sin ella,
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
