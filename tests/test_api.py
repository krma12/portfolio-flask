"""
Pruebas automáticas de la API.

Se corren desde la carpeta del proyecto, con el entorno virtual activado:

    python -m pytest

Usan una base de datos temporal en memoria, así que NO tocan tu proyectos.db.
"""

import os

# Estas variables se definen ANTES de importar la app, porque app.py las lee al arrancar.
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['PORTFOLIO_API_KEY'] = 'clave-de-prueba'
os.environ.pop('FORMSPREE_ID', None)

import pytest  # noqa: E402

from app import app  # noqa: E402
from models import Proyecto, db  # noqa: E402

CLAVE = {'X-API-Key': 'clave-de-prueba'}
NUEVO = {'titulo': 'Proyecto de prueba', 'tecnologias': 'Python, Flask', 'emoji': '🧪'}


@pytest.fixture
def cliente():
    """Antes de cada prueba: tablas vacías y un cliente que simula al navegador."""
    app.config['TESTING'] = True
    app.config['API_KEY'] = 'clave-de-prueba'
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Proyecto(titulo='Existente', tecnologias='Python'))
        db.session.commit()
    return app.test_client()


# ---------- Lectura pública ----------

def test_pagina_principal_carga(cliente):
    respuesta = cliente.get('/')
    assert respuesta.status_code == 200
    assert b'Existente' in respuesta.data


def test_listar_proyectos(cliente):
    respuesta = cliente.get('/proyectos')
    assert respuesta.status_code == 200
    assert respuesta.get_json()[0]['tecnologias'] == ['Python']


def test_proyecto_inexistente_da_404(cliente):
    assert cliente.get('/proyectos/999').status_code == 404


# ---------- Escritura protegida ----------

def test_crear_sin_clave_da_401(cliente):
    assert cliente.post('/proyectos', json=NUEVO).status_code == 401


def test_crear_con_clave_incorrecta_da_401(cliente):
    respuesta = cliente.post('/proyectos', json=NUEVO, headers={'X-API-Key': 'adivinando'})
    assert respuesta.status_code == 401


def test_crear_con_clave_correcta(cliente):
    respuesta = cliente.post('/proyectos', json=NUEVO, headers=CLAVE)
    assert respuesta.status_code == 201
    assert respuesta.get_json()['tecnologias'] == ['Python', 'Flask']


def test_crear_sin_titulo_da_400(cliente):
    respuesta = cliente.post('/proyectos', json={'descripcion': 'sin título'}, headers=CLAVE)
    assert respuesta.status_code == 400


def test_editar_y_borrar_con_clave(cliente):
    assert cliente.put('/proyectos/1', json={'titulo': 'Editado'}, headers=CLAVE).get_json()['titulo'] == 'Editado'
    assert cliente.delete('/proyectos/1', headers=CLAVE).status_code == 200
    assert cliente.get('/proyectos/1').status_code == 404


def test_borrar_sin_clave_no_borra(cliente):
    assert cliente.delete('/proyectos/1').status_code == 401
    assert cliente.get('/proyectos/1').status_code == 200


def test_sin_clave_configurada_la_api_es_solo_lectura(cliente):
    app.config['API_KEY'] = None
    respuesta = cliente.post('/proyectos', json=NUEVO, headers=CLAVE)
    assert respuesta.status_code == 403


# ---------- Página ----------

def test_sin_formspree_muestra_botones_de_contacto(cliente):
    app.config['FORMSPREE_ID'] = ''
    html = cliente.get('/').data
    assert b'formspree.io' not in html
    assert b'Email me' in html


def test_con_formspree_muestra_el_formulario(cliente):
    app.config['FORMSPREE_ID'] = 'abc123'
    html = cliente.get('/').data
    assert b'https://formspree.io/f/abc123' in html
    app.config['FORMSPREE_ID'] = ''


# ---------- Idiomas e interactividad ----------

def test_api_incluye_textos_en_espanol(cliente):
    respuesta = cliente.post('/proyectos', headers=CLAVE, json={
        'titulo': 'Bilingüe', 'descripcion': 'English text', 'descripcion_es': 'Texto en español',
    })
    datos = respuesta.get_json()
    assert datos['descripcion_es'] == 'Texto en español'


def test_pagina_trae_ambos_idiomas_y_la_terminal(cliente):
    html = cliente.get('/').data.decode()
    assert 'data-lang="es"' in html and 'data-lang="en"' in html
    assert 'id="terminal"' in html
    assert 'portfolio.js' in html


def test_archivo_js_se_sirve(cliente):
    assert cliente.get('/static/portfolio.js').status_code == 200
