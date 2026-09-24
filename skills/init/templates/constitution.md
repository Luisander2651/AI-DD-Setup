---
version: 1.0.0
ratified: {{date}}
last_amended: {{date}}
status: draft   # draft hasta que el usuario la apruebe → approved
---

# Constitución de {{project_name}}

Principios innegociables. Toda spec, plan y tarea debe cumplirlos. `/plan` y `/tasks` incluyen un
**Constitution Check** que evalúa cada principio; un incumplimiento sin justificación bloquea.

<!-- if brownfield -->

## Código previo
El código existente anterior a esta constitución que no cumple un principio **no bloquea** por sí
mismo: queda registrado como deuda en [roadmap.md](roadmap.md) y en las "Observaciones" de cada
spec. Los principios se exigen a todo código **nuevo o modificado**.
<!-- endif -->

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
