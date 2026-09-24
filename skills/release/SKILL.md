---
name: "release"
description: "Libera specs revisadas: versión, CHANGELOG, staging y, solo con aprobación explícita del usuario, producción; con rollback guiado. Úsala con /release NNN o cuando el usuario pida desplegar o publicar una versión."
---

# /release — De código revisado a producción

Último paso del flujo:

```
/init → /specify → /plan → /tasks → /analyze → /implement → /review → [/release]
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Prepara la versión, la despliega a staging, verifica y **solo con aprobación explícita del
usuario** la lleva a producción. Sigue `docs/deployment.md` al pie de la letra.

## Uso

```
/release <NNN> [<NNN> …]     # una o varias specs en la misma versión
/release --rollback          # revertir la última versión en producción
```

## Reglas innegociables

- **Producción solo con aprobación explícita** en esta sesión, dada después de ver el resumen
  del Paso 5. "Ok", "sigue" o una aprobación anterior no cuentan: pide una confirmación inequívoca
  (p. ej. que el usuario escriba `desplegar v1.4.0 a producción`). En una sesión desatendida,
  deténte siempre antes de producción.
- **Nunca** hagas force push, saltes CI, desactives checks, despliegues desde un árbol con cambios
  sin commitear o apliques la fase *contract* de una migración en la misma versión que su *expand*.
- **Nunca improvises el procedimiento.** Si `docs/deployment.md` no dice cómo desplegar o cómo
  revertir, detente y pide completarlo.
- **Nada de secretos** en comandos, logs, changelog o mensajes.

---

## Paso 0 — Precondiciones

Para cada spec incluida:
1. `status: implemented` y T001–T092 marcadas.
2. `review.md` con `verdict: approved` y `human_signoff` distinto de `pending`.
3. El `head` de la review coincide con el código actual de la rama; si hubo commits después,
   sugiere `/review NNN --rerun`.
Para el repositorio:
4. Árbol limpio y rama correcta según `docs/deployment.md`.
5. CI en verde para el commit a liberar (consulta con `gh` o la herramienta disponible; si no
   puedes consultarlo, pide al usuario que lo confirme).
6. **Puerta de seguridad:** corre la herramienta SCA (y la de contenedores, si aplica) de
   `.ai/project.yaml → security.tools` sobre el commit a liberar; pueden haber aparecido CVEs
   nuevas desde la review. Cualquier vulnerabilidad crítica o alta sin excepción vigente en
   `docs/security.md → Excepciones aceptadas` detiene el release. Una excepción solo la registra el
   usuario, con motivo y fecha de vencimiento; las vencidas no cuentan.
7. Lee `.ai/project.yaml → deploy`. Si `strategy: none`, ejecuta solo los Pasos 1–3, 7 y 8
   (versión, changelog y cierre, sin despliegue); en ese caso T095–T097 se marcan como
   `no aplica`.

8. `python .ai/bin/aidd.py validate docs/specs/NNN-<slug>` (o `python3`) para cada spec incluida, sin errores.

Si algo falla, detente e indica qué skill lo resuelve.

## Paso 1 — Versión

Propone la nueva versión SemVer a partir de la versión actual (último tag o manifiesto):
- **major:** cambio incompatible en API pública, contrato entre capas o datos.
- **minor:** funcionalidad nueva compatible.
- **patch:** solo correcciones.
En `library`, usa el impacto en SemVer declarado en cada plan. Si varias specs van juntas, gana el
nivel más alto. Confirma la versión con el usuario antes de escribirla.

## Paso 2 — Changelog y versión en archivos

1. En `CHANGELOG.md`, mueve lo de `[Unreleased]` y añade lo de estas specs bajo
   `## [X.Y.Z] - AAAA-MM-DD`, agrupado en *Added / Changed / Fixed / Removed / Security*. Cada
   entrada en lenguaje de usuario, con referencia a la spec (`(spec 004)`). Sin detalles internos.
2. Actualiza la versión en los manifiestos del proyecto (`package.json`, `pyproject.toml`, etc.).
3. Commit `chore(release): vX.Y.Z` (o la convención del proyecto).

## Paso 3 — Integración

