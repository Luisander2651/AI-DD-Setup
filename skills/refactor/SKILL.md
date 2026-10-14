---
name: refactor
description: Cambia la estructura del código sin cambiar su comportamiento - tests de caracterización primero, cambio, los mismos tests en verde y review ligera - dejando una ficha en docs/changes/. Úsala con /refactor o cuando el usuario pida limpiar, reorganizar, renombrar o pagar deuda técnica sin cambiar lo que hace la aplicación.
---

# /refactor — Cambiar la estructura, no el comportamiento

Carril ligero para deuda técnica: renombrar, extraer, mover, simplificar, quitar duplicados. Si el
resultado hace algo distinto para el usuario (aunque sea "mejor"), no es un refactor: es `/fix`
(si lo actual es un bug) o `/specify`.

> Antes de actuar, lee `../../shared/contract.md` → "Carriles" y el procedimiento común
> `../../shared/lanes.md` (relativos a este archivo). Si algo aquí los contradice, prevalece el
> contrato.

## Uso

```
/refactor <qué y por qué>             # ficha nueva
/refactor --continue [<ficha>]        # retoma una ficha abierta
/refactor --retro <commit|rango>      # ficha retroactiva (lanes.md §5)
```

## Reglas

- **Los tests de caracterización mandan.** Fijan lo que el código hace **hoy** (aunque parezca
  raro) y no se modifican durante el cambio. Si para que pasen hay que cambiarlos, el
  comportamiento cambió: detente.
- **Ni una funcionalidad nueva, ni un bug arreglado de paso.** Un bug encontrado es una ficha
  `/fix` aparte (antes o después, no mezclado).
- **Pasos pequeños** con la suite en verde entre uno y otro; un commit por paso si la política lo
  permite.
- Un renombrado o un movimiento puede tocar muchos archivos: si `lane-check` escala **solo por
  tamaño** y el cambio es mecánico, el usuario puede aceptarlo (`supuesto`). Por cualquier otro
  motivo, escala.

---

## Paso 0 — Arranque

`../../shared/lanes.md` §1 con carril `refactor`. En "Problema" escribe qué cuesta hoy esa deuda
(tests difíciles, duplicación que ya causó bugs, módulo que nadie entiende) y por qué ahora.
`relates` con las specs cuyo código se toca; `covers: []`.

## Paso 1 — Tests de caracterización

1. Revisa qué tests cubren hoy el código afectado. Lo que no esté cubierto se cubre **antes** de
   tocarlo: entradas y salidas reales, errores, efectos (lo que se escribe, se llama o se emite).
   Para código sin tests y difícil de probar, un test de nivel superior (endpoint, comando,
   componente renderizado) que fije la salida vale más que ninguno.
2. Ejecútalos en el código **sin cambiar**: deben pasar. Uno que falla es un bug: ficha `/fix`.
3. Anota en "Tests de caracterización" qué fijan, sus rutas y la salida en verde. Commit de los
   tests solos.

## Paso 2 — Cambio

Pasos pequeños; tras cada uno, los tests de caracterización y los del módulo. Sin cambiar ningún
test de caracterización. `lane-check` sobre el diff. Describe el resultado en "Cambio".

## Paso 3 — Cierre

`../../shared/lanes.md` §4. Encargo de la review ligera:
- `git diff <base> -- <tests de caracterización>` vacío desde el commit de los tests.
- ¿Algún cambio de comportamiento observable? Mensajes de error, orden, formato, valores por
  defecto, tiempos de espera, lo que se registra en logs y auditoría.
- ¿El código queda más simple de verdad (no solo distinto)? ¿Quedó código muerto?
- ¿Nada de `../../shared/lanes.md` §3 en el diff, salvo tamaño aceptado?

Un refactor no entra al changelog de usuario.

## Paso 4 — Informe

Qué deuda se pagó, qué tests lo garantizan, resultado de la review y estado de la ficha.
