# Carriles ligeros: procedimiento común

Lo siguen `/fix` (y `/fix --hotfix`), `/refactor` y `/chore`. Las reglas están en
`shared/contract.md` → "Carriles"; aquí, cómo se aplican. Si algo de aquí contradice el contrato,
prevalece el contrato.

## 1. Arranque

1. Lee `.ai/project.yaml`, `docs/constitution.md`, `docs/security.md`, `AGENTS.md` (comandos de
   test, lint y build) y las specs que el cambio toca. Si falta `.ai/project.yaml`, el proyecto no
   usa el flujo: haz el cambio con las mismas buenas prácticas (test primero) sin ficha y dilo.
2. **Triaje.** Antes de escribir nada, decide si el cambio cabe en el carril (§3). Si claramente
   no cabe (es una feature, cambia un contrato), dilo y propone `/specify` sin crear ficha.
3. **Ficha.** Crea `docs/changes/AAAA-MM-DD-<carril>-<slug>.md` desde `docs/templates/change.md`
   (o `skills/init/templates/change.md` del plugin si el proyecto aún no la tiene) con
   `status: open`, `base: <commit actual abreviado>`, `relates` y, en `/fix`, `covers`. Borra las
   secciones que no son del carril y escribe "Problema". Es lo primero que se escribe: con la
   ficha abierta el hook deja editar código (contrato → "Carriles").
4. **Git.** Si hay cambios sin commitear ajenos, pregunta antes de seguir. En la rama principal,
   propone una rama `<carril>/<slug>` (o la convención de `AGENTS.md`). Política de commits como
   en `/implement` Paso 0.7, con `<tipo>(<carril>-<slug>): <qué>` y `Ficha: <ruta>` en el cuerpo.
5. **Línea base.** Corre la suite una vez; los tests que ya fallaban se anotan en "Verificación" y
   no deben aumentar.
6. `python .ai/bin/aidd.py lane-check <ficha> --files <archivos previstos>` (intérprete según el
   contrato) y anota el resultado en "Escalado".

## 2. Durante el cambio

- **Solo lo que pide el carril.** Nada de "ya que estoy": otro bug visto es otra ficha; una mejora
  es una spec. Si lo visto es de la misma ficha, pregunta en ese momento (hallazgo colateral).
- Mismas reglas de código que `/implement`: convenciones de `AGENTS.md`, código seguro por defecto
  (`shared/security-checklist.md`), seguridad del agente (`shared/agent-security.md`), nunca
  debilitar un test, tests nuevos de UI, e2e o asíncronos ejecutados dos veces.
- Si `security.tools.secrets` o `sast` están `instalada` o `en-ci`, córrelos sobre lo tocado.
- **3 intentos** sin éxito: detente y reporta qué se intentó, el error y tu hipótesis; deja en la
  ficha `- bloqueo: AAAA-MM-DD — <qué falta> — <skill>` bajo "Cambio".

## 3. Escalado

Escala al flujo completo si se cumple **cualquiera** (el script ve 2–7; el 1 lo decides tú):

1. El cambio **añade o cambia comportamiento** (no lo define ninguna spec, o lo contradice).
2. Contrato público: API, eventos, esquemas, interfaz pública de una `library`.
3. Datos: migraciones, modelos persistidos, formato de lo guardado.
4. Seguridad: autenticación, permisos, datos sensibles, rutas protegidas.
5. Dependencia **nueva** (subir la versión de una existente no cuenta).
6. Tokens o componentes del sistema de diseño.
7. Más de `workflow.lanes.max_files` archivos de código (por defecto 5; sin tests ni docs).

Con algún motivo, pregunta: **escalar** (recomendado) o seguir con aceptación explícita. Si sigue,
regístralo en "Decisiones" como `supuesto` con la fuente `usuario`. `seguridad?` es una sospecha
por el nombre del archivo: confírmala mirando el cambio antes de preguntar.

**Al escalar:** la ficha pasa a `status: escalated` con `escalated_to: NNN` cuando `/specify` crea
la spec; su "Problema" y "Reproducción" son el punto de partida de la spec (con `extends` si toca
specs cerradas) y el test que falla, si ya existe, se conserva para su `tasks.md`.

## 4. Cierre

1. `lane-check <ficha>` otra vez, ahora sobre el diff real desde `base`. Un motivo nuevo se trata
   como en §3 antes de cerrar.
2. **Review ligera** (no en `/chore`): un solo subagente con **solo** el diff desde `base`
   (`git diff <base>`), la ficha y el texto de los criterios de `covers`. Encargo según el carril
   (lo dice cada skill). Devuelve hallazgos con ubicación, impacto y corrección. Los bloqueantes se
   corrigen; los menores se corrigen o se aceptan con motivo en "Decisiones". El resultado va en
   "Verificación" (no hay `review.md`).
3. Suite completa, lint y type-check; resultado en "Verificación".
4. `status: done`, `python .ai/bin/aidd.py validate` sin errores y commit final.
5. **Informe** (corto): qué se cambió, test que lo prueba, resultado de la review y cómo se libera
   (con la siguiente `/release`, o `/release --changes` si urge).

## 5. Ficha retroactiva

Si el cambio ya se hizo fuera del flujo (lo detecta `/sync` o lo dice el usuario), crea la ficha
con `base` en el padre del primer commit, rellena las secciones con lo que muestra el diff y
pregunta lo que no se puede deducir (síntoma, causa). En `/fix`, si no hay test que pruebe el
arreglo, escríbelo ahora y comprueba que falla con el arreglo revertido. Cierra con §4.
