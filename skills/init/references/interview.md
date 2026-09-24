# Guía de entrevista

Hasta 4 preguntas por ronda; omite las rondas o preguntas cuya respuesta ya conozcas. Opción múltiple siempre que se pueda; el usuario siempre
puede escribir su propia respuesta. En brownfield, cada pregunta arranca con lo inferido
("Detecté X — ¿correcto?").

**Configuración no versionada:** antes de la primera ronda, reúne los puntos "No determinado"
de la exploración que dependan de valores reales de `.env` o del entorno (canal y nivel de log,
`APP_ENV`, `APP_DEBUG`, driver de colas y de caché, hosts de servicios). No son secretos:
pregúntalos en una sola pregunta de respuesta libre ("¿qué valores tienen en tu entorno local y en
producción?"). Nunca pidas valores de contraseñas, claves o tokens. Con la respuesta, confirma o
descarta las brechas que dependían de ellos.

**Ronda 1 — Identidad**
1. ¿Qué problema resuelve el proyecto y para quién? (texto libre, 1–3 frases)
2. Tipo: frontend · backend · fullstack · monorepo · library.
3. Stack (greenfield: proponer 2–3 opciones coherentes con el tipo; brownfield: confirmar).
4. Etapa: prototipo · MVP · producción · mantenimiento.
**Ronda 2 — Reglas**
1. Principios innegociables: presenta el borrador según tipo (tabla de la Fase 3) más los
   universales de abajo; el usuario marca cuáles conservar y añade los suyos.
2. Testing: TDD obligatorio · tests por feature antes de merge · solo críticos · por definir.
3. Definición de terminado: tests pasan · lint limpio · docs actualizadas · revisión humana (multi).
4. Restricciones: compliance (GDPR, HIPAA, PCI), performance, presupuesto, plataformas objetivo.
**Ronda 3 — Despliegue** (obligatoria salvo `deploy.strategy: none`; en `library`,
"desplegar" = publicar en el registro: npm, PyPI, crates.io…)
1. Entornos: solo local · dev + prod · dev + staging + prod · otro.
2. Plataforma y disparador: ¿dónde corre y qué dispara un deploy (push, tag, manual)?
3. Aprobación de producción: ¿quién la da? (por defecto: el usuario, siempre explícita).
4. Rollback: ¿cómo se revierte hoy? (redeploy de la versión anterior · revert + pipeline ·
   no existe → se registra como riesgo y se propone uno).
**Ronda 4 — Seguridad** (obligatoria)
1. Datos sensibles que maneja el proyecto: ninguno · datos personales · financieros · salud ·
   credenciales de terceros (multi).
2. Autenticación: sin usuarios · sesión propia · JWT · OAuth/OIDC con proveedor externo.
3. Nivel ASVS objetivo: 1 (básico, la mayoría de apps) · 2 (datos sensibles o negocio crítico,
   recomendado) · 3 (alto riesgo: salud, finanzas, infraestructura).
4. Herramientas: proponer un set según el stack (secretos, SAST, SCA, contenedores); el usuario
   confirma cuáles adoptar. Registrar los comandos en `docs/security.md` y `.ai/project.yaml`.

**Ronda 5 — Observabilidad y auditoría** (obligatoria salvo `library`)
1. Eventos que **deben** quedar registrados (multi): logins exitosos y fallidos · accesos
   denegados · lecturas de datos sensibles · cambios de datos sensibles · cambios de permisos y
   roles · acciones administrativas · exportaciones.
2. ¿Hay obligación legal o contractual de registrar accesos a datos personales o de salud?
   Si la hay, ¿cuánto tiempo se conservan los registros? (no se sabe → `TODO(init)` y riesgo).
3. ¿Quién puede leer los registros de auditoría y cómo se protegen contra modificación?
   (solo administradores · equipo de seguridad · almacenamiento de solo anexado · por definir).
4. Nivel de log por defecto en producción e identificador de correlación por petición
   (proponer `info` y cabecera `X-Request-Id` devuelta en la respuesta).

**Ronda 6 — Operación** (solo si falta información)
1. Convenciones de ramas y commits (proponer Conventional Commits si no hay).
2. Versionado y changelog (proponer SemVer + `CHANGELOG.md` si no hay).
3. Próximos 3 objetivos (→ roadmap).
4. En brownfield con > 15 features: cuáles documentar ahora.
**Principios universales sugeridos** (el usuario decide; todos deben ser verificables):
- Ninguna implementación sin spec aprobada en `docs/specs/`.
- Todo cambio de comportamiento lleva test que falla antes y pasa después.
- No se introducen dependencias nuevas sin registrarlas en un ADR.
- Secretos nunca en el repositorio.
- Toda decisión arquitectónica que contradiga `docs/architecture.md` requiere un ADR.
- Ningún deploy a producción sin aprobación humana explícita.
- Nada llega a producción sin pasar por staging (si existe staging).
- Todo cambio desplegable tiene un plan de rollback probado o documentado.
- Las migraciones son compatibles con la versión anterior del código (expand → migrate → contract).
- Toda autorización se verifica en el servidor; ningún endpoint nuevo sin control de acceso explícito.
- Toda entrada externa se valida en el servidor; consultas siempre parametrizadas.
- Ninguna vulnerabilidad crítica o alta llega a producción sin excepción aprobada y con fecha de
  vencimiento en `docs/security.md`.
- Toda feature que toca datos sensibles o autenticación tiene modelo de amenazas en su plan.
- Los accesos y cambios a datos sensibles, los logins (incluidos los fallidos) y los accesos
  denegados se registran como eventos de auditoría con actor, acción, recurso, resultado y fecha.
- Cada petición lleva un identificador de correlación presente en sus logs y en la respuesta.
- Ningún log contiene datos personales, de salud, credenciales ni tokens; nivel por defecto `info`
  en producción.

Rechaza principios no verificables ("código limpio", "buen rendimiento") y propón una versión
medible ("funciones ≤ 50 líneas salvo justificación", "p95 < 300 ms en endpoints públicos").
