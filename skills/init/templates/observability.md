---
status: {{proposed|inferred|approved}}
updated: {{date}}
---

# Observabilidad y auditoría de {{project_name}}

Estado de cada capacidad: **presente** (instalada o declarada) · **configurada** (configurada para
este proyecto) · **en uso** (el código o la operación la ejercitan). Solo "en uso" cuenta como
cubierta.

## Resumen
| Capacidad | Herramienta | Estado | Evidencia |
|---|---|---|---|
| Logs de aplicación | {{…}} | {{presente · configurada · en uso}} | {{ruta}} |
| Agregación de logs | {{…}} | | |
| Correlación por petición | {{…}} | | |
| Registro de auditoría | {{…}} | | |
| Métricas | {{…}} | | |
| Trazas distribuidas | {{…}} | | |
| Alertas | {{…}} | | |

## Logs
- Formato: {{estructurado JSON · texto}}; campos obligatorios: `timestamp`, `level`,
  `request_id`, `actor_id` (si hay sesión), `message`, `context`.
- Nivel por entorno: local `debug` · staging `info` · producción {{info}}.
- Destino y retención: {{…}}.
- Qué **nunca** se registra: datos personales ({{teléfono, email, dirección…}}), datos de salud,
  contraseñas, tokens, secretos, cuerpos completos de petición. Cómo se enmascara: {{…}}.

## Correlación
- Identificador por petición: cabecera {{X-Request-Id}}; se acepta del cliente si es válido o se
  genera; se devuelve en la respuesta y se añade al contexto de todos los logs de la petición
  y de los trabajos en cola que dispare.

## Registro de auditoría
Separado de los logs técnicos: responde **quién hizo qué, sobre qué, cuándo y con qué resultado**.

| Evento | Obligatorio | Campos |
|---|---|---|
| Login exitoso y fallido | sí | actor (o identificador intentado), IP, resultado, fecha |
| Acceso denegado (401/403) | sí | actor, acción, recurso, fecha |
| Lectura de datos sensibles | {{sí}} | actor, recurso, fecha |
| Cambio de datos sensibles | {{sí}} | actor, recurso, campos cambiados (sin valores sensibles), fecha |
| Cambio de permisos o roles | sí | actor, sujeto, antes → después, fecha |
| {{…}} | | |

- Almacenamiento: {{tabla propia · servicio externo}}; **solo anexado** (nadie, tampoco un
  administrador, puede modificar o borrar entradas desde la aplicación).
- Retención: {{…}} (base legal: {{…}} · `TODO(init)` si no se conoce).
- Quién puede leerlo: {{…}}; cada lectura del registro también se audita.

## Métricas y alertas
| Métrica / alerta | Umbral | Canal |
|---|---|---|
| Tasa de errores 5xx | {{…}} | {{…}} |
| Logins fallidos por IP o cuenta | {{…}} | {{…}} |
| Latencia p95 | {{…}} | {{…}} |
| Cola de trabajos atascada | {{…}} | {{…}} |

## Brechas
<!-- En brownfield: lo que está presente pero no en uso, datos sensibles en logs, eventos de
     auditoría faltantes. Cada brecha con prioridad y enlace al objetivo del roadmap. -->
- {{…}}
