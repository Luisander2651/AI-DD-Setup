# Plan — Carriles ligeros y `/sync` (1.14.0)

**Estado:** aprobado el 2026-10-14 con las cuatro recomendaciones de §10 e implementado en 1.14.0,
salvo la prueba real (§9, 8.18).
**Origen:** `docs/analisis-brechas.md` §4.1 y §4.2. Hoy todo cambio exige spec + plan + tareas +
`/analyze` + `/review`: un bug de una línea cuesta lo mismo que una feature, y eso empuja a
saltarse el flujo (el hook avisa de "código sin spec activa" y la salida fácil es aprobarlo sin
dejar rastro). La hoja de ruta tenía esto como 1.13.0, pero ese número lo usaron `design-spec` y
`seo`: pasa a **1.14.0** y lo demás se corre un número.

## 1. Objetivo

1. Un proceso **proporcional** para el trabajo que no es feature, que deje rastro igual que una
   spec: qué se cambió, por qué, con qué test y en qué commit.
2. Una regla **determinista** de cuándo un cambio pequeño deja de serlo y debe ir por el flujo
   completo, comprobada al empezar y otra vez al cerrar sobre el diff real.
3. `/sync`: detectar la deriva entre documentos y código (lo hecho fuera del flujo) y proponer
   cómo conciliarla, sin editar documentos aprobados por su cuenta.

Fuera de alcance: cambiar el flujo de features, numeración de specs sin colisiones (1.16.0) y
trabajo en equipo (2.0.0).

## 2. Los carriles

| Carril | Cuándo | Proceso | Review | Release |
|---|---|---|---|---|
| `/fix` | Bug: el comportamiento esperado ya está en una spec, o es un defecto evidente (excepción, caída, dato corrupto) | test que falla → causa raíz → arreglo → test en verde + suite | ligera (§5) | con la siguiente `/release` (patch) |
| `/fix --hotfix` | Incidente en producción | igual que `/fix`, desde el tag de producción | ligera | inmediato, **misma puerta humana** a producción (§6) |
| `/refactor` | Deuda técnica sin cambio de comportamiento | tests de caracterización en verde **antes** → cambio → los mismos tests en verde sin modificarlos | ligera | con la siguiente `/release`; no entra al changelog de usuario |
| `/chore` | Dependencias (versiones existentes), configuración, docs, CI | tarea directa → validación (tests, lint, SCA si toca dependencias) | solo validación | con la siguiente `/release`; solo `Security` si arregla una CVE |

Ningún carril sirve para **añadir** comportamiento. Si al reproducir resulta que el "bug" es un
comportamiento que ninguna spec define y no es un defecto evidente, se escala a `/specify`.

## 3. La ficha de cambio

Cada carril deja **una ficha** en `docs/changes/AAAA-MM-DD-<carril>-<slug>.md`. Fecha y slug en
lugar de número: no compite con la numeración de specs ni choca entre dos personas.

```yaml
---
lane: fix            # fix | hotfix | refactor | chore
status: open         # open → done → released · escalated
base: <commit>       # lo registra la skill al empezar (como impl_base)
relates: [004]       # specs cuyo comportamiento toca (opcional en chore)
covers: [CA3]        # criterios de esas specs que el arreglo vuelve a cumplir (fix)
escalated_to: null   # NNN si se escaló
---
```

Secciones (vocabulario en español e inglés, `shared/vocabulary.md`):

| Sección | fix / hotfix | refactor | chore |
|---|---|---|---|
| Problema · *Problem* | ✔ síntoma, cómo se vio | ✔ qué deuda y por qué ahora | ✔ |
| Reproducción · *Reproduction* | ✔ test que falla (ruta y nombre) y su salida en rojo | — | — |
| Tests de caracterización · *Characterization tests* | — | ✔ qué fijan y su salida en verde antes del cambio | — |
| Causa raíz · *Root cause* | ✔ | — | — |
| Cambio · *Change* | ✔ | ✔ | ✔ |
| Escalado · *Escalation* | ✔ salida de `aidd.py lane-check` al empezar y al cerrar | ✔ | ✔ |
| Verificación · *Verification* | ✔ test en verde, suite, revisión ligera | ✔ | ✔ |
| Decisiones · *Decisions* | misma tabla que en las specs (tipos y fuentes del contrato) | | |

## 4. Cuándo se escala al flujo completo

`aidd.py lane-check <ficha>` lo calcula sobre el diff desde `base` (o sobre los archivos previstos,
al empezar). Escala si se cumple **cualquiera**:

1. **Comportamiento nuevo o distinto del especificado:** lo decide el agente al reproducir y lo
   confirma el usuario; el script no puede verlo.
