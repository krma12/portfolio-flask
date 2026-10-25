"""
Pruebas de la sincronización con GitHub.
Usan repos "falsos" (con la misma forma que responde la API de GitHub),
así no necesitan internet.
"""

import os

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['PORTFOLIO_API_KEY'] = 'clave-de-prueba'

import pytest  # noqa: E402

from app import app  # noqa: E402
from models import Proyecto, db  # noqa: E402
from sync_github import sincronizar, tecnologias_de, titulo_bonito  # noqa: E402


def repo(nombre, **extra):
    """Crea un repo de mentira con los campos que usa sync_github.py."""
    datos = {
        "name": nombre,
        "html_url": f"https://github.com/krma12/{nombre}",
        "description": f"Descripción de {nombre}",
        "homepage": "",
        "language": "Python",
        "topics": [],
        "fork": False,
        "archived": False,
        "private": False,
    }
    datos.update(extra)
    return datos


@pytest.fixture
def contexto():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Proyecto(
            titulo='Face Filter', descripcion='Escrita a mano', descripcion_es='En español',
            repo_url='https://github.com/krma12/Filtro_Facial', emoji='🎭', orden=0,
        ))
        db.session.commit()
        yield


def test_agrega_repos_nuevos(contexto):
    agregados, _ = sincronizar([repo("Nuevo_Proyecto", topics=["flask", "sqlite"])], db, Proyecto)
    assert agregados == ["Nuevo Proyecto"]
    nuevo = Proyecto.query.filter_by(titulo="Nuevo Proyecto").one()
    assert nuevo.tecnologias == "Python, Flask, SQLite"
    assert nuevo.orden == 1


def test_no_duplica_ni_pisa_lo_escrito_a_mano(contexto):
    sincronizar([repo("Filtro_Facial", description="Otra descripción")], db, Proyecto)
    assert Proyecto.query.count() == 1
    proyecto = Proyecto.query.one()
    assert proyecto.descripcion == "Escrita a mano"
    assert proyecto.descripcion_es == "En español"


def test_rellena_campos_vacios(contexto):
    _, actualizados = sincronizar([repo("Filtro_Facial", homepage="https://demo.example")], db, Proyecto)
    assert actualizados == ["Face Filter"]
    assert Proyecto.query.one().demo_url == "https://demo.example"


def test_marca_forks(contexto):
    sincronizar([repo("numpy", fork=True, language="Jupyter Notebook")], db, Proyecto)
    fork = Proyecto.query.filter_by(titulo="Numpy").one()
    assert fork.es_fork is True
    assert fork.tecnologias == "Jupyter"


def test_ignora_ocultos_archivados_y_perfil(contexto):
    agregados, _ = sincronizar([
        repo("Secreto", topics=["hide-from-portfolio"]),
        repo("Viejo", archived=True),
        repo("krma12"),
    ], db, Proyecto)
    assert agregados == []


def test_ayudantes():
    assert titulo_bonito("Space_Invaders") == "Space Invaders"
    assert titulo_bonito("analisis-rnid-mexico") == "Analisis Rnid Mexico"
    assert tecnologias_de({"language": "Python", "topics": ["kali-linux", "python"]}) == "Python, Kali Linux"


# ---------- Modo remoto (el que usa GitHub Actions) ----------

def test_sincronizar_remoto_solo_agrega_lo_nuevo():
    from sync_github import sincronizar_remoto

    llamadas = []

    def pedir_falso(url, metodo="GET", datos=None, clave=None):
        llamadas.append((metodo, url, clave))
        if metodo == "GET":
            return 200, [{"repo_url": "https://github.com/krma12/Filtro_Facial", "orden": 4}]
        return 201, {"titulo": datos["titulo"], "orden": datos["orden"]}

    agregados = sincronizar_remoto(
        [repo("Filtro_Facial"), repo("Nuevo_Repo"), repo("Oculto", topics=["hide-from-portfolio"])],
        "https://ejemplo.com/", "clave", pedir=pedir_falso,
    )
    assert agregados == ["Nuevo Repo"]
    assert llamadas[-1] == ("POST", "https://ejemplo.com/proyectos", "clave")


def test_sincronizar_remoto_avisa_si_la_clave_falla():
    from sync_github import sincronizar_remoto

    def pedir_falso(url, metodo="GET", datos=None, clave=None):
        return (200, []) if metodo == "GET" else (401, {"mensaje": "Clave inválida"})

    with pytest.raises(RuntimeError):
        sincronizar_remoto([repo("Nuevo")], "https://ejemplo.com", "mala", pedir=pedir_falso)
