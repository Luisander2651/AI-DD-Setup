---
name: fix
description: Corrige un bug sin pasar por spec, plan y tareas - test que falla, causa raíz, arreglo mínimo y review ligera - dejando una ficha en docs/changes/. Con --hotfix, para un incidente en producción, además libera con la misma aprobación humana. Úsala con /fix o /fix --hotfix, o cuando el usuario pida arreglar un error, un fallo o un comportamiento que no cumple lo especificado.
---

# /fix — Corregir un bug

Carril ligero para lo que **ya debería funcionar**: el comportamiento correcto está en una spec, o
es un defecto evidente (excepción, caída, dato corrupto, error de cálculo). No sirve para añadir ni
cambiar comportamiento: eso es `/specify`.

> Antes de actuar, lee `../../shared/contract.md` → "Carriles" y el procedimiento común
> `../../shared/lanes.md` (relativos a este archivo). Si algo aquí los contradice, prevalece el
> contrato.

## Uso

```
/fix <descripción del bug>            # ficha nueva
/fix --hotfix <descripción>           # incidente en producción: arreglo + release inmediato
/fix --continue [<ficha>]             # retoma una ficha abierta
/fix --retro <commit|rango>           # ficha retroactiva de un arreglo ya hecho (lanes.md §5)
```

## Reglas

- **Test primero, siempre.** Ningún arreglo sin un test que falle antes por la razón del bug y
  pase después. Si el bug no se puede reproducir con un test automático (solo en un dispositivo,
  solo en producción), la reproducción manual se escribe paso a paso en "Reproducción" y se
  confirma con el usuario; aun así, añade el test más cercano posible (unidad del cálculo, parser).
- **Causa raíz antes que arreglo.** Un arreglo que solo esconde el síntoma (un `try` que traga el
  error, un `if` para el caso exacto del reporte) no es arreglo: se rechaza en la review.
- **Arreglo mínimo.** Nada de refactor "de paso": eso es `/refactor` aparte.
- **Escala** cuando `../../shared/lanes.md` §3 lo dice.

---

## Paso 0 — Arranque

`../../shared/lanes.md` §1 con carril `fix` (`hotfix` con `--hotfix`, ver Paso 5). En el triaje,
busca qué spec define el comportamiento esperado:
- Lo define una spec → `relates: [NNN]` y `covers` con los criterios que hoy no se cumplen.
- No lo define ninguna, pero es un defecto evidente → `relates: []`; regístralo en "Decisiones"
  como `implícita` (fuente: el síntoma) o pregunta si dudas.
- No lo define ninguna y hay que **decidir** cómo debería ser → no es un fix: escala (§3, motivo 1).
- El reporte contradice una spec (el usuario quiere otra cosa de lo especificado) → `contradicción`:
  la resuelve el usuario y, si cambia lo especificado, es `/specify` con `extends`.

## Paso 1 — Reproducción

1. Escribe el test en el lugar y con las convenciones de los tests vecinos.
2. Ejecútalo y confirma que **falla por la razón del bug** (no por un import o un dato de prueba
   mal puesto). Copia la línea relevante de la salida a "Reproducción".
3. Si el test pasa, el bug no es lo que se pensaba: vuelve al reporte o pide más datos. No sigas
   con un test que no reproduce nada.

## Paso 2 — Causa raíz

Lee el código implicado, la historia del archivo (`git log -p` del tramo) y, si hace falta, añade
trazas temporales que retirarás. Escribe en "Causa raíz" **por qué** pasa, no solo dónde. Si la
causa está en otro módulo o es de diseño (el plan de la spec lo decidió así), dilo: puede que el
arreglo correcto ya no quepa en el carril.

## Paso 3 — Arreglo

El cambio mínimo que ataca la causa. Después: el test nuevo en verde, los del módulo en verde, y
`lane-check` sobre el diff (`../../shared/lanes.md` §3). Describe el cambio en "Cambio".

## Paso 4 — Cierre

`../../shared/lanes.md` §4. Encargo de la review ligera:
- Revierte **solo el código** del arreglo (no el test) en una copia o con `git stash` del código,
  ejecuta el test y confirma que falla; restaura y confirma que pasa.
- ¿La causa raíz explica el síntoma? ¿El arreglo ataca la causa o tapa el síntoma?
- ¿Hay otros sitios con el mismo defecto (mismo patrón copiado)? Si los hay, son de esta ficha
  (pregunta) o fichas nuevas.
- ¿Nada de `../../shared/lanes.md` §3 en el diff?

## Paso 5 — Hotfix (`--hotfix`)

Para un incidente en producción. Lo acelerado es que no espera a otras specs ni pasa por
`/analyze`; **nada** de las reglas de producción se relaja.

1. Lee `docs/deployment.md` → "Hotfix". Si falta, detente y pide completarla (rama, si hay
   staging, cómo vuelve a la rama principal); no improvises el procedimiento.
2. Crea la rama desde el tag que está en producción, según esa sección.
3. Pasos 0–4 con `lane: hotfix`. Si el arreglo escala, no hay hotfix: propón mitigar
   (`/release --rollback`, desactivar el flag) y llevar el arreglo por el flujo completo.
4. `/release --changes <ficha>` con todas sus reglas: puerta de seguridad, versión patch,
   aprobación humana escrita para producción, verificación post-deploy.
5. Integra la rama del hotfix en la principal según `docs/deployment.md` y confirma que el test
   nuevo sigue ahí.

## Paso 6 — Informe

Una línea por punto: el bug y su causa, el test que lo prueba, el resultado de la review, el
estado de la ficha y cómo se libera.
