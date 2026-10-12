# Checklist de SEO técnico

Referencia común para `/init` (subagente H de `skills/init/references/explore-agents.md`), `/plan`
(sección "Descubribilidad"), `/review` (revisor de SEO) y `/release` (verificación en producción).
Aplica si `.ai/project.yaml → seo.indexable` es `true`, salvo el tema 12 (íconos), que aplica a
toda interfaz web aunque el sitio no sea indexable. Las reglas del sitio (URL canónica, idiomas, qué
no se indexa, renderizado) están en `docs/seo.md`.

Cubre lo técnico y comprobable: que un buscador pueda rastrear, indexar e interpretar cada ruta
indexable y que el enlace se vea bien al compartirlo. **No** cubre palabras clave, estrategia de
contenido, enlaces externos, analítica ni posiciones en buscadores: ninguna skill promete ni mide
posicionamiento.

## Cómo usarla

- **Sobre el resultado, no sobre el código fuente.** Cada tema indica dónde se comprueba:
  - `generado`: el HTML que produce la build de producción (`dist/`, `build/`, `out/`,
    `.output/public/`…) o, si el sitio se renderiza en el servidor, la respuesta de la vista previa
    local (`curl -s <url>`). Nunca el servidor de desarrollo.
  - `servidor`: códigos HTTP y cabeceras, en local o en staging.
  - `producción`: solo en `/release`, contra la URL pública.
- **Lo que ve un rastreador sin JavaScript.** Evalúa el HTML tal como llega, no el DOM después de
  hidratar. Algunos buscadores ejecutan JavaScript con retraso; las vistas previas de redes y
  mensajería no lo ejecutan nunca.
- **Evidencia.** Cada hallazgo cita la ruta, el archivo generado o la URL y el fragmento (o el
  comando y su salida). Un ✅ también lleva evidencia.
- **Declarado ≠ real.** La configuración del hosting (`vercel.json`, `netlify.toml`, `_redirects`,
  `nginx.conf`) es declarada; lo que responde el servidor es lo real. Si no hay build, vista previa
  ni URL que consultar, el tema queda `no determinado` y va a "Brechas por confirmar": nunca se
  reporta como brecha con severidad.
- **Ruta indexable o no.** Lo decide `docs/seo.md` (inventario de rutas y reglas del sitio). Las
  rutas tras inicio de sesión, la 404, los resultados de búsqueda interna y los entornos que no son
  producción no se indexan salvo decisión explícita.
- Reporta cada tema como ✅ cumple / ➖ no aplica (con motivo) / ❌ falla.

## 1. Rastreo
Dónde: `generado`, `servidor`.
- `robots.txt` en la raíz del sitio: no bloquea rutas indexables y declara
  `Sitemap: <URL absoluta>`. Un `Disallow: /` que llega a producción es severidad alta.
- `sitemap.xml` válido, con el espacio de nombres de sitemaps, que lista **todas** las rutas
  indexables del inventario (también las generadas a partir de datos: artículos, productos) con su
  URL canónica absoluta construida desde `seo.site_url`, y **ninguna** 404, redirección ni ruta con
  `noindex`.
- La navegación interna usa enlaces `<a href>` rastreables; una ruta indexable a la que solo se
  llega por un manejador de clic no existe para el rastreador.

## 2. Códigos HTTP, redirecciones y páginas de error
Dónde: `servidor`, `producción`; la existencia y el contenido de las páginas de error, también en
`generado`.
- Cada ruta indexable responde `200`.
- Una URL inexistente responde `404` real; una página de error con `200` ("404 blando") se indexa
  como contenido.
- **Página 404 propia** (no la genérica del hosting o del framework): dice que la página no existe,
  ofrece enlaces a la portada o a las secciones principales, mantiene la navegación del sitio y no
  está en el sitemap.
- **Rutas que exigen inicio de sesión o permisos:** sin sesión, redirigen al inicio de sesión
  (`302`/`303`) o responden `401`/`403` con una **página propia** que lo explica y ofrece cómo
  entrar o volver. Nunca `200` con la página de error ni con un aviso dentro de la plantilla normal.
  El inicio de sesión, la página de no autorizado y las rutas privadas llevan `noindex` y no están
  en el sitemap. Si una ruta privada devuelve su contenido sin sesión, no es un tema de SEO: es un
  fallo de control de acceso y se reporta también como hallazgo de seguridad
  (`security-checklist.md` §1).
- Redirecciones permanentes (`301`/`308`) en un solo salto, sin cadenas ni bucles.
- Una sola variante de cada URL: `https`, con o sin `www` y con o sin barra final según
  `docs/seo.md`; las demás redirigen a ella.

## 3. Indexación y canónica
Dónde: `generado`, `servidor`.
- `noindex` (`<meta name="robots">` o cabecera `X-Robots-Tag`) solo en rutas no indexables, la
  404, staging y vistas previas. En producción, sobre una ruta indexable, es severidad alta.
- Una sola `<link rel="canonical">` por página, absoluta, construida desde `seo.site_url`, que
  apunta a la propia página o a su versión preferida y coincide con la URL del sitemap.

## 4. Metadatos por ruta
Dónde: `generado`.
- `<html lang>` con el idioma del contenido.
- `<title>` presente, único entre rutas y descriptivo de esa página (orientativo: 30–60
  caracteres).
- `<meta name="description">` presente y única entre rutas (orientativo: 70–160 caracteres).
- Un solo `h1` por página y encabezados sin saltos de nivel.
- `<meta name="viewport">` presente.
- Títulos o descripciones idénticos en varias rutas son un hallazgo aunque cada página los tenga.

