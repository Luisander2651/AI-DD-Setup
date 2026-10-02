# Tipos de proyecto

Referencia de `/init`: cómo se detecta el tipo (Fase 0) y qué incluye cada uno (Fase 3).

## 1. Detección (Fase 0, paso 4)

En brownfield infiérelo y pide confirmación; en greenfield pregúntalo. Señales:

- Frontend: `react`, `vue`, `svelte`, `angular`, `next`, `vite`, carpetas `components/`, `pages/`.
- Backend: `express`, `fastapi`, `django`, `spring`, `gin`, `nestjs`, carpetas `routes/`, `controllers/`, `migrations/`.
- Fullstack: señales de ambos en un mismo paquete, o meta-frameworks con servidor (Next con API routes, Remix, Nuxt server, Laravel con vistas).
- Monorepo: `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, `workspaces` en `package.json`, varios manifiestos. En monorepo, registra el tipo **por paquete**.
- Mobile: `ionic.config.json`, `capacitor.config.*`, `@ionic/*`, `@capacitor/*`, `react-native`,
  `expo`, `pubspec.yaml` con `flutter`, carpetas `android/` e `ios/`. Una app híbrida (Ionic,
  Capacitor) es `mobile` aunque su código sea web; si además tiene backend propio en el mismo
  repo, es `monorepo` con un paquete `mobile`.
- Library: sin punto de entrada de app, con `exports`/`main` publicable o `[project]` sin servidor.

## 2. Secciones condicionales (Fase 3)

Aplica según `project.type` (en monorepo, por paquete):

| Tipo | Arquitectura incluye | Constitución propone | Skills habilitadas |
|---|---|---|---|
| frontend | Componentes, estado, routing, design tokens, accesibilidad | WCAG AA, componentes con tests, sin lógica de negocio en vistas, preview por PR | `design` |
| backend | API (contratos), modelo de datos, migraciones, observabilidad, seguridad | Contrato de API antes de implementar, migraciones reversibles y compatibles con la versión anterior, logs estructurados con correlación, auditoría de accesos a datos sensibles, health check | — |
| fullstack | Ambas + **contrato entre capas** (tipos compartidos, versionado de API) | Unión de ambas + el contrato es la fuente de verdad entre capas | `design` |
| mobile | Pantallas y navegación, estado, almacenamiento local y offline, permisos del dispositivo, plugins nativos, versiones mínimas de SO, contrato con el backend, actualizaciones (tiendas, en vivo, forzada) | OWASP MASVS L1; tokens y datos sensibles solo en almacenamiento seguro del sistema (Keychain/Keystore), nunca en `localStorage`/Preferences; permisos mínimos y justificados; accesibilidad de la plataforma; claves de firma fuera del repo; compatibilidad con versiones de la app ya instaladas (la API no rompe clientes antiguos); objetivos de toque ≥ 44 pt/48 dp | `design` |
| library | API pública, compatibilidad, versionado semántico | SemVer estricto, API pública documentada y testeada, publicación solo desde CI con tag | — |

Las skills no se cargan ni descargan desde aquí: se registran en `.ai/project.yaml → skills.enabled`.
`design` es el plugin oficial `design` de Anthropic, no una skill de este plugin
(`../../../shared/contract.md` → "Dependencias externas"): pregunta si está instalado y regístrala solo
si el usuario lo confirma; si no, deja la lista vacía y anota en `AGENTS.md` que la revisión de
diseño la hace cada skill por su cuenta.
Cada skill condicional debe comprobar ese archivo al activarse (ver `../../../shared/contract.md`).
