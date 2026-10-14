---
name: sync
description: Detecta la deriva entre documentos y código - commits hechos fuera del flujo, specs liberadas que el código ya no cumple, architecture.md desactualizado, specs inferidas sin validar y fichas olvidadas - y propone cómo conciliarla. Úsala con /sync, antes de planear en una zona tocada, o cuando el usuario pregunte si los documentos siguen al día.
---

# /sync — Conciliar documentos y código

Lo hecho fuera del flujo (un arreglo directo, un cambio de otra persona, una sesión sin el plugin)
deja specs y documentos que ya no describen el código. `/sync` lo detecta y propone cómo
conciliarlo. **Solo lee** salvo lo que el usuario apruebe.

> Antes de actuar, lee `../../shared/contract.md` → "Deriva (`/sync`)" y "Carriles" (relativo a
> este archivo). Si algo aquí lo contradice, prevalece el contrato.

## Uso

```
/sync                     # desde .ai/project.yaml → sync.last (o desde el /init)
/sync --since <REF>       # desde un commit o tag concreto
```

## Reglas

- **No edita** specs, `architecture.md` ni documentos `approved`: propone por sección
  (`../init/references/brownfield.md` §5) y aplica solo lo confirmado.
- **No cambia código.** Las correcciones son fichas o specs.
- Una spec `implemented` o `released` nunca se edita: lo que cambió se recoge en una spec que la
  extienda o en una ficha.
- Lo que no se puede saber por la historia (por qué se hizo un commit) se pregunta, no se supone.

---

## Paso 1 — Datos

`python .ai/bin/aidd.py drift --json` (con `--since` si se pidió; intérprete según el contrato).
Si no es un repositorio git, dilo y detente. Lee también `aidd.py status`.

## Paso 2 — Interpretación

Para cada grupo del informe, mira lo justo para clasificarlo (mensaje, diff resumido con
`git show --stat`, la spec afectada):

| Grupo | Clasifica como | Propone |
|---|---|---|
| Commit fuera del flujo | bug arreglado · refactor · mantenimiento · comportamiento nuevo · trivial | ficha retroactiva (`/fix --retro`, `/refactor --retro`, `/chore --retro`) · spec nueva con `extends` · nada (trivial: formato, comentario) |
| Spec `released` tocada después | el cambio respeta sus criterios · los contradice | nada · spec que la extienda (o ficha `/fix` si el cambio es el bug) |
| Hueco en `architecture.md` | carpeta, servicio o manifiesto nuevo | propuesta de sección |
| Spec `inferred` sin validar | sigue describiendo el código · ya no | `/specify --edit NNN` para validarla · proponer descartarla |
| Ficha abierta vieja | sigue pendiente · ya se hizo · ya no aplica | `/<carril> --continue` · cerrarla · marcarla `escalated` o borrarla con permiso |

Agrupa los commits que son el mismo cambio. Un commit con varias cosas se clasifica por lo más
grave.

## Paso 3 — Informe

Escribe `docs/sync.md` (si ya existe, muévelo antes a `docs/history/sync.<fecha anterior>.md`;
nunca se borra):

```markdown
---
date: AAAA-MM-DD
since: <commit> (<origen>)
head: <commit>
status: open        # open → closed cuando el usuario cierra la conciliación
---
# Conciliación AAAA-MM-DD
## Resumen
## Commits fuera del flujo        (| commit | qué es | propuesta | decisión |)
## Specs con deriva
## Arquitectura
## Specs inferidas
## Fichas abiertas
```

Muestra el resumen y pregunta por cada propuesta (agrupadas): aplicar, posponer o descartar.

## Paso 4 — Aplicar

Solo lo aceptado: fichas retroactivas con la skill del carril, specs nuevas con `/specify`,
propuestas de `architecture.md` aplicadas por sección. Anota la decisión en `docs/sync.md`.

Cuando no quede nada pendiente de decidir (aplicado, pospuesto con motivo o descartado),
`status: closed` y `.ai/project.yaml → sync.last: <head>`. Si quedan decisiones abiertas,
`sync.last` no se mueve: el siguiente `/sync` las vuelve a mostrar.

## Paso 5 — Informe

Cuántos commits y specs se revisaron, qué se propuso y qué quedó aplicado o pendiente.
