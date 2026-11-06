"""
Pruebas de seguridad: que los encabezados estén, que la API rechace links
peligrosos y textos enormes, y que frene a quien adivina la clave.
"""

import os

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['PORTFOLIO_API_KEY'] = 'clave-de-prueba'

import pytest  # noqa: E402

from app import app  # noqa: E402
from models import Proyecto, db  # noqa: E402
from seguridad import MAX_FALLOS, limpiar_intentos  # noqa: E402

CLAVE = {'X-API-Key': 'clave-de-prueba'}


@pytest.fixture
def cliente():
    app.config['TESTING'] = True
    app.config['API_KEY'] = 'clave-de-prueba'
    limpiar_intentos()
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Proyecto(titulo='Existente', tecnologias='Python'))
        db.session.commit()
    yield app.test_client()
    limpiar_intentos()


# ---------- Encabezados ----------

@pytest.mark.parametrize('ruta', ['/', '/proyectos'])
def test_encabezados_de_seguridad(cliente, ruta):
    h = cliente.get(ruta).headers
    assert "script-src 'self'" in h['Content-Security-Policy']
    assert "frame-ancestors 'none'" in h['Content-Security-Policy']
    assert h['Strict-Transport-Security'].startswith('max-age=')
    assert h['X-Content-Type-Options'] == 'nosniff'
    assert h['X-Frame-Options'] == 'DENY'
    assert 'Referrer-Policy' in h and 'Permissions-Policy' in h


def test_csp_no_permite_scripts_en_linea(cliente):
    csp = cliente.get('/').headers['Content-Security-Policy']
    script_src = [p for p in csp.split(';') if p.strip().startswith('script-src')][0]
    assert "'unsafe-inline'" not in script_src


def test_la_pagina_no_tiene_scripts_en_linea(cliente):
    """Si alguien vuelve a poner un <script> o un onclick= en el HTML, la CSP lo bloquearía."""
    html = cliente.get('/').get_data(as_text=True)
    assert '<script>' not in html
    for evento in ('onclick=', 'onerror=', 'onload='):
        assert evento not in html


# ---------- Validación de datos ----------

@pytest.mark.parametrize('link', [
    'javascript:alert(1)',
    'JaVaScRiPt:alert(1)',
    'data:text/html,<script>alert(1)</script>',
    'http://inseguro.com',
    'https://',
    'no-es-un-link',
])
def test_rechaza_links_peligrosos(cliente, link):
    r = cliente.post('/proyectos', json={'titulo': 'X', 'repo_url': link}, headers=CLAVE)
    assert r.status_code == 400
    r = cliente.post('/proyectos', json={'titulo': 'X', 'demo_url': link}, headers=CLAVE)
    assert r.status_code == 400


def test_acepta_links_https(cliente):
    r = cliente.post('/proyectos', json={'titulo': 'X', 'repo_url': 'https://github.com/krma12/x'}, headers=CLAVE)
    assert r.status_code == 201


def test_rechaza_textos_demasiado_largos(cliente):
    r = cliente.post('/proyectos', json={'titulo': 'a' * 121}, headers=CLAVE)
    assert r.status_code == 400
    r = cliente.post('/proyectos', json={'titulo': 'ok', 'descripcion': 'a' * 501}, headers=CLAVE)
    assert r.status_code == 400


def test_el_html_escapa_lo_que_viene_de_la_base(cliente):
    """Un título con HTML se muestra como texto, no se ejecuta."""
    cliente.post('/proyectos', json={'titulo': '<img src=x onerror=alert(1)>'}, headers=CLAVE)
    html = cliente.get('/').get_data(as_text=True)
    assert '<img src=x onerror=alert(1)>' not in html
    assert '&lt;img src=x onerror=alert(1)&gt;' in html


# ---------- Límite de intentos ----------

def test_bloquea_despues_de_varios_fallos(cliente):
    for _ in range(MAX_FALLOS):
        assert cliente.delete('/proyectos/1', headers={'X-API-Key': 'adivinando'}).status_code == 401
    bloqueado = cliente.delete('/proyectos/1', headers={'X-API-Key': 'adivinando'})
    assert bloqueado.status_code == 429
    assert 'Retry-After' in bloqueado.headers
    # durante el bloqueo, ni con la clave correcta (no se puede seguir probando claves)
    assert cliente.delete('/proyectos/1', headers=CLAVE).status_code == 429
    # y el proyecto sigue ahí
    assert cliente.get('/proyectos/1').status_code == 200


def test_leer_nunca_se_bloquea(cliente):
    for _ in range(MAX_FALLOS + 2):
        cliente.delete('/proyectos/1', headers={'X-API-Key': 'mal'})
    assert cliente.get('/proyectos').status_code == 200
    assert cliente.get('/').status_code == 200


def test_el_bloqueo_expira():
    from seguridad import BLOQUEO, esta_bloqueado, registrar_fallo
    limpiar_intentos()
    for _ in range(MAX_FALLOS):
        registrar_fallo('1.2.3.4', ahora=1000)
    assert esta_bloqueado('1.2.3.4', ahora=1001)
    assert not esta_bloqueado('1.2.3.4', ahora=1000 + BLOQUEO + 1)
    limpiar_intentos()


# ---------- Registro de eventos ----------

def test_registra_clave_invalida_sin_guardar_la_clave(cliente, caplog):
    with caplog.at_level('INFO', logger='portfolio.seguridad'):
        cliente.post('/proyectos', json={'titulo': 'X'}, headers={'X-API-Key': 'clave-secreta-adivinada'})
    texto = caplog.text
    assert 'evento=clave_invalida' in texto
    assert 'clave-secreta-adivinada' not in texto      # nunca se escribe la clave en el log


def test_registra_bloqueo_y_cambios(cliente, caplog):
    with caplog.at_level('INFO', logger='portfolio.seguridad'):
        cliente.post('/proyectos', json={'titulo': 'Nuevo'}, headers=CLAVE)
        for _ in range(MAX_FALLOS):
            cliente.delete('/proyectos/1', headers={'X-API-Key': 'mal'})
    assert 'evento=proyecto_creado' in caplog.text
    assert 'evento=ip_bloqueada' in caplog.text


# ---------- CORS: la bitácora puede leer la lista de proyectos ----------
def test_cors_permite_leer_proyectos_a_la_bitacora(cliente):
    r = cliente.get('/proyectos', headers={'Origin': 'https://krma12.github.io'})
    assert r.headers.get('Access-Control-Allow-Origin') == 'https://krma12.github.io'


def test_cors_no_permite_otros_sitios(cliente):
    r = cliente.get('/proyectos', headers={'Origin': 'https://sitio-malo.example'})
    assert 'Access-Control-Allow-Origin' not in r.headers


def test_cors_solo_para_leer(cliente):
    r = cliente.post('/proyectos', json={'titulo': 'x'}, headers={'Origin': 'https://krma12.github.io'})
    assert 'Access-Control-Allow-Origin' not in r.headers
