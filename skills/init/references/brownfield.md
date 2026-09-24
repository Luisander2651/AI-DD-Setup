# Procedimientos para proyectos existentes

## 1. Metodologías o reglas de agentes en competencia

Un proyecto puede traer instrucciones de otro flujo (AI-DLC, Spec Kit, reglas de Cursor, Kiro,
Windsurf, Copilot, Cline) o secciones de `CLAUDE.md`/`AGENTS.md` que se declaran prioritarias.
Dos flujos activos a la vez producen instrucciones contradictorias para el agente.

1. **Inventario:** lista cada fuente con su ruta, qué pretende controlar (flujo de trabajo,
   estilo de código, herramientas) y su estado (activo, a medias, abandonado). Separa las reglas
   de **flujo** (qué pasos seguir) de las de **estilo o framework** (p. ej. guías de Laravel
   Boost): estas últimas suelen ser compatibles y se conservan.
2. **Pregunta al usuario** qué hacer con cada regla de flujo:
   - **Pausar** (recomendado si hay trabajo a medias): mueve el texto **literal, sin reescribir**
     a un archivo propio en la raíz (p. ej. `AIDLC.md`) que no se carga por defecto, con una
     cabecera que diga cuándo se movió, por qué y cómo retomarlo. Añade ese archivo y su carpeta
     de estado a `security.agent.protected_paths`.
   - **Migrar:** sus specs o requisitos pasan a `docs/specs/` (§3) y sus principios se proponen
     como principios de la constitución; el original queda en `referencias/` o se pausa.
   - **Convivir:** documenta en `AGENTS.md` qué flujo manda en qué caso. Úsalo solo si no se
     solapan.
3. Registra la decisión en `.ai/project.yaml` (p. ej. `workflow.legacy_workflow: <nombre>-paused`),
   en `AGENTS.md` (una línea) y en `CHANGELOG.md`.
4. Nunca borres el material de la otra metodología ni sus carpetas de estado.

## 2. Convenciones de las specs inferidas

- `status: inferred` y `confidence: alta | media | baja`.
- **Casillas de criterios:** en una spec inferida, `[x]` significa "un test existente cubre este
  criterio" y `[ ]` "comportamiento observado en el código, sin test". Explícalo con un comentario
  al inicio de la sección y en `docs/specs/README.md`.
- **Detalle técnico permitido:** a diferencia de las specs nuevas, los criterios de una spec
  inferida pueden citar endpoints, rutas o códigos HTTP, porque describen el sistema actual.
  Al aprobarla con `/specify --edit`, se reescriben sin tecnología solo si el usuario lo pide.
- **Casos de abuso incumplidos:** si el comportamiento seguro esperado no se cumple hoy, escribe
  el criterio `(abuso)` con el comportamiento deseado y la marca **HOY NO SE CUMPLE: <motivo>**.
  No se marca `[x]`. Estos criterios son el punto de partida de specs de corrección y se
  enlazan desde el roadmap y `docs/security.md`.
- Bugs aparentes, deuda y contradicciones entre docs y código van en "Observaciones", nunca en
  los criterios.

## 3. Migración de specs previas en otros formatos

Si el subagente B encuentra specs, diseños o planes previos (p. ej. `features/`, `specs/`,
`.specify/specs/`, `docs/requirements/`, `aidlc-docs/`):

1. Crea una spec nueva `docs/specs/NNN-<slug>/spec.md` con `status: draft` que recoja solo el
   **qué** y el **por qué** (sin diseño técnico), con criterios `CA` numerados y casos de abuso.
2. Copia los originales **sin modificar** a `docs/specs/NNN-<slug>/referencias/` y enlázalos
   desde la spec y desde "Notas para /plan".
3. Lo que el original resuelve pero sea ambiguo o contradictorio con el código va a
   `[NECESITA ACLARACIÓN]` (máximo 3) o a "Supuestos".
4. No borres el original: anota en `docs/roadmap.md → Pendientes` que puede eliminarse cuando el
   usuario revise la migración.

## 4. Conciliar brechas con el roadmap

