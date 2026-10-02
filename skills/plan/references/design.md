# Diseño en `/plan`

Aplica a specs con interfaz cuando `.ai/project.yaml → design.status` es `draft` o `approved`.
Formato del sistema y de los HTML: `../../init/references/design.md` (§2.4 y §5) y
`../../init/templates/design/`.

## 1. Spec que usa el sistema (lo habitual)

En "Contratos y datos":
- Cada pantalla, con los **componentes del sistema** que usa y sus estados (vacío, carga, error,
  éxito). Ningún valor visual nuevo: si falta algo (un componente, una variante, un token), va a
  la subsección **"Cambios a incorporar al sistema"** del plan, con el valor propuesto y el motivo.
- Si hay "Cambios a incorporar al sistema", la **primera tarea** de `/tasks` actualiza
  `docs/design/system.md` y `system.html` (con su entrada en "Decisiones") antes del código.
- Si `design` está en `skills.enabled`, añade la nota: "Revisar con `design:design-handoff` antes de
  `/implement`" y usa `design:ux-copy` para textos de error, estados vacíos y confirmaciones.
- En Trazabilidad, cada criterio visual lleva `verificación manual: <pantalla> a <design.widths>
  contra system.html` (o contra el HTML de la spec del §2).

## 2. Spec de rediseño o con pantallas que el sistema no cubre

Un rediseño **siempre** es una spec propia; `/init` nunca lo hace. Antes del Paso 3 del plan:

1. Brief en modo spec (`../../init/references/design.md` §5) con el contenido real de la spec.
2. Opciones en `docs/specs/NNN-<slug>/design/opcion-<a|b|c>.html` desde `option.html`: **3 por
   defecto, 2 si se mantiene la marca**; con la skill `design` si la sesión la ofrece (el canvas se
   enlaza en el plan), siempre también en HTML. Mismas reglas que en `/init`: distintas de verdad,
   contraste sin ningún "no cumple", sin clichés de `docs/design/anti-cliches.md`.
3. El usuario elige; la elección va a "Decisiones" del plan (tipo `diseño`).
4. "Cambios a incorporar al sistema" recoge todo lo que cambia de `system.md` (tokens, componentes,
   pantallas) y la primera tarea lo aplica, subiendo `version` de `system.md`.
5. **Migración por pantalla:** una tarea por pantalla (o grupo pequeño), cada una con su
   `verificación manual:` contra el HTML elegido y el test de "solo tokens". Las pantallas no
   migradas siguen funcionando con el sistema anterior hasta su tarea; si conviven dos versiones de
   tokens, dilo en Rollout y en Riesgos.
6. Si el rediseño cambia la dirección creativa, `creative-direction.md` se actualiza en la misma
   primera tarea, con aprobación del usuario.
