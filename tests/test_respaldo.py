"""Pruebas del respaldo y la restauración (sin internet: la API es de mentira)."""

import json

from respaldo import descargar, restaurar

RESPALDO = [
    {"id": 1, "titulo": "Face Filter", "repo_url": "https://github.com/krma12/Filtro_Facial", "tecnologias": ["Python"]},
    {"id": 2, "titulo": "Space Invaders", "repo_url": "https://github.com/krma12/Space_Invaders", "tecnologias": ["Python", "Pygame"]},
]


def test_descargar_guarda_un_json(tmp_path):
    def pedir_falso(url, metodo="GET", datos=None, clave=None):
        return 200, RESPALDO

    archivo, total = descargar("https://ejemplo.com", carpeta=str(tmp_path), pedir=pedir_falso)
    assert total == 2
    assert json.load(open(archivo, encoding="utf-8")) == RESPALDO


def test_restaurar_solo_crea_lo_que_falta():
    creados = []

    def pedir_falso(url, metodo="GET", datos=None, clave=None):
        if metodo == "GET":   # el portfolio perdió Space Invaders
            return 200, [{"id": 7, "titulo": "Face Filter", "repo_url": "https://github.com/krma12/Filtro_Facial"}]
        creados.append(datos)
        return 201, datos

    assert restaurar(RESPALDO, "https://ejemplo.com", "clave", pedir=pedir_falso) == ["Space Invaders"]
    assert "id" not in creados[0]
    assert creados[0]["tecnologias"] == "Python, Pygame"


def test_restaurar_sobre_portfolio_vacio_crea_todo():
    def pedir_falso(url, metodo="GET", datos=None, clave=None):
        return (200, []) if metodo == "GET" else (201, datos)

    assert restaurar(RESPALDO, "https://ejemplo.com", "clave", pedir=pedir_falso) == ["Face Filter", "Space Invaders"]
