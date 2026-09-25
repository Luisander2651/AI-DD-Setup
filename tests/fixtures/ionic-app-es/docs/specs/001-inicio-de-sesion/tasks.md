---
spec: 001-inicio-de-sesion
status: approved
---
# Tareas
- [x] T001 Tests que fallan — `src/app/login/login.spec.ts`, `src/app/core/secure-storage.spec.ts` — hecho cuando: fallan por la razón esperada (TM1) — cubre: CA1, CA2, CA3
- [x] T002 Guardar el token con almacenamiento seguro — `src/app/core/auth.service.ts` — hecho cuando: secure-storage.spec.ts pasa — cubre: CA2 — depende: T001
  - nota: A2 — el plugin de almacenamiento seguro se inicializa antes del login
- [ ] T003 Rechazar token manipulado — `src/app/core/auth.interceptor.ts` — hecho cuando: login.spec.ts pasa — cubre: CA1, CA3 — depende: T002

- [ ] T090 Actualizar `docs/architecture.md` — hecho cuando: refleja el cambio
- [ ] T091 Actualizar `docs/deployment.md` — hecho cuando: refleja el cambio
- [ ] T092 Marcar la spec como implementada — hecho cuando: status implemented
- [ ] T095 Publicar en el canal de pruebas
- [ ] T096 Aprobación humana para producción
- [ ] T097 Publicación escalonada en tiendas
- [ ] T098 Marcar spec como `released`