2. **Contrato:** rutas de API, esquemas, eventos, interfaces públicas de una `library` (rutas de
   `docs/architecture.md → contratos` y las de `skills/plan/references/contracts-by-type.md`).
3. **Datos:** migraciones, modelos persistidos, formato de archivos guardados.
4. **Seguridad:** rutas o temas marcados en `docs/security.md`, autenticación, permisos, datos
   sensibles; rutas protegidas (`protected_paths`).
5. **Dependencia nueva** (en `/chore` solo se suben versiones de las que ya existen).
6. **Sistema de diseño:** tokens o componentes de `docs/design/system.md`.
7. **Tamaño:** más de `workflow.lanes.max_files` archivos de código (por defecto **5**; no
   cuentan tests, docs ni lockfiles).

`/refactor` admite más archivos si el usuario lo acepta explícitamente (un renombrado toca muchos);
se registra como `supuesto` en "Decisiones". Al escalar, la ficha queda `escalated` con
`escalated_to: NNN` y su "Reproducción" o "Problema" alimenta la spec nueva (`extends` si toca
specs cerradas). El test que falla ya escrito se conserva.

## 5. Review ligera

Un solo subagente, con contexto mínimo: el diff desde `base`, la ficha y los criterios citados en
`covers`. Comprueba:

- `fix`: el test falla sin el arreglo y pasa con él (lo ejecuta revirtiendo solo el código, no el
  test); la causa raíz explica el síntoma; el arreglo no es un parche del síntoma.
- `refactor`: los tests de caracterización no cambiaron y siguen en verde; no hay cambio funcional.
- Todos: nada de lo del §4 apareció en el diff final; secretos y SAST sobre lo tocado
  (como `/implement`); tests nuevos de UI o asíncronos ejecutados dos veces (contrato).

Devuelve hallazgos; los bloqueantes se corrigen antes de `done`. Sin `review.md`: el resultado va
en "Verificación" de la ficha. `/chore` no lanza subagente.

## 6. Hotfix y release

- `/release` aprende a incluir fichas `done`: `/release 004 005` pregunta si añade las fichas
  pendientes de liberar, y `/release --changes` libera solo fichas (versión patch). Las fichas
  `fix`/`hotfix` van a `Fixed`; las `chore` de seguridad a `Security`; `refactor` y el resto de
  `chore` no entran al changelog de usuario. Al terminar las marca `released`.
- `/fix --hotfix`: rama desde el tag de producción, ficha, arreglo, review ligera y después
  `/release --changes <ficha>` con **todas** sus reglas (puerta de seguridad, aprobación escrita a
  producción, rollback). Lo acelerado es que no espera a otras specs ni pasa por `/analyze`. Si
  `docs/deployment.md` no tiene sección "Hotfix" (cómo ramificar, si hay staging, cómo volver a
  integrar en la rama principal), se detiene y pide completarla, como hoy con el despliegue.
- Tras producción, el hotfix se integra en la rama principal y el test que fallaba queda ahí.

## 7. `/sync`

Solo lectura salvo lo que el usuario apruebe. `aidd.py drift [--since REF]` hace la parte
determinista; la skill interpreta y propone.

| Detecta | Cómo | Propone |
|---|---|---|
| Commits fuera del flujo | desde `sync.last`, commits que tocan código sin `(NNN)` ni `Ficha:` en el mensaje | ficha retroactiva (`/fix` o `/chore` sin tocar código), o spec nueva |
| Specs `released` que ya no describen el código | archivos de sus `tasks.md` cambiados después de su release por commits sin spec ni ficha | revisar criterios; spec que la extienda |
| `architecture.md` desactualizado | carpetas de primer nivel, manifiestos o servicios nuevos desde su `updated` | propuesta por sección (contrato: documentos `approved` solo reciben propuestas) |
| Specs `inferred` envejecidas | sin aprobar y con sus archivos cambiados | validarlas con `/specify --edit` o descartarlas |
| Fichas abiertas olvidadas | `open` con más de N días o sin commits | cerrar, escalar o descartar |

Escribe el informe en `docs/sync.md` (se sobrescribe; el anterior va a `history/` del propio
`docs/`, nunca se borra) y actualiza `sync.last` solo cuando el usuario cierra la conciliación.
`aidd.py status` sugiere `/sync` si hay commits fuera del flujo desde `sync.last`.

## 8. Cambios en lo que ya existe