## 5. Contenido disponible sin JavaScript
Dónde: `generado`. Según `seo.rendering`:
- `static`, `ssr`, `hybrid`: el HTML de cada ruta indexable ya contiene su título, sus metadatos y
  su contenido principal.
- `spa`: si todas las rutas comparten el mismo HTML con título y metadatos genéricos, es severidad
  alta para metadatos y para compartir. La corrección (prerenderizar o renderizar en el servidor
  las rutas indexables) es una decisión de `/plan` con ADR, no de esta lista.

## 6. Imágenes y medios
Dónde: `generado`.
- Imágenes de contenido con `alt` descriptivo; decorativas con `alt=""`.
- `width` y `height` (o relación de aspecto) declarados, para que la página no salte al cargar.
- Carga diferida solo por debajo del primer pantallazo; nunca en la imagen principal.
- Formatos y tamaños acordes al presupuesto del tema 10.

## 7. Compartir (Open Graph y tarjetas)
Dónde: `generado`; la vista previa real, en `producción` (la confirma el usuario con la
herramienta de inspección de la red correspondiente).
- `og:title`, `og:description`, `og:type`, `og:url` (igual a la canónica) y `og:locale`.
- `og:image` absoluta, pública (sin autenticación), con `og:image:width`, `og:image:height` y
  `og:image:alt`; 1200×630 y ≤ 300 kB.
- Cada ruta usa la imagen que dice su fila de "Descubribilidad" del plan o `docs/seo.md`: la
  general del sitio, una **generada** a partir de su contenido o una propia. Si hay sistema de
  diseño, la imagen sigue su "Tarjeta para compartir" (`docs/design/system.md`): el texto sale de
  los metadatos de la página (título, sección, descripción), nunca se inventa, y lo importante
  queda dentro de la zona segura central (algunas apps recortan la imagen en cuadrado).
- `og:image:alt` describe lo que muestra la imagen (por defecto, el título de la página).
- Etiquetas `twitter:*` solo si `docs/seo.md` las incluye.

## 8. Datos estructurados
Dónde: `generado`; validación con una herramienta de schema.org o de resultados enriquecidos en
`producción` (la confirma el usuario).
- JSON-LD que se parsea, con un tipo de schema.org que describe el contenido real de la página
  (`Organization`, `Person`, `Product`, `Article`, `BreadcrumbList`, `LocalBusiness`…).
- Los datos coinciden con lo visible en la página: sin valoraciones, reseñas, precios ni
  disponibilidad inventados.
- Una sola declaración por entidad, sin duplicados contradictorios entre componentes.

## 9. Varios idiomas o regiones (solo si existen)
Dónde: `generado`.
- `hreflang` recíproco entre todas las versiones, con `x-default`.
- Cada versión con su propia canónica y su `lang`.

## 10. Rendimiento
Dónde: `generado`, medido sobre la build de producción servida en local, no sobre el servidor de
desarrollo.
- Peso de JavaScript por ruta y de imágenes dentro del presupuesto de la constitución.
- Lighthouse SEO ≥ 90 y Performance dentro del objetivo de la constitución, si lo fija.
- Sin presupuesto en la constitución, informa la medida sin severidad y propón el principio.

## 11. Entornos
Dónde: `servidor` (staging), `producción`.
- Staging y vistas previas con `noindex` o protegidos con contraseña.
- Producción sin `noindex`: comprueba que la variable o la configuración que lo activa en staging
  no viaja a producción.

## 12. Íconos del sitio
Dónde: `generado` (y `servidor` para el código de estado). Aplica a toda interfaz web, también
privada: el ícono es la pestaña del navegador.
- `favicon.svg` (o `favicon.ico`), PNG de 32×32 y `apple-touch-icon` de 180×180, enlazados en el
  `<head>` de **todas** las rutas y respondiendo `200`.
- `<meta name="theme-color">` con el color de fondo del sistema de diseño (`--color-bg`) si existe.
- Salen del logo o de la marca del proyecto (`docs/design/system.md` → "Marca en el navegador y al
  compartir"); nunca el ícono por defecto de la plantilla del framework (logos de Vite, Astro,
  Next, Angular, React, Svelte…). Si el proyecto no tiene logo, un monograma provisional marcado
  como tal hasta que el usuario decida.
- Solo si el sitio es una PWA: `manifest` con íconos de 192×192 y 512×512 (y versión `maskable`).
- Fuera de alcance: íconos de tienda y pantallas de arranque de apps móviles.

## Severidad
| Severidad | Criterio |
|---|---|
| alta | Una ruta indexable no se puede rastrear, indexar o atribuir a su URL: `noindex` o `Disallow: /` en producción, canónica hacia otra URL o dominio, metadatos solo después de JavaScript, sitemap con un dominio que no es `seo.site_url`. |
| media | Se indexa, pero mal: título o descripción ausentes o repetidos, sin sitemap o incompleto, 404 blando, una ruta privada o la página de no autorizado que responde `200` o es indexable, varios `h1`, JSON-LD que no se parsea, sin `lang`, Lighthouse SEO < 90, imagen para compartir con texto que no corresponde a la página o inventado. |
| baja | Mejora: sin página 404 o de no autorizado propias (se usa la genérica, con el código correcto), sin Open Graph o sin datos estructurados, imagen para compartir fuera de tamaño o de peso, títulos fuera del rango orientativo, `alt` ausente en imágenes que no son de contenido, favicon ausente o el de la plantilla del framework. |

En `/review`, **alta es bloqueante**; media es importante; baja es menor. Las brechas `SE` de
`docs/seo.md` usan la misma escala.
