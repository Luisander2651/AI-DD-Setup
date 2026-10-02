# Contratos y datos según el tipo de proyecto

Referencia de `/plan` Paso 3 (sección "Contratos y datos" del plan).

- `backend` / `fullstack`: endpoints o mensajes (método, ruta, request, response, errores),
  cambios de modelo de datos y migraciones (patrón expand → migrate → contract), permisos.
- `frontend` / `fullstack`: pantallas y componentes nuevos o modificados, estados (carga, vacío,
  error, éxito), manejo de estado, accesibilidad con objetivos medibles (roles y nombres, foco al
  abrir y cerrar diálogos, anuncios de errores y estados, tamaño de los objetivos según el nivel
  WCAG de la constitución; 44 pt/48 dp en `mobile`). Si `design` está en `skills.enabled`, añade
  la nota: "Revisar con el plugin `design` (`design:design-handoff`) antes de `/implement`". Con
  sistema de diseño (`design.status` `draft` o `approved`), sigue `design.md` de esta carpeta.
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
