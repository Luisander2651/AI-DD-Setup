# {{project_name}}

{{descripción en 2–3 frases: qué es, para quién, etapa actual}}

> Antes de cualquier cambio lee [docs/constitution.md](docs/constitution.md). Si algo aquí
> contradice la constitución, prevalece la constitución.

## Stack
{{lenguajes, frameworks, base de datos, gestor de paquetes}} · tipo: `{{type}}`

## Comandos
```bash
{{install}}     # instalar
{{dev}}         # desarrollo local
{{test}}        # tests
{{lint}}        # lint
{{build}}       # build
```

## Flujo de trabajo
1. `/specify` → spec en `docs/specs/NNN-<slug>/spec.md`
2. `/plan` → `plan.md` con Constitution Check
3. `/tasks` → `tasks.md`
4. `/analyze` → verificación independiente de consistencia → `analysis.md`
5. `/implement` → solo tareas aprobadas, una a la vez, con tests
6. `/review` → contra spec, plan y constitución → `review.md`
7. `/release` → versión, changelog, staging y, con tu aprobación, producción

Usa `/clarify` para cerrar ambigüedades de una spec antes de aprobarla. Estado de todas las specs:
`python .ai/bin/aidd.py status`.

No implementes sin spec aprobada. No hagas commit sin que pasen `{{test}}` y `{{lint}}`.
Nunca despliegues a producción sin aprobación explícita; sigue [docs/deployment.md](docs/deployment.md).
Nunca escribas secretos en el código, los logs ni los docs.

## Reglas y estilo
- {{convención 1: naming, estructura}}
- {{convención 2: manejo de errores, patrones}}
- Commits: {{convención}}

## Mapa del repositorio
| Ruta | Contenido |
|---|---|

## Documentación
- [Constitución](docs/constitution.md) — principios innegociables
- [Arquitectura](docs/architecture.md)
- [Despliegue](docs/deployment.md) — entornos, deploy y rollback
- [Seguridad](docs/security.md) — datos sensibles, auth, herramientas y excepciones
- [Roadmap](docs/roadmap.md) — etapa actual y objetivos
- [Specs](docs/specs/README.md)
- [ADRs](docs/adr/)
- [Plantillas](docs/templates/)
