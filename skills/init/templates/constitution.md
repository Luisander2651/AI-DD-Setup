---
version: 1.0.0
ratified: {{date}}
last_amended: {{date}}
status: draft   # draft hasta que el usuario la apruebe → approved
---

# Constitución de {{project_name}}

Principios innegociables. Toda spec, plan y tarea debe cumplirlos. `/plan` y `/tasks` incluyen un
**Constitution Check** que evalúa cada principio; un incumplimiento sin justificación bloquea.

## Principios

### P1. {{nombre}}
**Regla:** {{regla verificable}}
**Cómo se verifica:** {{test, lint, revisión, métrica}}
**Por qué:** {{motivo}}

<!-- repetir por principio -->

## Restricciones
- {{compliance, plataformas, presupuesto, performance}}

## Definición de terminado
- [ ] {{criterio}}

## Gobierno
- Cambiar esta constitución requiere subir `version` (SemVer: MAJOR elimina o redefine un
  principio, MINOR añade uno, PATCH aclara redacción) y registrar la enmienda abajo.
- Ante conflicto, la constitución prevalece sobre specs, planes y `AGENTS.md`.

## Enmiendas
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0.0 | {{date}} | Versión inicial | /init |
