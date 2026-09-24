---
id: {{NNN}}
slug: {{slug}}
status: {{draft|inferred|approved|implemented|released}}
confidence: {{alta|media|baja}}   # solo si status=inferred
created: {{date}}
extends: []   # specs cuyo comportamiento cambia esta spec, p. ej. [005, 006]
---

# {{NNN}} · {{nombre de la feature}}

## Problema
{{qué necesidad resuelve y para quién}}

## Historias de usuario
- Como {{rol}}, quiero {{acción}} para {{beneficio}}.

## Criterios de aceptación
- [ ] CA1 · Dado {{contexto}}, cuando {{acción}}, entonces {{resultado}}.   <!-- numerar CA1, CA2… -->

## Fuera de alcance
- {{…}}

## Seguridad y privacidad
- Datos sensibles involucrados: {{ninguno · cuáles, según docs/security.md}}
- Quién puede hacer qué: {{rol → acción permitida / denegada}}
- Casos de abuso (cada uno con su criterio `CA` marcado `(abuso)`):
  - Como {{atacante o usuario malintencionado}}, intento {{acción}} → {{resultado esperado: se rechaza, se limita, se registra}}

<!-- if la feature toca datos sensibles, autenticación o permisos -->

## Auditoría
Eventos que deben quedar registrados, cada uno como criterio `CA` verificable:
- {{evento}} → registra {{actor, acción, recurso, resultado}} (ver `docs/observability.md`)
<!-- endif -->

## Requisitos no funcionales
- {{performance, seguridad, accesibilidad}}

## Preguntas abiertas
- [NECESITA ACLARACIÓN] {{…}}   <!-- máximo 3; con alguna abierta la spec no puede aprobarse -->

## Supuestos
- {{decisión razonable tomada sin preguntar, para revisión del usuario}}

## Notas para /plan
- {{preferencias técnicas mencionadas por el usuario; no son requisitos}}

## Evidencia (solo si status=inferred)
- Archivos: {{rutas}}
- Tests: {{rutas o "sin tests"}}

## Observaciones (solo si status=inferred)
Discrepancias, comportamiento aparentemente erróneo y deuda. Documentan lo que el código hace hoy;
no son requisitos.

## Historial
| Fecha | Cambio | Motivo |
|---|---|---|