Aplica cuando `/init` o `/init --upgrade` detectan brechas (en `docs/observability.md`,
`docs/security.md` → Riesgos, `docs/deployment.md` → Riesgos) y el proyecto ya tiene
`docs/roadmap.md`. **El roadmap es del usuario:** nunca añadas, renumeres ni reescribas objetivos
sin su confirmación.

0. **Solo brechas confirmadas.** Las "Brechas por confirmar" (dependen de configuración no
   versionada o de algo no verificado) no se concilian ni generan propuestas: primero se
   confirman con el usuario.
1. **Compara por significado, no por texto.** Para cada brecha, busca en el roadmap (objetivos y
   "Pendientes y deuda") y en las specs existentes algo que ya la cubra, aunque use otras
   palabras (p. ej. "registrar accesos a expedientes" cubre "sin eventos de auditoría de
   lecturas de datos de salud").
2. **Clasifica** cada brecha:
   - **Cubierta:** un objetivo o spec existente la resuelve. En el documento de la brecha, enlaza
     el objetivo (`→ roadmap objetivo N`) o la spec. No toques el roadmap.
   - **Parcial:** un objetivo existente la cubre en parte. Propón añadir lo que falta a su
     criterio de éxito, mostrando el texto actual y el propuesto.
   - **Nueva:** nada la cubre. Propón una fila nueva con objetivo, criterio de éxito medible y
     origen (documento y sección de la brecha).
   - En cualquier caso, un objetivo que atiende un riesgo o brecha con correcciones (`RS1.a`…)
     las cita **todas**: las que cubre y las que quedan fuera con su destino. Una propuesta que
     omite correcciones se marca como **parcial** y se dice cuáles faltan.
3. **Pregunta una sola vez** con la lista de propuestas (parciales y nuevas); el usuario elige
   cuáles aplicar. Si la sesión es desatendida, no modifiques el roadmap: deja las propuestas en
   el resumen final.
4. **Informa también lo inverso:** lo que un objetivo del usuario menciona y la exploración **no**
   detectó. Es una señal útil (la exploración se quedó corta o el objetivo va más allá del código
   actual) y no se trata como error.
5. Registra la conciliación en el resumen: cubiertas (con su enlace), propuestas aplicadas,
   propuestas rechazadas y diferencias del punto 4.

## 5. Re-sincronizar sin perder lo que el usuario confirmó o decidió

Al re-sincronizar, la exploración nueva solo ve el código y la configuración declarada; no sabe
lo que el usuario confirmó ni decidió. Para no perderlo:

1. **Contenido protegido.** Nunca propongas eliminar ni reescribir:
   - frases o filas con el marcador `(confirmado por el usuario, …)` o `(decisión del usuario, …)`;
   - excepciones aceptadas, retenciones, responsables y cualquier valor que no pueda deducirse
     del código (plazos legales, quién aprueba, quién puede leer);
   - las secciones "Aclaraciones", "Historial" y "Enmiendas" de cualquier documento.
2. **Documentos aprobados.** Un documento con `status: approved` no se regenera. Solo recibe
   propuestas **por sección** (texto actual → propuesto, con evidencia) que el usuario acepta o
   rechaza una por una.
3. **Documentos inferidos** (`status: inferred` o `proposed`): puedes proponer cambios en el
   resto del contenido, mostrando el diff por archivo antes de escribir.
4. **Contradicciones.** Si la exploración nueva contradice algo protegido (p. ej. detecta
   `single` en `.env.example` y el documento dice `stderr` confirmado por el usuario), **no lo
   cambies**: pregunta al usuario si sigue siendo cierto, mostrando ambos valores y la evidencia.
   Si lo reconfirma, actualiza la fecha del marcador.
5. **Brechas.** Una brecha resuelta desde la última sincronización (el código ya la corrige) se
   propone como resuelta con su evidencia, no se borra en silencio; una nueva sigue las reglas de
   §4 y de "declarado ≠ real".
6. **Resumen.** Lista por documento: cambios aplicados, rechazados, contenido protegido
   conservado y contradicciones consultadas.
