---
lane: refactor
status: done
base: 9c1d0e2
relates: [001]
covers: []
escalated_to: null
---

# Refactor: separar el almacenamiento del token del servicio de sesión

## Problema
`SessionService` mezcla la llamada de inicio de sesión con el acceso al almacenamiento seguro, y
cada test necesita simular los dos.

## Tests de caracterización
`src/app/core/session.service.spec.ts`: inicio correcto, credenciales inválidas y token manipulado.
En verde antes del cambio (3/3).

## Cambio
Nuevo `TokenStore` con la lectura y escritura del token; `SessionService` lo recibe inyectado.

## Escalado
`aidd.py lane-check`: no (3 archivos de código; `session` en el nombre se confirmó: no cambia
permisos ni el formato del token).

## Verificación
- Los tests de caracterización no cambiaron y siguen en verde; `npm test` en verde.
- Review ligera sin hallazgos.

## Decisiones
| Fecha | Tipo | Pregunta / conflicto | Decisión | Fuente |
|---|---|---|---|---|
| 2026-10-12 | supuesto | `lane-check` marca "seguridad?" por el nombre `session` | Sigue en el carril: no cambia permisos ni formato del token | usuario |
