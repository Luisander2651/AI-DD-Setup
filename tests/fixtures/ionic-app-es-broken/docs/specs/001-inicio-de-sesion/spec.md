---
status: approved
---
# Inicio de sesión en la app
## Problema
El token se guarda en `localStorage`. Esta spec atiende RS1 parcialmente.
## Criterios de aceptación
- [ ] CA1 El usuario inicia sesión con correo y contraseña
- [ ] CA2 El token se guarda en almacenamiento seguro del sistema
- [ ] CA3 (abuso) Un token manipulado se rechaza y cierra la sesión
## Fuera de alcance
Biometría.
## Seguridad y privacidad
Credenciales y token de sesión.
## Auditoría
- Inicio de sesión fallido: se registra en el backend.
## Cobertura de riesgos
| Corrección | Alcance | Criterios / motivo y destino |
|---|---|---|
| RS1.a | dentro | CA2 |

## Historial
| Fecha | Cambio | Origen |
|---|---|---|
| 2026-09-28 | Creada; cubre el riesgo 1 en parte | /specify |