| Pieza | Cambio |
|---|---|
| `shared/contract.md` | Regla "Carriles" (cuándo, ficha, escalado, review ligera, release); `/sync`; commits trazables con `<tipo>(<carril>): <qué>` y `Ficha: docs/changes/…` en el cuerpo |
| `scripts/aidd.py` | `lane-check`, `drift`; `validate` revisa fichas (frontmatter, secciones por carril, `escalated_to` existente, `covers` en las specs de `relates`, `done` sin test en `fix`); `status` lista fichas abiertas y sugiere `/sync`; el **hook** acepta una ficha `open` como "spec activa" (las dependencias siguen pidiendo aprobación) |
| `skills/fix`, `refactor`, `chore`, `sync` | Skills nuevas, cada una < 3 000 palabras; el procedimiento común en `shared/lanes.md` |
| `skills/release` | Fichas en Paso 0 (precondiciones), 2 (changelog) y 7 (cierre); modo `--changes` |
| `skills/implement` | Si una tarea revela un bug ajeno a la spec: ficha `/fix` aparte o tarea nueva (hallazgo colateral), nunca arreglo sin rastro |
| `skills/init` | Plantillas `change.md` y sección "Hotfix" en `deployment.md`; `workflow.lanes.max_files` y `sync.last` en `project.yaml`; `AGENTS.md` menciona los carriles |
| `references/upgrade.md` | Crea `docs/changes/`, añade claves, **propone** la sección "Hotfix" y el párrafo de `AGENTS.md` (archivo del agente: se pregunta) |
| `shared/vocabulary.md` + `VOCAB`/`W` | Títulos de la ficha en español e inglés |
| `README.md` | Tabla de carriles y cuándo usar cada uno |
| `docs/analisis-brechas.md` | Hoja de ruta corrida (1.14.0 carriles, 1.15.0 escalabilidad, 1.16.0 SBOM…, 1.17.0 diseño propio); 4.1 y 4.2 ✅ al terminar |

## 9. Pruebas

Contra el sobreajuste (README → Mantenimiento §4), en tipos e idiomas distintos:

- **Fixtures:** `go-cli-en` con una ficha `fix` en inglés correcta; `ionic-app-es` con una
  `refactor`; `*-broken` con: `fix` en `done` sin test, `escalated` sin `escalated_to`, `covers` que
  no existe en la spec, sección de otro carril.
- **Escenarios en `tests/run.py`** (repos git temporales): el hook permite editar con ficha abierta
  y avisa sin ella; `lane-check` escala por tamaño, migración, manifiesto con dependencia nueva y
  ruta protegida, y no escala con 5 archivos + tests; `drift` marca un commit sin referencia y
  reconoce `(004)` y `Ficha:`; `release` en modo `--changes` (solo validación de precondiciones).
- **Prueba real 8.18:** un bug real con `/fix` en Petatlán clima o tu portafolio; un `/chore` de
  dependencias; un `/refactor`; `/sync` sobre un proyecto con commits hechos fuera del flujo; y
  `--hotfix` en una copia con despliegue simulado. Informe en `docs/pruebas/8.18-carriles.md`.

## 10. Decisiones (aprobadas por el usuario, 2026-10-14)

| # | Pregunta | Decisión |
|---|---|---|
| 1 | `/hotfix` como skill propia o modo `/fix --hotfix` | **Modo**: es el mismo proceso más el release; una skill menos que mantener |
| 2 | Umbral de tamaño por defecto | **5 archivos de código**, configurable en `project.yaml` |
| 3 | Lo que quedó de 8.10 (separar plan/tareas, más reglas, conflictos entre specs) | **Sacarlo a 1.14.1**: no depende de los carriles y así esta versión se prueba antes |
| 4 | Informe de `/sync` | **Archivo `docs/sync.md`**: deja rastro y `status` puede leerlo |

## 11. Riesgos

- **Que los carriles se usen para colar features.** Mitigado por el escalado del §4 al cerrar
  sobre el diff real y por la review ligera, que compara con `covers`.
- **Falsos positivos de `lane-check`** (p. ej. un archivo que parece contrato). Se puede continuar
  con aceptación explícita, registrada como `supuesto`.
- **`drift` ruidoso en proyectos con historia larga antes de `/init`.** `sync.last` arranca en el
  commit del `/init` o del upgrade, no al principio de la historia.
- **Hotfix con prisa.** No hay atajo para la puerta de producción; si `deployment.md` no dice cómo,
  se detiene.

## 12. Orden de implementación

1. Contrato, vocabulario y plantilla `change.md`.
2. `aidd.py`: validación de fichas, `lane-check`, hook, `status`; fixtures y escenarios.
3. Skills `/fix` (con `--hotfix`), `/refactor`, `/chore` y `shared/lanes.md`.
4. `/release` con fichas y `--changes`; sección "Hotfix" de `deployment.md`.
5. `aidd.py drift` y skill `/sync`.
6. `/init` y `--upgrade`; README, CHANGELOG, versión 1.14.0 y hoja de ruta.
7. Prueba real 8.18 y correcciones.
