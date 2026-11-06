# Portfolio Flask — Reporte del proyecto

**Autor:** Hugo Maldonado ([@krma12](https://github.com/krma12)) · **Sitio en vivo:** [hugoportfolio.pythonanywhere.com](https://hugoportfolio.pythonanywhere.com) · **Fecha:** noviembre 2026

> Este reporte omite a propósito datos sensibles: claves, identificadores de servicios, rutas del servidor y datos personales de contacto. Donde hacen falta para explicar algo, aparecen como `[REDACTADO]`.

## 1. Propósito

Este proyecto es mi portfolio profesional: una página web que presenta quién soy, qué sé hacer y los proyectos que he construido, con un link al código de cada uno.

No es una página estática. Los proyectos viven en una **base de datos** y se administran a través de una **API REST** propia. La página se arma sola con esa información, y una automatización diaria mantiene el portfolio al día con mis repositorios de GitHub.

En otras palabras, el portfolio también es un proyecto técnico en sí mismo: muestra mis proyectos y a la vez demuestra cómo construyo, pruebo, publico y protejo una aplicación web completa.

## 2. Cómo empezó y por qué

El proyecto nació como una práctica de la materia de **Servicios Web** en mi carrera de Ingeniería en Inteligencia Artificial: construir una API REST con Flask que hiciera las operaciones básicas (crear, leer, actualizar y borrar) sobre una base de datos.

En lugar de dejarlo como un ejercicio, decidí convertirlo en algo que de verdad usara. Las razones fueron tres:

- **Necesitaba un portfolio.** Para buscar oportunidades en tecnología, sobre todo en ciberseguridad, necesitaba un lugar donde mostrar mis proyectos de forma profesional.
- **Quería aprender haciendo algo real.** Publicar en internet, automatizar y proteger una aplicación enseña cosas que un ejercicio de clase no cubre.
- **Quería que se mantuviera solo.** Cada vez que creo un proyecto nuevo en GitHub, el portfolio debería enterarse sin que yo tenga que editar nada a mano.

## 3. Objetivo

Tener un portfolio **publicado, bilingüe, automatizado y seguro**, que cumpla con estos puntos:

1. Mostrar mis proyectos desde una base de datos, sin HTML escrito a mano para cada uno.
2. Verse bien en computadora y celular, en inglés y español, y en modo claro y oscuro.
3. Actualizarse solo con mis repositorios de GitHub.
4. Estar protegido: que solo yo pueda modificar los datos y que la página resista ataques comunes de aplicaciones web.
5. Tener pruebas automáticas que avisen si algo se rompe.

## 4. Acciones tomadas

| Etapa | Qué se hizo |
|---|---|
| **Base** | API REST con Flask-RESTful y SQLAlchemy sobre SQLite: listar, crear, editar y borrar proyectos. La página se genera con plantillas Jinja2 a partir de la base de datos. |
| **Proteger la escritura** | Cualquier cambio en la API ahora pide una clave en el encabezado `X-API-Key`. La clave vive en una variable de entorno y nunca en el código. Si no hay clave configurada, la API queda de solo lectura. |
| **Pruebas** | Pruebas automáticas con pytest para la API, la página, la sincronización y la seguridad. Hoy son 45 pruebas. |
| **Interfaz** | Diseño responsive con modo claro/oscuro, cambio de idioma inglés/español, filtros por tecnología, una vista JSON que muestra la API en vivo y una terminal interactiva con comandos como `projects --tag security`. Formulario de contacto conectado a Formspree. |
| **Publicación** | El sitio se publicó en PythonAnywhere con HTTPS forzado y el modo debug apagado en producción. |
| **Automatización** | GitHub Actions corre las pruebas en cada cambio y, cada mañana, sincroniza el portfolio con mis repositorios: agrega los nuevos y completa la descripción y los topics de los que ya existen, sin pisar lo que escribí a mano. |
| **Pulido** | Las etiquetas de tecnologías se muestran limpias (siglas correctas, máximo 6 por tarjeta con un botón para ver el resto). Los títulos recuperan los acentos que GitHub quita. La página ya no se oscurece a la fuerza por extensiones del navegador. |
| **Seguridad** | Validación de datos, encabezados de seguridad, límite de intentos, auditoría de dependencias y pruebas de seguridad. Los detalles están en la sección 6. |

## 5. Arquitectura y conceptos aplicados

```
GitHub (repos) ──► GitHub Actions ──► API REST del portfolio ──► SQLite
                     (cada día)          (con clave)                 │
                                                                     ▼
Visitante ◄── HTTPS ◄── Flask + Jinja2 (página) ◄────────────────────┘
```

**Conceptos de desarrollo web**
- **REST:** cada proyecto es un recurso con su URL (`/proyectos/<id>`), y los métodos HTTP indican la acción (GET, POST, PUT, DELETE).
- **ORM (SQLAlchemy):** las tablas se manejan como clases de Python en lugar de escribir SQL a mano.
- **Separación de responsabilidades:** `app.py` arranca la app, `routes.py` define las rutas, `resources.py` tiene la lógica, `models.py` los datos y `seguridad.py` la protección.
- **Plantillas (Jinja2):** el HTML se genera con los datos de la base, y Jinja2 escapa automáticamente el texto para evitar inyecciones.
- **Diseño responsive, accesibilidad e internacionalización (inglés/español).**

**Conceptos de DevOps**
- **Variables de entorno** para los secretos, así ninguna clave queda en el código ni en GitHub.
- **Integración continua (CI):** cada cambio corre las pruebas y la auditoría antes de llegar a producción.
- **Automatización programada:** un trabajo diario de GitHub Actions usa la propia API del portfolio para sincronizarlo.
- **Idempotencia:** correr la sincronización muchas veces da el mismo resultado; no duplica proyectos ni pisa datos.

**Conceptos de seguridad**
- Autenticación con clave, comparación en tiempo constante, *fail closed*, validación de entradas, XSS, CSP, HSTS, *clickjacking*, *rate limiting*, mínimo privilegio y gestión de dependencias. Se explican en la siguiente sección.

## 6. Seguridad: qué se protegió y por qué

**Resultado:** calificación **A+ (110/100, 12 de 12 pruebas)** en [Mozilla HTTP Observatory](https://developer.mozilla.org/en-US/observatory/analyze?host=hugoportfolio.pythonanywhere.com), la herramienta pública de Mozilla que evalúa la seguridad de un sitio web (noviembre 2026).

| Amenaza | Protección | Por qué importa |
|---|---|---|
| Alguien edita o borra mis proyectos | La API pide una clave (`X-API-Key`), que se compara con `hmac.compare_digest` | Solo yo puedo escribir. La comparación en tiempo constante evita adivinar la clave midiendo cuánto tarda la respuesta. |
| Me olvido de configurar la clave | *Fail closed*: sin clave configurada, la API queda de solo lectura | Un error de configuración deja la API cerrada en vez de abierta. |
| Adivinar la clave a fuerza bruta | **Límite de intentos:** 5 fallos en 10 minutos bloquean esa IP 15 minutos (respuesta `429`) | Hace impráctico probar miles de claves. Leer la página nunca se bloquea. |
| Guardar un link malicioso (`javascript:...`) | La API solo acepta links `https://` y rechaza `javascript:`, `data:` y `http:` | Evita XSS: que un link ejecute código cuando alguien le da clic. |
| Guardar textos gigantes | Largo máximo por campo, por ejemplo 120 caracteres en el título | Evita abusos y datos que rompan el diseño. |
| Inyectar HTML o scripts en la página | Jinja2 escapa el texto, y la terminal y la vista JSON también escapan los datos | El texto se muestra como texto, nunca se ejecuta. |
| Que un script ajeno se ejecute | **Content-Security-Policy:** solo se permiten scripts del propio sitio, sin scripts en línea; las fuentes solo vienen de Google Fonts y el formulario solo envía a Formspree | Aunque alguien lograra inyectar código, el navegador se negaría a ejecutarlo. |
| Tráfico sin cifrar | HTTPS forzado + **HSTS** | El navegador recuerda que el sitio solo se abre con HTTPS. |
| *Clickjacking* (meter el sitio en un marco invisible) | `frame-ancestors 'none'` + `X-Frame-Options: DENY` | Nadie puede incrustar el portfolio en otra página para engañar usuarios. |
| Otros abusos del navegador | `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` | Bloquean la adivinación de tipos de archivo, limitan lo que se comparte al salir del sitio y niegan cámara, micrófono y ubicación. |
| Errores que muestran información interna | Modo debug apagado en producción | En internet, el modo debug permitiría ejecutar código en el servidor. |
| Spam en el formulario | Campo trampa (*honeypot*) que solo llenan los bots | Formspree descarta esos mensajes. |
| Librerías con vulnerabilidades | `pip-audit` en cada cambio + **Dependabot** semanal | Me entero si Flask u otra dependencia tiene un fallo conocido y GitHub propone la actualización. |
| Que una protección se pierda sin darme cuenta | 16 pruebas de seguridad automáticas | Si un cambio quita un encabezado o vuelve a aceptar links peligrosos, las pruebas fallan. |
| Claves expuestas | Secretos solo en variables de entorno y GitHub Secrets; **rotación** de la clave cuando quedó visible | Una clave vista por alguien más se cambia de inmediato. |

## 7. Problemas encontrados y cómo se resolvieron

- **Error 500 al publicar.** La carpeta se llamaba `Templates` con mayúscula. Windows no distingue mayúsculas, pero el servidor Linux sí. Se renombró a `templates`.
- **Las tareas programadas de PythonAnywhere son de paga.** La sincronización diaria se movió a GitHub Actions, que es gratis y además corre las pruebas.
- **OneDrive bloqueaba archivos de git.** Se pausó la sincronización de OneDrive mientras se usaba git.
- **La sincronización falló tras renombrar un repositorio.** El portfolio guardaba la dirección vieja y la clave de GitHub ya no coincidía con la del servidor. Se actualizó la dirección y se volvió a sincronizar la clave.
- **`PUT` reemplaza el proyecto completo.** Mandar solo un campo borraba los demás. Ahora los scripts envían el proyecto completo con el cambio.
- **Proyectos nuevos sin descripción.** La sincronización solo agregaba repos y nunca volvía a revisarlos. Ahora también completa la descripción y los topics que falten.
- **Tarjetas saturadas de etiquetas y siglas mal escritas** ("Ai", "Llm"). Ahora hay un máximo de 6 etiquetas visibles por tarjeta y las siglas se corrigen al mostrarlas.
- **El modo claro regresaba a oscuro.** Una herramienta de modo oscuro del navegador sobreescribía el tema. La página ahora declara que tiene su propio modo oscuro.

## 8. Próximos pasos

- Escribir la descripción en español de los proyectos nuevos.
- Agregar una búsqueda por texto en los proyectos.
- Registrar los intentos bloqueados para revisarlos (*logging*).
- Evaluar una base de datos administrada si el sitio crece.
- Seguir sumando proyectos, en especial de ciberseguridad e IA.
