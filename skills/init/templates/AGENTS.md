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
   - Con pantallas: `/design-spec NNN` → 2–3 composiciones y `design.md` aprobado
2. `/plan` → `plan.md` con Constitution Check
3. `/tasks` → `tasks.md`
4. `/analyze` → verificación independiente de consistencia → `analysis.md`
5. `/implement` → solo tareas aprobadas, una a la vez, con tests
6. `/review` → contra spec, plan y constitución → `review.md`
7. `/release` → versión, changelog, staging y, con tu aprobación, producción

Trabajo que no añade comportamiento (carriles ligeros, ficha en `docs/changes/`): `/fix` para un
bug (`--hotfix` en producción), `/refactor` para deuda sin cambio de comportamiento, `/chore` para
dependencias, configuración y docs. Si el cambio crece o toca contratos, datos o seguridad, pasa
al flujo completo. `/sync` concilia lo que se hizo fuera del flujo.

Usa `/clarify` para cerrar ambigüedades de una spec antes de aprobarla. Sistema de diseño:
`/design-spec system`. Sitio público: `/seo audit` para re-auditar el SEO técnico. Estado de todas las specs:
`python .ai/bin/aidd.py status`.

No implementes sin spec aprobada o ficha abierta de un carril. No hagas commit sin que pasen `{{test}}` y `{{lint}}`.
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
- [Observabilidad](docs/observability.md) — logs, correlación, auditoría, métricas y alertas
- [SEO técnico](docs/seo.md) — URL canónica, rutas indexables y brechas (solo sitios públicos)
- [Roadmap](docs/roadmap.md) — etapa actual y objetivos
- [Specs](docs/specs/README.md)
- [ADRs](docs/adr/)
- [Plantillas](docs/templates/)
