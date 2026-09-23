---
name: clarify
description: Detecta ambigüedades y huecos en una spec en borrador y los resuelve con preguntas dirigidas, actualizando la spec. Úsala con /clarify NNN, antes de aprobar una spec o cuando una spec parezca vaga o incompleta.
---

# /clarify — Cerrar ambigüedades antes de planear

Paso opcional (recomendado) entre `/specify` y la aprobación de la spec:

```
/init → /specify → [/clarify] → /plan → /tasks → /analyze → /implement → /review → /release
```

> Antes de actuar, lee el contrato común del flujo: `../../shared/contract.md` (relativo a este
> archivo). Si algo aquí lo contradice, prevalece el contrato.

Una ambigüedad que llega a `/plan` se convierte en una suposición del agente; una que llega a
`/implement`, en código a reescribir. Esta skill encuentra las que más impacto tienen y las
resuelve con el usuario.

## Uso

```
/clarify <NNN|slug>
/clarify            # la spec en draft más reciente
```

## Reglas

- **Máximo 5 preguntas por sesión**, priorizadas por impacto. Si quedan más, dilo y sugiere otra
  ronda.
- Cada pregunta es de **opción múltiple** (2–4 opciones) con una opción **recomendada** y su motivo
  en una línea, o de respuesta corta (≤ 5 palabras) cuando no hay opciones naturales.
- **Sin tecnología:** igual que en `/specify`, las respuestas se escriben como comportamiento, no
  como implementación.
- **No preguntes lo que ya responde** la spec, la constitución, `docs/security.md` o el glosario.
- Solo modifica la spec indicada; su estado sigue siendo `draft` (o `inferred`).
- Escribe en el idioma del proyecto.

---

## Paso 0 — Precondiciones

1. La spec existe y está en `draft` o `inferred`. Si está `approved` o más, detente: los cambios
   van por `/specify --edit`.
2. Lee `.ai/project.yaml`, `docs/constitution.md`, `docs/security.md` y el glosario si existe.

## Paso 1 — Barrido de ambigüedades

Evalúa la spec en cada categoría y clasifícala como **Clara**, **Parcial** o **Faltante**:

| Categoría | Qué buscar |
|---|---|
| Alcance | Límites difusos, "Fuera de alcance" débil, historias que podrían ser dos features. |
| Actores y permisos | Quién puede hacer qué; roles no nombrados; qué pasa con usuarios no autenticados. |
| Datos | Entidades, campos clave, unicidad, volumen esperado, retención y borrado. |
| Estados y casos límite | Vacío, error, duplicado, concurrencia, cancelación, reintento, límites de tamaño. |
| Requisitos no funcionales | Adjetivos sin número ("rápido", "escalable", "seguro"): pide la métrica. |
| Seguridad y abuso | Datos sensibles sin clasificar, casos de abuso ausentes, qué se registra. |
| Integraciones | Sistemas externos, qué pasa si fallan o responden lento. |
| Experiencia y accesibilidad | Mensajes al usuario, flujos alternativos, requisitos de accesibilidad (frontend). |
| Terminología | Un mismo concepto con varios nombres, o términos que chocan con el glosario. |
| Verificabilidad | Criterios `CA` que no se pueden comprobar con un test o una observación. |

Incluye los marcadores `[NECESITA ACLARACIÓN]` y los "Supuestos" existentes como candidatos.

## Paso 2 — Priorización

Ordena los huecos por **impacto × incertidumbre**. Impacto alto = cambia el alcance, el modelo de
datos, la seguridad, la experiencia principal o la forma de probar. Descarta lo que se puede decidir
razonablemente en `/plan` sin riesgo (regístralo como supuesto si no lo está).

## Paso 3 — Preguntas

Haz las preguntas **de una en una** (o todas juntas si la herramienta de preguntas lo permite),
cada una con su recomendación. Tras cada respuesta, **actualiza la spec de inmediato**:

1. Escribe la respuesta en la sección que corresponde (criterio `CA` nuevo o corregido, requisito
   no funcional con número, fila de "Fuera de alcance", caso de abuso, etc.).
2. Elimina el marcador `[NECESITA ACLARACIÓN]` o el supuesto que resolvió.
3. Registra la pregunta al final de la spec:

   ```markdown
   ## Aclaraciones
   ### Sesión AAAA-MM-DD
   - P: <pregunta> → R: <respuesta>
   ```

Si el usuario responde "no sé" o "decide tú", toma la opción recomendada y regístrala en
"Supuestos" (no en Aclaraciones).

## Paso 4 — Verificación

1. Ejecuta `python .ai/bin/aidd.py validate docs/specs/NNN-<slug>` (o `python3`) y corrige los
   errores de formato.
2. Revisa que la spec no se contradiga tras los cambios (numeración de `CA`, alcance vs. fuera de
   alcance).

## Paso 5 — Informe

Muestra:
- Preguntas hechas y secciones actualizadas.
- Tabla de cobertura por categoría (Clara / Parcial / Faltante), antes y después.
- Huecos que quedan y si justifican otra ronda de `/clarify`.

Siguiente paso sugerido: aprobar la spec (vía `/specify --edit NNN` o confirmación directa) y
luego `/plan NNN`.
