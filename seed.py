"""
Script to fill the database with your real GitHub projects.
Run it with the virtual environment activated:

    python seed.py

It rebuilds the table from scratch and loads this list, so you can re-run it
any time you change the info below (or add new columns to the model).
"""

from app import app
from models import Proyecto, db

proyectos = [
    {
        "titulo": "Face Filter",
        "descripcion": "Real-time augmented reality filters: detects 478 facial landmarks and overlays glasses, a mustache, ears or a hat that follow your head.",
        "resultado": "Real-time tracking with 7 filter combos",
        "descripcion_es": "Filtros de realidad aumentada en tiempo real: detecta 478 puntos de la cara y coloca lentes, bigote, orejas o un gorro que siguen tu cabeza.",
        "resultado_es": "Seguimiento en tiempo real con 7 combos de filtros",
        "repo_url": "https://github.com/krma12/Filtro_Facial",
        "tecnologias": "Python, OpenCV, Mediapipe, NumPy",
        "emoji": "🎭",
    },
    {
        "titulo": "Space Invaders",
        "descripcion": "Space Invaders clone built with Pygame, featuring power-ups, a leaderboard, and enemies that shoot back.",
        "resultado": "Fully playable game",
        "descripcion_es": "Versión de Space Invaders hecha con Pygame, con power-ups, tabla de récords y enemigos que disparan.",
        "resultado_es": "Juego completamente jugable",
        "repo_url": "https://github.com/krma12/Space_Invaders",
        "tecnologias": "Python, Pygame, OOP",
        "emoji": "👾",
    },
    {
        "titulo": "TaskFlow",
        "descripcion": "Productivity app (task manager) with full CRUD, a modern interface and object-oriented design.",
        "resultado": "Full CRUD working",
        "descripcion_es": "App de productividad (gestor de tareas) con CRUD completo, interfaz moderna y diseño orientado a objetos.",
        "resultado_es": "CRUD completo funcionando",
        "repo_url": "https://github.com/krma12/Task_Flow",
        "tecnologias": "Python, Flask, SQLite, OOP",
        "emoji": "✅",
    },
    {
        "titulo": "Mexico Crime Data Analysis",
        "descripcion": "Data cleaning, transformation and exploratory analysis of state-level crime incidence in Mexico, using the National Crime Incidence Registry (RNID).",
        "resultado": "Full exploratory analysis",
        "descripcion_es": "Limpieza, transformación y análisis exploratorio de la incidencia delictiva por estado en México, con datos del Registro Nacional de Incidencia Delictiva (RNID).",
        "resultado_es": "Análisis exploratorio completo",
        "repo_url": "https://github.com/krma12/analisis-rnid-mexico",
        "tecnologias": "Python, Pandas, Jupyter",
        "emoji": "📊",
    },
    {
        "titulo": "My Logbook (Bitácora)",
        "descripcion": "A digital logbook of my journey from veterinary school to AI engineering, with an interactive map and a design that turns from paper diary into terminal.",
        "resultado": "Live on GitHub Pages",
        "descripcion_es": "Bitácora digital de mi camino, de la veterinaria a la ingeniería en IA, con un mapa interactivo y un diseño que pasa de diario de papel a terminal.",
        "resultado_es": "Publicada en GitHub Pages",
        "repo_url": "https://github.com/krma12/mi-bitacora",
        "demo_url": "https://krma12.github.io/mi-bitacora/",
        "tecnologias": "HTML, CSS, JavaScript, Leaflet",
        "emoji": "📓",
    },
    {
        "titulo": "Portfolio + Flask API",
        "descripcion": "This same portfolio: projects are stored in a database and served through a REST API protected with an API key.",
        "resultado": "Secured CRUD API",
        "descripcion_es": "Este mismo portfolio: los proyectos viven en una base de datos y se sirven con una API REST protegida con clave.",
        "resultado_es": "API CRUD protegida",
        "repo_url": "https://github.com/krma12/portfolio-flask",
        "tecnologias": "Python, Flask, SQLAlchemy, REST API",
        "emoji": "🌐",
    },
    {
        "titulo": "Image Processing with NumPy",
        "descripcion": "Interactive notebooks on multidimensional arrays and basic image analysis.",
        "resultado": "Interactive notebooks",
        "descripcion_es": "Notebooks interactivos sobre arreglos multidimensionales y análisis básico de imágenes.",
        "resultado_es": "Notebooks interactivos",
        "repo_url": "https://github.com/krma12/Image-Processing-with-NumPy",
        "tecnologias": "Python, NumPy, Jupyter",
        "emoji": "🖼️",
    },
    {
        "titulo": "Kali/Win7 Pentest Lab",
        "descripcion": "Isolated home lab (Kali + Windows 7) with network troubleshooting and a write-up, built for certification practice.",
        "resultado": "Functional isolated lab",
        "descripcion_es": "Laboratorio casero y aislado (Kali + Windows 7) con troubleshooting de red y un write-up, para practicar rumbo a certificaciones.",
        "resultado_es": "Laboratorio aislado funcional",
        "repo_url": "https://github.com/krma12/kali-win7-pentest-labs",
        "tecnologias": "Kali Linux, Networking, Cybersecurity",
        "emoji": "🛡️",
    },
    {
        "titulo": "Kali/Win7 DoublePulsar Lab",
        "descripcion": "A second isolated home lab (Kali + Windows 7) for certification practice.",
        "resultado": "Functional isolated lab",
        "descripcion_es": "Un segundo laboratorio casero y aislado (Kali + Windows 7) para practicar rumbo a certificaciones.",
        "resultado_es": "Laboratorio aislado funcional",
        "repo_url": "https://github.com/krma12/kali-win7-doublepulsar-lab",
        "tecnologias": "Kali Linux, Cybersecurity",
        "emoji": "🔐",
    },
]

with app.app_context():
    # drop_all + create_all rebuilds the table, so new columns in models.py
    # (like "tecnologias" or "emoji") always exist. It only touches local test data.
    db.drop_all()
    db.create_all()

    for posicion, datos in enumerate(proyectos):
        db.session.add(Proyecto(orden=posicion, **datos))

    db.session.commit()
    print(f"Added {len(proyectos)} projects to the database.")