Según `docs/deployment.md`:
- Si se libera desde un PR: créalo (título `Release vX.Y.Z`, cuerpo con el changelog y enlaces a
  specs y reviews). **No lo fusiones** sin confirmación del usuario.
- Si se libera por tag: crea el tag anotado `vX.Y.Z` y súbelo solo tras confirmación.

## Paso 4 — Staging (T095)

Si existe staging:
1. Despliega con el procedimiento de `docs/deployment.md` (o espera al pipeline si se dispara
   solo). Aplica migraciones *expand* si corresponde.
2. Verifica: health check, smoke tests y, por cada spec, los criterios de aceptación que puedan
   comprobarse en staging.
3. Revisa logs y errores durante unos minutos.
4. Si `security.tools.dast` está configurado, pide confirmación y ejecútalo **solo contra la URL de
   staging** de `docs/deployment.md` (nunca contra producción ni contra dominios de terceros).
   Hallazgos críticos o altos detienen el release como en el Paso 0.
5. Marca T095 en cada `tasks.md`.
Si falla, **no sigas a producción**: reporta, revierte staging si hace falta y sugiere volver a
`/implement` con una tarea nueva.

Si no existe staging y la constitución exige pasar por staging, detente.

## Paso 5 — Puerta de aprobación (T096)

Presenta al usuario, en un solo mensaje:
- Versión y specs incluidas.
- Resultado de staging.
- Migraciones y su orden.
- Feature flags y su estado inicial.
- Riesgos principales (de los planes y las reviews).
- Estado de seguridad: resultado de SCA/DAST y excepciones vigentes que aplican a esta versión.
- **Plan de rollback** exacto y tiempo estimado.
- Métricas que vas a vigilar después.
Pide la confirmación inequívoca. Registra en cada `tasks.md` bajo T096:
`  - aprobado por <usuario> el <fecha hora> para vX.Y.Z`. Sin eso, termina aquí.

## Paso 6 — Producción (T097)

1. Despliega con el procedimiento de `docs/deployment.md`.
2. Verifica health check y smoke tests. Toma el `request_id` de una petición de los smoke tests y
   confirma que sus logs y, si aplica, sus eventos de auditoría llegan al destino de
   `docs/observability.md`.
3. Vigila las métricas del Rollout durante la ventana definida en `docs/deployment.md` (por
   defecto 15 minutos) y reporta.
4. Marca T097.
**Si algo sale mal:** detén el avance, muestra la evidencia y propone el rollback de
`docs/deployment.md`. Ejecútalo solo con confirmación del usuario, salvo que `deployment.md`
defina un rollback automático. Después, crea una entrada en `docs/roadmap.md → Pendientes` con el
incidente y sugiere `/specify` o `/plan --redo` según la causa.

## Paso 7 — Cierre (T098)

Para cada spec:
1. `status: released` y añade al frontmatter `released: vX.Y.Z (AAAA-MM-DD)`.
2. Marca T098 y actualiza `docs/specs/README.md`.
3. En `docs/roadmap.md`, marca los objetivos cumplidos.
4. Si hay feature flags, añade en `docs/roadmap.md → Pendientes` la limpieza del flag y, si
   aplica, la migración *contract* para una versión posterior.

## Paso 8 — Informe

Versión liberada, specs incluidas, estado de staging y producción, métricas observadas, enlaces al
PR/tag y tareas de seguimiento añadidas al roadmap.

---

## Modo `--rollback`

1. Identifica la versión actual en producción y la anterior.
2. Muestra el procedimiento de rollback de `docs/deployment.md` y las migraciones involucradas.
3. Pide confirmación explícita y ejecútalo.
4. Verifica health check y métricas.
5. Las specs afectadas vuelven de `released` a `implemented`, con una nota en su "Historial";
   añade la entrada `## [X.Y.Z] - revertida el <fecha>` en `CHANGELOG.md`.

## Library

Si `project.type: library`, "producción" es la publicación en el registro (npm, PyPI,
crates.io…). Staging es un dry-run (`npm publish --dry-run`, `twine check`, etc.) o una publicación
en un registro de pruebas. La publicación real sigue exigiendo la puerta del Paso 5, y debe
hacerse desde CI con el tag si la constitución lo exige. Un paquete publicado no se puede
retirar: el rollback es publicar un patch.`
