# Checklist de seguridad (OWASP)

Referencia común para `/plan` (modelo de amenazas), `/review` (auditoría) y `/security-audit`.
Está organizada por **temas** para no depender de una edición concreta del OWASP Top 10: al usarla,
mapea cada hallazgo al ID de la edición vigente registrada en `docs/security.md → Referencias`
(p. ej. `A01:<año>`). Si `docs/security.md` no indica edición, usa la más reciente que conozcas y
anótalo en el informe.

Para cada tema: revisa solo lo que aplique al tipo de proyecto y al alcance del cambio. Todo
hallazgo necesita evidencia (`archivo:línea` o salida de una herramienta).

## 1. Control de acceso
- Toda operación sensible verifica autorización **en el servidor**, no solo en la UI.
- Acceso a objetos por ID comprueba que el recurso pertenece al usuario (IDOR / BOLA).
- Denegar por defecto; roles y permisos centralizados, no repartidos en condicionales sueltos.
- CORS restrictivo; sin métodos o rutas administrativas expuestas sin protección.
- Limitación de tasa en endpoints costosos o de autenticación.

## 2. Criptografía y datos sensibles
- Datos sensibles (según `docs/security.md → Clasificación de datos`) cifrados en tránsito (TLS) y
  en reposo cuando corresponda.
- Contraseñas con algoritmos de hash lentos y con sal (argon2, bcrypt, scrypt). Nunca cifrado
  reversible ni hash rápido.
- Sin algoritmos obsoletos (MD5, SHA-1 para seguridad, DES, ECB) ni aleatoriedad no criptográfica
  para tokens.
- Sin datos sensibles en URLs, logs, mensajes de error o almacenamiento del navegador.

## 3. Inyección
- Consultas parametrizadas / ORM; nada de concatenar entradas en SQL, NoSQL, LDAP, comandos de
  shell o expresiones.
- Salida codificada según contexto (HTML, atributo, JS, URL) para evitar XSS; sin
  `dangerouslySetInnerHTML`/`v-html`/`innerHTML` con datos del usuario sin sanear.
- Sin `eval`, deserialización insegura ni plantillas construidas con entrada del usuario.
- Validación de entrada en el servidor con listas de permitidos (tipo, longitud, formato).

## 4. Diseño inseguro
- Existe modelo de amenazas para la feature (sección del plan) y cada amenaza tiene control y test.
- Casos de abuso de la spec cubiertos (límites de negocio, enumeración, automatización abusiva).
- Flujos críticos (pagos, cambio de correo/contraseña, borrado) con re-autenticación o
  confirmación cuando aplique.

## 5. Configuración
- Sin credenciales por defecto, modos debug o trazas de error expuestas en producción.
- Cabeceras de seguridad (CSP, HSTS, X-Content-Type-Options, frame-ancestors) en apps web.
- Principio de mínimo privilegio en cuentas de servicio, IAM, contenedores (no root) y tokens.
- Configuración distinta por entorno; secretos en gestor de secretos, nunca en el repo.

## 6. Componentes y cadena de suministro
- Dependencias sin vulnerabilidades conocidas críticas o altas (herramienta SCA).
- Lockfile versionado; dependencias nuevas justificadas en un ADR.
- Imágenes base y acciones de CI fijadas a versión o digest; sin scripts remotos ejecutados sin
  verificar (`curl | sh`).

## 7. Autenticación y sesiones
- Protección contra fuerza bruta y relleno de credenciales (rate limit, bloqueo progresivo, MFA
  donde aplique).
- Tokens y cookies de sesión: `HttpOnly`, `Secure`, `SameSite`, expiración y rotación; invalidación
  al cerrar sesión o cambiar contraseña.
- JWT: algoritmo fijado, firma verificada, expiración corta, sin datos sensibles en el payload.
- Recuperación de cuenta sin enumeración de usuarios.

## 8. Integridad de software y datos
- Protección CSRF en operaciones con estado basadas en cookies.
- Webhooks y mensajes entrantes con firma verificada.
- Artefactos de build y despliegue reproducibles y firmados cuando la plataforma lo permita.

## 9. Registro y monitoreo
- Se registran eventos de seguridad (login fallido, cambios de permisos, accesos denegados) sin
  datos sensibles.
- Logs estructurados con correlación; alertas definidas en `docs/deployment.md`.

## 10. Peticiones del lado del servidor (SSRF)
- URLs proporcionadas por el usuario validadas contra lista de permitidos; bloqueo de direcciones
  internas y metadatos cloud.

## 11. Manejo de errores y condiciones excepcionales
- Los errores no filtran detalles internos (stack traces, consultas, rutas).
- Fallos cerrados: ante error en autorización o validación, se deniega.
- Límites de tamaño, tiempo y recursos para evitar agotamiento (DoS).

## Adicionales según tipo de proyecto
- **backend / fullstack con API:** revisa también el OWASP API Security Top 10 (autorización a
  nivel de objeto y de propiedad, consumo de recursos sin límite, exposición excesiva de datos).
- **Apps que usan LLMs:** revisa el OWASP Top 10 para aplicaciones LLM (inyección de prompt,
  salida no validada usada como código o consulta, filtración de datos en el contexto, agencia
  excesiva de herramientas).
- **Mobile:** OWASP MASVS.

## Severidad
| Severidad | Criterio |
|---|---|
| crítica | Explotable sin autenticación o con impacto sobre todos los usuarios o datos sensibles. |
| alta | Explotable con condiciones razonables; compromete cuentas, datos o integridad. |
| media | Requiere condiciones poco comunes o tiene impacto limitado. |
| baja | Endurecimiento o buena práctica sin vector claro. |

En `/review`, **crítica y alta son bloqueantes**; media es importante; baja es menor.
