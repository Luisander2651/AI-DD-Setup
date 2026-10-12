---
status: {{proposed|inferred|approved}}
updated: {{date}}
---

# SEO técnico de {{project_name}}

Fuente de verdad de lo que un buscador puede rastrear, indexar e interpretar del sitio público y de
cómo se ve al compartirlo (`shared/contract.md` → "SEO técnico"). Los temas que se comprueban están
en `shared/seo-checklist.md`; aquí van las reglas del sitio, el estado de cada ruta y las brechas.
No incluye palabras clave, estrategia de contenido ni enlaces externos.

## Reglas del sitio
- URL canónica: {{https://…}} · variante única: {{con o sin `www`}}, {{con o sin barra final}}
  (las demás redirigen con `301`/`308`).
- Idiomas: {{es}}{{; si hay varios: estructura de URLs y `hreflang` con `x-default`}}.
- Renderizado: {{static · ssr · spa · hybrid}} — {{cómo llega el HTML de cada ruta indexable}}.
- No se indexa: {{404, resultados de búsqueda interna, rutas tras inicio de sesión, staging y
  vistas previas}} — mecanismo: {{`noindex` en meta · `X-Robots-Tag` · contraseña}}.
- Páginas de error: 404 propia {{ruta del archivo o componente · genérica del hosting}};
  rutas privadas sin sesión → {{redirección a /login · 401/403 con página propia · no hay rutas
  privadas}}; ambas con `noindex` y fuera del sitemap.
- Archivos generados: `robots.txt` y `sitemap.xml` {{en la build · por el servidor · por el
  hosting}}, construidos desde la URL canónica.
- Compartir: Open Graph {{sí}}{{; tarjetas `twitter:*` sí/no}}; imagen general {{ruta, 1200×630}};
  {{solo la general · generada por página desde la tarjeta del sistema de diseño (qué tipos de
  página) · propia por ruta}}.
- Íconos: {{favicon.svg, favicon-32.png, apple-touch-icon.png · los de la plantilla del framework
  (brecha)}}; `theme-color` {{#…}}.
- Datos estructurados: {{tipos de schema.org por tipo de página, p. ej. `Organization` en la
  home, `Product` en fichas, `Article` en el blog · ninguno}}.
- Presupuesto: {{JS por ruta y peso de imágenes según la constitución}} · Lighthouse SEO ≥ {{90}}.

## Inventario de rutas
<!-- Una fila por ruta o plantilla de ruta (`/blog/[slug]/`). Estados: ✅ cumple · ❌ falla ·
     ➖ no aplica · `no determinado` (sin build, servidor ni URL que consultar). Evidencia: archivo
     generado, URL o comando. En brownfield, solo lo verificado sobre el resultado. -->
| Ruta | Indexable | Título | Descripción | Canónica | `h1` | Open Graph | Datos estructurados | Evidencia |
|---|---|---|---|---|---|---|---|---|
| {{/}} | {{sí · no (motivo)}} | {{✅ · ❌ · ➖}} | | | | | | {{dist/index.html}} |

## Brechas
<!-- Solo hechos verificados sobre el HTML generado, el servidor o producción, o confirmados por el
     usuario. Cada brecha con ID `SE<n>` (no se reutiliza), severidad de `shared/seo-checklist.md`,
     evidencia, correcciones `SE<n>.<letra>` con estado y enlace al roadmap cuando exista. -->
### SE1 · {{alta · media · baja}} — {{brecha}}
Evidencia: {{ruta del archivo generado, URL o comando y salida}}.
Correcciones:
- SE1.a {{corrección}} — estado: pendiente

## Brechas por confirmar
<!-- Dependen de algo que no se pudo verificar (sin build, sin staging, configuración del hosting no
     versionada). Sin severidad ni entrada en el roadmap hasta confirmarlas. -->
- {{brecha}} — depende de: {{dato}} — cómo confirmarla: {{…}}

## Verificación en producción
<!-- La llena /release después de cada despliegue que toque rutas públicas. Lo que comprueba una
     herramienta externa lo confirma el usuario: (confirmado por el usuario, AAAA-MM-DD). -->
| Fecha | Comprobación | Resultado | Evidencia |
|---|---|---|---|
| {{date}} | {{robots.txt y sitemap.xml responden 200 · producción sin noindex · staging con noindex · datos estructurados válidos · vista previa al compartir}} | {{✅ · ❌}} | {{URL, herramienta}} |

## Pendientes operativos
<!-- Fuera del código: alta del sitio y envío del sitemap en las consolas de los buscadores,
     dominio propio, analítica. No son brechas `SE`. -->
- {{…}}

## Historial
| Fecha | Cambio | Origen |
|---|---|---|
| {{date}} | {{Documento creado}} | {{/init · /init --upgrade · /release NNN}} |
