"""
Respaldo y restauración de los proyectos del portfolio.

    python respaldo.py descargar https://hugoportfolio.pythonanywhere.com
        Guarda todos los proyectos en respaldos/proyectos-AAAA-MM-DD.json.
        No necesita clave: solo lee la API pública.
        GitHub Actions lo corre cada día y guarda el archivo 90 días
        (pestaña Actions → la ejecución → "Artifacts").

    python respaldo.py restaurar respaldos/proyectos-AAAA-MM-DD.json https://hugoportfolio.pythonanywhere.com
        Vuelve a crear los proyectos que falten en el portfolio, a partir de un respaldo.
        Necesita la clave en la variable PORTFOLIO_API_KEY.
        No borra ni pisa nada: solo agrega lo que no esté (compara por repo_url o título).

Por qué existe: si la base de datos se borra o se daña (por un error, un ataque o
un problema del servidor), el portfolio se puede reconstruir en minutos.
"""

import datetime
import json
import os
import sys

from sync_github import pedir_json


def descargar(url_base, carpeta="respaldos", pedir=pedir_json):
    codigo, proyectos = pedir(f"{url_base.rstrip('/')}/proyectos")
    if codigo != 200 or not isinstance(proyectos, list):
        raise RuntimeError(f"No se pudo leer la API: {codigo}")
    os.makedirs(carpeta, exist_ok=True)
    nombre = os.path.join(carpeta, f"proyectos-{datetime.date.today().isoformat()}.json")
    with open(nombre, "w", encoding="utf-8") as archivo:
        json.dump(proyectos, archivo, ensure_ascii=False, indent=2)
    return nombre, len(proyectos)


def _clave_de(proyecto):
    return ((proyecto.get("repo_url") or "").rstrip("/").lower(), (proyecto.get("titulo") or "").strip().lower())


def restaurar(proyectos_respaldo, url_base, clave, pedir=pedir_json):
    """Crea en el portfolio los proyectos del respaldo que no existan. Devuelve los títulos creados."""
    url_base = url_base.rstrip("/")
    _, actuales = pedir(f"{url_base}/proyectos")
    urls = {_clave_de(p)[0] for p in actuales if p.get("repo_url")}
    titulos = {_clave_de(p)[1] for p in actuales}

    creados = []
    for proyecto in proyectos_respaldo:
        url, titulo = _clave_de(proyecto)
        if (url and url in urls) or titulo in titulos:
            continue
        datos = {k: v for k, v in proyecto.items() if k != "id"}
        if isinstance(datos.get("tecnologias"), list):
            datos["tecnologias"] = ", ".join(datos["tecnologias"])
        codigo, respuesta = pedir(f"{url_base}/proyectos", "POST", datos, clave)
        if codigo != 201:
            raise RuntimeError(f"No se pudo restaurar {proyecto.get('titulo')}: {codigo} {respuesta}")
        creados.append(proyecto.get("titulo"))
    return creados


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "descargar":
        archivo, total = descargar(sys.argv[2])
        print(f"Respaldo guardado en {archivo} ({total} proyectos).")
    elif len(sys.argv) >= 4 and sys.argv[1] == "restaurar":
        clave = os.environ.get("PORTFOLIO_API_KEY")
        if not clave:
            sys.exit("Falta la variable PORTFOLIO_API_KEY.")
        with open(sys.argv[2], encoding="utf-8") as archivo:
            respaldo = json.load(archivo)
        creados = restaurar(respaldo, sys.argv[3], clave)
        print(f"Restaurados ({len(creados)}): {', '.join(creados) or '—'}")
    else:
        sys.exit(__doc__)
