---
name: chore
description: Mantenimiento sin cambio de comportamiento - subir versiones de dependencias existentes, configuración, documentación, CI - con validación y una ficha en docs/changes/. Úsala con /chore o cuando el usuario pida actualizar dependencias, ajustar configuración o tareas de mantenimiento del repo.
---

# /chore — Mantenimiento

Carril ligero para lo que no cambia lo que hace la aplicación: versiones de dependencias **que ya
existen**, configuración de herramientas, documentación, CI. Una dependencia nueva, una
configuración que cambia el comportamiento en producción (tiempos de espera, límites, permisos) o
algo de `../../shared/lanes.md` §3 escala.

> Antes de actuar, lee `../../shared/contract.md` → "Carriles", el procedimiento común
> `../../shared/lanes.md` y `../../shared/agent-security.md` §2 (relativos a este archivo). Si algo
> aquí los contradice, prevalece el contrato.

## Uso

```
/chore <qué>                          # ficha nueva
/chore --continue [<ficha>]           # retoma una ficha abierta
/chore --retro <commit|rango>         # ficha retroactiva (lanes.md §5)
```

## Reglas

- **Dependencias:** solo versiones de las que ya están. Antes de subir una, lee su changelog entre
  la versión actual y la nueva (cambios incompatibles, migraciones, avisos de seguridad) y
  verifica el paquete según `../../shared/agent-security.md` §2 (existe, antigüedad mínima
  `security.agent.min_package_age_days`, origen). Una versión **mayor** con cambios incompatibles
  que obliguen a cambiar código propio de forma no mecánica escala.
- **Rutas protegidas** (CI, hooks, `.claude/`): solo con aprobación explícita, como siempre.
- **Docs del flujo** (`docs/constitution.md`, specs, plan, `architecture.md`): no son un chore.
  Tienen sus skills (`/init` re-sincronizar, `/specify --edit`, `/sync`).
- Sin review con subagente: la validación es la review.

---

## Paso 0 — Arranque

`../../shared/lanes.md` §1 con carril `chore`; borra "Reproducción", "Causa raíz" y "Tests de
caracterización". En "Problema", qué hay que poner al día y por qué (CVE, fin de soporte,
configuración rota).

## Paso 1 — Cambio

- Dependencias: actualiza el manifiesto y el lockfile con el gestor del proyecto
  (`stack.package_manager`), una dependencia o un grupo coherente por commit.
- Configuración o CI: el cambio mínimo; si toca CI, explica qué jobs cambian.
- Docs: solo lo que se pidió.

Anota en "Cambio" qué versiones pasaron de cuál a cuál y lo relevante de sus changelogs.

## Paso 2 — Validación

1. Build, suite completa, lint y type-check.
2. Si se tocaron dependencias: la herramienta SCA (`security.tools.sca` `instalada` o `en-ci`) y,
   con `security.tools.sast`, sobre lo tocado. Una vulnerabilidad crítica o alta nueva detiene el
   chore.
3. `lane-check <ficha>` sobre el diff real; un motivo se trata como en `../../shared/lanes.md` §3.
4. Resultado en "Verificación", `status: done`, `validate` sin errores y commit.

Un chore entra al changelog de usuario solo si corrige una vulnerabilidad (`Security`).

## Paso 3 — Informe

Qué se actualizó, resultado de la validación y estado de la ficha.
