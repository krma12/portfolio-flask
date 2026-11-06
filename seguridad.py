"""
Seguridad del portfolio, todo en un solo lugar:

1. Encabezados de seguridad en cada respuesta (CSP, HSTS, etc.)
2. Límite de intentos: bloquea por un rato a quien falla la clave muchas veces
3. Validadores para los datos que llegan a la API (links https y largos máximos)

Se conecta a la app con  instalar_seguridad(app)  desde app.py.
"""
import time
from collections import defaultdict, deque
from urllib.parse import urlparse

from flask import request

# ---------------------------------------------------------------------------
# 1. Encabezados de seguridad
# ---------------------------------------------------------------------------
# Content-Security-Policy: la lista de lugares de donde la página puede cargar cosas.
# Si alguien lograra meter un <script> en la página, el navegador no lo ejecutaría,
# porque solo se permiten scripts de este mismo sitio ('self').
CSP = "; ".join([
    "default-src 'self'",
    "script-src 'self'",                                            # sin scripts en línea
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",  # estilos de la página + Google Fonts
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data:",
    "connect-src 'self'",                                           # la vista JSON pide /proyectos
    "form-action 'self' https://formspree.io",                      # el formulario solo envía a Formspree
    "frame-ancestors 'none'",                                       # nadie puede meter el sitio en un iframe
    "base-uri 'self'",
    "object-src 'none'",
    "upgrade-insecure-requests",
])

ENCABEZADOS = {
    "Content-Security-Policy": CSP,
    # HSTS: el navegador recordará por un año que este sitio solo se abre con HTTPS
    "Strict-Transport-Security": "max-age=31536000",
    # No adivinar el tipo de archivo (evita que un .txt se ejecute como script)
    "X-Content-Type-Options": "nosniff",
    # Versión antigua de frame-ancestors, para navegadores viejos
    "X-Frame-Options": "DENY",
    # Al salir a otro sitio, solo se comparte el dominio, no la ruta completa
    "Referrer-Policy": "strict-origin-when-cross-origin",
    # La página no usa cámara, micrófono ni ubicación: se los negamos a todo
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
}


def agregar_encabezados(respuesta):
    for nombre, valor in ENCABEZADOS.items():
        respuesta.headers.setdefault(nombre, valor)
    return respuesta


# ---------------------------------------------------------------------------
# 2. Límite de intentos con clave incorrecta
# ---------------------------------------------------------------------------
MAX_FALLOS = 5            # intentos fallidos permitidos...
VENTANA = 10 * 60         # ...dentro de 10 minutos
BLOQUEO = 15 * 60         # después, 15 minutos bloqueado

_fallos = defaultdict(deque)   # ip -> momentos de los últimos fallos
_bloqueados = {}               # ip -> momento en que termina el bloqueo


def ip_cliente():
    # En PythonAnywhere la petición pasa por su proxy, que pone la IP real en X-Real-IP
    return request.headers.get("X-Real-IP") or request.remote_addr or "desconocida"


def esta_bloqueado(ip, ahora=None):
    ahora = ahora or time.time()
    fin = _bloqueados.get(ip)
    if fin and ahora < fin:
        return int(fin - ahora)          # segundos que faltan
    _bloqueados.pop(ip, None)
    return 0


def registrar_fallo(ip, ahora=None):
    ahora = ahora or time.time()
    fallos = _fallos[ip]
    fallos.append(ahora)
    while fallos and ahora - fallos[0] > VENTANA:
        fallos.popleft()
    if len(fallos) >= MAX_FALLOS:
        _bloqueados[ip] = ahora + BLOQUEO
        fallos.clear()


def limpiar_intentos():
    """Borra el historial (lo usan las pruebas)."""
    _fallos.clear()
    _bloqueados.clear()


# ---------------------------------------------------------------------------
# 3. Validadores para reqparse
# ---------------------------------------------------------------------------
def link_https(valor):
    """Acepta vacío o un link https:// de verdad. Rechaza javascript:, data:, http:, etc."""
    if valor is None or str(valor).strip() == "":
        return None
    valor = str(valor).strip()
    partes = urlparse(valor)
    if partes.scheme != "https" or not partes.netloc or len(valor) > 300:
        raise ValueError("Debe ser un link https:// válido (máx. 300 caracteres)")
    return valor


def texto(maximo):
    """Crea un validador de texto con largo máximo."""
    def validar(valor):
        if valor is None:
            return None
        valor = str(valor).strip()
        if len(valor) > maximo:
            raise ValueError(f"Máximo {maximo} caracteres")
        return valor
    validar.__name__ = f"texto_max_{maximo}"
    return validar


def instalar_seguridad(app):
    app.after_request(agregar_encabezados)
