"""
Sincroniza el portfolio con tus repositorios públicos de GitHub.

Dos formas de usarlo:

    python sync_github.py
        Modo local: escribe directo en la base de datos (tu PC o la consola
        de PythonAnywhere).

    python sync_github.py --remoto https://hugoportfolio.pythonanywhere.com
        Modo remoto: NO toca la base de datos; agrega los repos nuevos
        llamando a tu propia API (POST /proyectos) con la clave secreta
        PORTFOLIO_API_KEY. Es el que usa GitHub Actions cada día.

Qué hace:
  - Consulta la API pública de GitHub: https://api.github.com/users/<usuario>/repos
  - Si encuentra un repo que todavía no está en la base de datos, lo AGREGA.
  - Si el proyecto ya existe, completa lo que falte: la descripción y el link si
    están vacíos, y agrega los topics nuevos a las tecnologías. Esto pasa también
    en el modo remoto (GitHub Actions), así que si escribes la descripción o los
    topics en GitHub después de crear el repo, aparecen solos al día siguiente.
    Nunca pisa lo que escribiste a mano (descripción en español, emoji, título, etc.).
  - No borra nada: si eliminas un repo de GitHub, lo quitas tú desde la API.

Lo que toma de cada repo (lo editas en GitHub, en el engrane ⚙ de "About"):
  - Description  -> descripción del proyecto
  - Website      -> botón "Live site"
  - Topics       -> etiquetas de tecnologías (ej. python, flask, opencv)
  - Language     -> también se agrega como tecnología
  - Si es fork   -> etiqueta "Fork · Coursework"

Para ocultar un repo del portfolio, ponle el topic:  hide-from-portfolio

La automatización diaria vive en .github/workflows/portfolio.yml (GitHub Actions).
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

from etiquetas import etiqueta_bonita

USUARIO = os.environ.get("GITHUB_USER", "krma12")

# Repos que nunca se muestran (por ejemplo, el README especial de tu perfil)
IGNORAR = {USUARIO}
TOPIC_OCULTAR = "hide-from-portfolio"

# Cómo se escriben bonito algunos topics de GitHub (que siempre van en minúsculas)
NOMBRES_TOPICS = {
    "python": "Python", "flask": "Flask", "sqlite": "SQLite", "sqlalchemy": "SQLAlchemy",
    "opencv": "OpenCV", "mediapipe": "Mediapipe", "numpy": "NumPy", "pandas": "Pandas",
    "jupyter": "Jupyter", "pygame": "Pygame", "javascript": "JavaScript", "html": "HTML",
    "css": "CSS", "leaflet": "Leaflet", "rest-api": "REST API", "oop": "OOP",
    "kali-linux": "Kali Linux", "cybersecurity": "Cybersecurity", "networking": "Networking",
    "machine-learning": "Machine Learning", "computer-vision": "Computer Vision",
    "data-analysis": "Data Analysis", "scikit-learn": "scikit-learn",
}
LENGUAJES = {"Jupyter Notebook": "Jupyter"}
EMOJIS = {"Python": "🐍", "Jupyter Notebook": "📓", "HTML": "🌐", "JavaScript": "✨", "CSS": "🎨"}


def obtener_repos():
    """Descarga la lista de repos públicos (incluye forks) desde la API de GitHub."""
    url = f"https://api.github.com/users/{USUARIO}/repos?per_page=100&sort=created"
    peticion = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolio-sync",  # GitHub exige un User-Agent
    })
    # Opcional: con un token se pueden hacer más consultas por hora (no es necesario)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        peticion.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(peticion, timeout=20) as respuesta:
        return json.load(respuesta)


def titulo_bonito(nombre_repo):
    """'Space_Invaders' -> 'Space Invaders' ; 'mi-bitacora' -> 'Mi Bitacora'
    GitHub no acepta acentos en el nombre y pone un guion: 'automatizaci-n' -> 'Automatización'."""
    nombre_repo = re.sub(r"ci-n(?=$|[_\-])", "ción", nombre_repo)
    palabras = nombre_repo.replace("_", " ").replace("-", " ").split()
    return " ".join(p if p.isupper() or any(c.isupper() for c in p[1:]) else p.capitalize() for p in palabras)


def tecnologias_de(repo):
    """Junta el lenguaje principal y los topics en "Python, Flask, SQLite"."""
    lista = []
    lenguaje = repo.get("language")
    if lenguaje:
        lista.append(LENGUAJES.get(lenguaje, lenguaje))
    for topic in repo.get("topics") or []:
        if topic == TOPIC_OCULTAR:
            continue
        nombre = NOMBRES_TOPICS.get(topic) or etiqueta_bonita(topic)
        if nombre not in lista:
            lista.append(nombre)
    return ", ".join(lista)


def unir_tecnologias(actuales, repo):
    """
    Junta las tecnologías que ya tiene el proyecto con las de GitHub (lenguaje + topics).
    Nunca quita ninguna: solo agrega las que falten. Devuelve None si no hay nada nuevo.
    """
    actuales = [t.strip() for t in (actuales or []) if t and t.strip()]
    ya = {t.lower() for t in actuales}
    nuevas = [t.strip() for t in tecnologias_de(repo).split(",") if t.strip() and t.strip().lower() not in ya]
    if not nuevas:
        return None
    unidas = actuales + nuevas
    while len(", ".join(unidas)) > 600 and len(unidas) > len(actuales):   # la API acepta hasta 600
        unidas.pop()
    return ", ".join(unidas) if len(unidas) > len(actuales) else None


def campos_a_completar(proyecto, repo):
    """
    Compara un proyecto del portfolio (como dict) con su repo de GitHub y devuelve
    solo los campos que se pueden completar, SIN pisar lo que ya escribiste:
      - descripcion y demo_url: solo si en el portfolio están vacíos
      - tecnologias: agrega los topics nuevos de GitHub a los que ya había
      - es_fork: lo marca si GitHub dice que es fork
    """
    cambios = {}
    if not proyecto.get("descripcion") and repo.get("description"):
        cambios["descripcion"] = repo["description"][:500]
    if not proyecto.get("demo_url") and repo.get("homepage"):
        cambios["demo_url"] = repo["homepage"]
    tecnologias = proyecto.get("tecnologias") or []
    if isinstance(tecnologias, str):
        tecnologias = tecnologias.split(",")
    unidas = unir_tecnologias(tecnologias, repo)
    if unidas:
        cambios["tecnologias"] = unidas
    if repo.get("fork") and not proyecto.get("es_fork"):
        cambios["es_fork"] = True
    return cambios


def debe_mostrarse(repo):
    return (
        repo["name"] not in IGNORAR
        and TOPIC_OCULTAR not in (repo.get("topics") or [])
        and not repo.get("archived")
        and not repo.get("private")
    )


def datos_proyecto(repo, orden):
    """Traduce un repo de GitHub a los campos de un Proyecto."""
    return {
        "titulo": titulo_bonito(repo["name"]),
        "descripcion": (repo.get("description") or "")[:500],   # la API acepta hasta 500
        "repo_url": repo["html_url"].rstrip("/"),
        "demo_url": repo.get("homepage") or None,
        "tecnologias": unir_tecnologias([], repo) or "",
        "emoji": EMOJIS.get(repo.get("language"), "🚀"),
        "es_fork": bool(repo.get("fork")),
        "orden": orden,
    }


def sincronizar(repos, db, Proyecto):
    """
    Agrega los repos nuevos y rellena huecos en los existentes.
    Devuelve (agregados, actualizados) para poder mostrar un resumen.
    """
    existentes = {(p.repo_url or "").rstrip("/").lower(): p for p in Proyecto.query.all()}
    siguiente_orden = max([p.orden or 0 for p in existentes.values()] + [-1]) + 1
    agregados, actualizados = [], []

    for repo in repos:
        if not debe_mostrarse(repo):
            continue

        url = repo["html_url"].rstrip("/")
        proyecto = existentes.get(url.lower())

        if proyecto is None:
            proyecto = Proyecto(**datos_proyecto(repo, siguiente_orden))
            db.session.add(proyecto)
            siguiente_orden += 1
            agregados.append(proyecto.titulo)
            continue

        # Ya existe: solo completamos lo que falte, sin tocar lo escrito a mano
        cambios = campos_a_completar({
            "descripcion": proyecto.descripcion,
            "demo_url": proyecto.demo_url,
            "tecnologias": proyecto.tecnologias,
            "es_fork": proyecto.es_fork,
        }, repo)
        for campo, valor in cambios.items():
            setattr(proyecto, campo, valor)
        if cambios:
            actualizados.append(proyecto.titulo)

    db.session.commit()
    return agregados, actualizados


# ---------------------------------------------------------------------------
# Modo remoto: hablar con el portfolio publicado a través de su propia API
# ---------------------------------------------------------------------------
def pedir_json(url, metodo="GET", datos=None, clave=None):
    """Hace una petición HTTP y devuelve (código, json)."""
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    peticion = urllib.request.Request(url, data=cuerpo, method=metodo, headers={
        "Content-Type": "application/json",
        "User-Agent": "portfolio-sync",
    })
    if clave:
        peticion.add_header("X-API-Key", clave)
    try:
        with urllib.request.urlopen(peticion, timeout=30) as respuesta:
            return respuesta.status, json.load(respuesta)
    except urllib.error.HTTPError as error:
        # 401, 403, 404…: devolvemos el código para que quien llama decida qué hacer
        return error.code, json.loads(error.read() or b"{}")


def sincronizar_remoto(repos, url_base, clave, pedir=pedir_json):
    """
    Sincroniza el portfolio publicado a través de su API:
      - Agrega los repos que todavía no tiene (POST /proyectos).
      - En los que ya tiene, completa la descripción, el link y los topics
        que falten (PUT /proyectos/<id>), sin pisar lo que escribiste a mano.
    Devuelve (agregados, actualizados).
    """
    url_base = url_base.rstrip("/")
    _, existentes = pedir(f"{url_base}/proyectos")
    por_url = {(p.get("repo_url") or "").rstrip("/").lower(): p for p in existentes}
    siguiente_orden = max([p.get("orden") or 0 for p in existentes] + [-1]) + 1

    agregados, actualizados = [], []
    for repo in repos:
        if not debe_mostrarse(repo):
            continue
        proyecto = por_url.get(repo["html_url"].rstrip("/").lower())

        if proyecto is None:
            codigo, creado = pedir(f"{url_base}/proyectos", "POST", datos_proyecto(repo, siguiente_orden), clave)
            if codigo != 201:
                raise RuntimeError(f"No se pudo agregar {repo['name']}: {codigo} {creado}")
            agregados.append(creado["titulo"])
            siguiente_orden += 1
            continue

        cambios = campos_a_completar(proyecto, repo)
        if not cambios:
            continue
        # PUT reemplaza el proyecto completo: mandamos todo lo que ya tenía + los cambios
        datos = {k: v for k, v in proyecto.items() if k != "id"}
        if isinstance(datos.get("tecnologias"), list):
            datos["tecnologias"] = ", ".join(datos["tecnologias"])
        datos.update(cambios)
        codigo, respuesta = pedir(f"{url_base}/proyectos/{proyecto['id']}", "PUT", datos, clave)
        if codigo != 200:
            raise RuntimeError(f"No se pudo actualizar {proyecto['titulo']}: {codigo} {respuesta}")
        actualizados.append(proyecto["titulo"])
    return agregados, actualizados


if __name__ == "__main__":
    repos = obtener_repos()
    print(f"GitHub: {len(repos)} repos encontrados.")

    if "--remoto" in sys.argv:
        url = sys.argv[sys.argv.index("--remoto") + 1]
        clave = os.environ.get("PORTFOLIO_API_KEY")
        if not clave:
            sys.exit("Falta la variable PORTFOLIO_API_KEY.")
        agregados, actualizados = sincronizar_remoto(repos, url, clave)
        print(f"Agregados en {url} ({len(agregados)}): {', '.join(agregados) or '—'}")
        print(f"Actualizados ({len(actualizados)}): {', '.join(actualizados) or '—'}")
    else:
        from app import app
        from models import Proyecto, db

        with app.app_context():
            agregados, actualizados = sincronizar(repos, db, Proyecto)
            print(f"Agregados ({len(agregados)}): {', '.join(agregados) or '—'}")
            print(f"Actualizados ({len(actualizados)}): {', '.join(actualizados) or '—'}")
