---
spec: 001-inicio-de-sesion
status: approved
---
# Plan
## Constitution Check
| Principio | Resultado |
|---|---|
| P1 | ✅ |
| P2 | ➖ |
## Modelo de amenazas
| ID | Amenaza | Control | Test |
|---|---|---|---|
| TM1 | Token manipulado | Validación en backend + cierre de sesión | login.spec.ts |
## Trazabilidad
| Elemento | Test |
|---|---|
| CA1 | login.spec.ts |
| CA2 | secure-storage.spec.ts |
| CA3, TM1 | login.spec.ts |
## Observabilidad
Sin datos personales en los logs del dispositivo.
## Rollout
TestFlight y prueba interna de Play; publicación escalonada 10 % → 100 %; flag remoto.
