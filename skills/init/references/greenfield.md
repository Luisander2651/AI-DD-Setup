# Greenfield: proyecto base y auditoría de la plantilla

Lo usa `/init` (Fase 0 y Fase 3b) en proyectos nuevos. Sin proyecto base no hay comandos que
verificar, `/plan` no puede medir dependencias y `/implement` se detiene; por eso `/init` lo deja
creado o, si el usuario prefiere, lo convierte en la primera spec.

## 1. Andamiaje recién generado (Fase 0)

Si el repositorio tiene manifiesto pero todo el código salió de una plantilla (`ionic start`,
`npm create vite`, `create-next-app`, `dotnet new`, `cargo new`, `flutter create`, `rails new`…),
trátalo como **greenfield con andamiaje existente**, no como brownfield:

- Señales: ≤ 2 commits (o ninguno), los archivos de código coinciden con los de la plantilla
  (pantallas de ejemplo `Tab1`/`Home`, `App.test`, `main.ts` sin lógica propia) y no hay
  specs, docs ni tests escritos por el equipo.
- Pregunta en una línea: "Detecté un proyecto recién generado con <plantilla> — ¿lo trato como
  proyecto nuevo (recomendado) o como código existente?".
- Como proyecto nuevo: no lances los subagentes de exploración ni crees specs `inferred` del código
  de ejemplo; sigue con la entrevista. En el paso 2 no vuelvas a ejecutar el comando de la
  plantilla (ya se ejecutó), pero sí verifica sus dependencias en la tabla del ADR y fija y ejecuta
  los comandos reales; y haz el paso 3 (auditoría de la plantilla).

## 2. Crear el proyecto base (Fase 3b)

Tras la entrevista, con el stack decidido:

1. Propón el comando **oficial** de la plantilla del stack (el que documenta el framework) y la
   lista de dependencias que trae. Pregunta (opción múltiple):
   - **(a) Crearlo ahora en `/init`** (recomendado): es configuración, no comportamiento.
   - **(b) Primera spec `001-proyecto-base`**: cuando el andamiaje incluye decisiones que el usuario
     quiere revisar en plan y tareas (monorepo, varias apps, infraestructura).
2. Con (a):
   - Verifica las dependencias directas que añade la plantilla como pide
     `shared/agent-security.md` §2, en **una tabla** (paquete, versión, fecha de publicación de esa
     versión, licencia, repositorio, scripts de instalación) que va al ADR "Stack base". Instala con
     el modo que respeta la antigüedad mínima también en las transitivas (§2.2).
   - Ejecuta el comando con confirmación. Si el comando descarga la plantilla de un dominio que el
     entorno no alcanza, crea el equivalente con el gestor de paquetes y dilo.
   - Fija en `AGENTS.md` los comandos **reales** (instalar, dev, test, lint, type-check, build) y
     ejecútalos (Fase 4). Si la plantilla no trae tests o lint, añade los mínimos del stack y
     regístralos en el mismo ADR.
   - Commit propio (`chore: proyecto base`) para que la primera spec tenga una base limpia.
3. Con (b): deja los comandos como `TODO(init): los fija la spec 001` y crea la spec con
   `/specify`; su plan sigue esta guía.

## 3. Auditoría de la plantilla contra la constitución (siempre)

Los valores por defecto de una plantilla no los decidió nadie del proyecto y suelen contradecir
la constitución sin que ningún documento lo diga. Antes de cerrar `/init` (o en el plan de la spec
001), contrasta cada uno con la constitución, `docs/security.md` y las restricciones de la
entrevista, y regístralo en una tabla en `docs/architecture.md` → "Deuda técnica y riesgos":

| Valor de la plantilla | Dónde | Regla con la que choca | Acción |
|---|---|---|---|

Revisa como mínimo, según el tipo:

- **Todos:** versiones mínimas del runtime y del SO, scripts de instalación, telemetría activada por
  defecto, configuración de logs en modo debug, archivos de ejemplo que quedan en el build.
- **mobile:** `minSdkVersion`/`IPHONEOS_DEPLOYMENT_TARGET` frente a las versiones mínimas
  acordadas; permisos del manifiesto (las plantillas suelen traer `INTERNET`); copias de seguridad
  (`allowBackup`, `dataExtractionRules`, exclusión de iCloud); `FileProvider` y rutas expuestas;
  logging del puente nativo; tamaño de los controles frente a los objetivos de toque (p. ej. Ionic
  usa 32–36 px en Android); CSP del WebView.
- **frontend/fullstack:** contraste y tamaños por defecto del sistema de componentes, `lang` del
  documento, mapas de código fuente en producción, cabeceras de seguridad.
- **backend:** modo debug, CORS abierto, cabeceras, usuario y contraseña de ejemplo, migraciones de
  ejemplo.

Cada fila con acción "corregir" se convierte en una tarea con su test en la spec 001 (o en el
commit del proyecto base si es configuración pura con su comprobación ejecutada).
