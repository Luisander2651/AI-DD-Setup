# Contratos y datos según el tipo de proyecto

Referencia de `/plan` Paso 3 (sección "Contratos y datos" del plan).

- `backend` / `fullstack`: endpoints o mensajes (método, ruta, request, response, errores),
  cambios de modelo de datos y migraciones (patrón expand → migrate → contract), permisos.
- `frontend` / `fullstack`: pantallas y componentes nuevos o modificados, estados (carga, vacío,
  error, éxito), manejo de estado, accesibilidad con objetivos medibles (roles y nombres, foco al
  abrir y cerrar diálogos, anuncios de errores y estados, tamaño de los objetivos según el nivel
  WCAG de la constitución; 44 pt/48 dp en `mobile`). Si `design` está en `skills.enabled`, añade
  la nota: "Revisar con el plugin `design` (`design:design-handoff`) antes de `/implement`". Con
  sistema de diseño (`design.status` `draft` o `approved`), sigue el diseño aprobado de la spec (`docs/specs/NNN-<slug>/design.md`, hecho con `/design-spec`).
- **Si cambian permisos o roles** y hay interfaz: una tabla **"Qué ve cada rol"** por pantalla
  afectada (saludos y textos, menús, columnas, botones y enlaces, estados vacíos). Ocultar un
  control no basta: los textos que prometen una acción ("gestiona", "ver y editar"), las columnas
  que quedan vacías y los mensajes pensados para otro rol también cambian, y cada fila lleva su
  test. Es la fuente habitual de hallazgos de `/review` en specs de control de acceso.
- `fullstack` / `monorepo`: dónde vive el contrato compartido y cómo se regenera.
- `mobile`: pantallas y estados como en `frontend`, más permisos del dispositivo nuevos (y su texto
  de justificación en `Info.plist`/`AndroidManifest`), plugins nativos, datos guardados en el
  dispositivo (dónde y si son sensibles), comportamiento offline y **compatibilidad con versiones
  instaladas**: un cambio de API o de datos locales debe funcionar con la versión anterior de la
  app, que seguirá en uso semanas. En Rollout: canal de pruebas, porcentaje de publicación
  escalonada, flag remoto para apagar la feature (una app publicada no se puede retirar) y, si hay
  actualizaciones en vivo, qué cambios pueden ir por ahí (solo capa web, sin cambios nativos).
  **Sin backend no hay flag remoto:** dilo en Rollout, cita el riesgo `RD` correspondiente de
  `docs/deployment.md` (o propónlo) y compensa con publicación escalonada obligatoria y una prueba
  de actualización desde la versión anterior instalada. En el modelo de amenazas, mapea cada
  amenaza también a su control MASVS (`MASVS-STORAGE`, `-PLATFORM`, `-PRIVACY`…), no solo al
  OWASP Top 10.
- `library`: cambios en la API pública y su impacto en SemVer (patch, minor o major).

## Sitio indexable (`seo.indexable: true`)

Sección "Descubribilidad", según `docs/seo.md` y `../../../shared/seo-checklist.md`:
- **Una fila por ruta nueva o modificada** (o por plantilla de ruta: `/blog/[slug]/`): indexable o
  no (con motivo), título y descripción (o de dónde salen, si vienen de datos), canónica absoluta
  desde `seo.site_url`, si entra al sitemap, datos estructurados (tipo de schema.org que describe
  lo visible, sin datos inventados) y su test.
- **Valores exactos y su origen** de los metadatos comunes: `og:site_name`, `og:locale` (y
  alternativos), campos del JSON-LD, `theme-color` (= `--color-bg`) e íconos, para que los tests
  comparen valores y no solo presencia.
- **Exclusiones deliberadas** de la spec (p. ej. sin `twitter:*`) con motivo, coherentes con
  `docs/seo.md`.
- **Tests sobre el HTML generado** (la build o la respuesta del servidor), no sobre el componente
  aislado: una sola canónica, título y descripción únicos entre rutas, un solo `h1`, JSON-LD que se
  parsea, la ruta en el sitemap o con `noindex` según su fila. Cada requisito de descubribilidad
  de la spec va a Trazabilidad como `RNF:` con su test.
- **Renderizado:** una ruta indexable nueva usa el `seo.rendering` del proyecto. Cambiarlo (p. ej.
  pasar rutas de una SPA a prerenderizadas) es una decisión → ADR, con su prueba de concepto
  (Paso 1b) si el framework aún no lo hace en el proyecto.
- **Lo que solo se comprueba en producción** (vista previa real al compartir, validador de
  resultados enriquecidos) va como `verificación manual:` a T095.
- Si la spec atiende brechas `SE`, cita cada corrección dentro o fuera, como cualquier riesgo.
