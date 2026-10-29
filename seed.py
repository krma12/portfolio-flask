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
        "demo_url": "https://hugoportfolio.pythonanywhere.com/",
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
        "titulo": "Cybersecurity Research Lab",
        "descripcion": "Isolated home lab where I reproduce and document critical Windows vulnerabilities (EternalBlue, DoublePulsar, BlueKeep, SMBGhost) and turn them into defensive fixes.",
        "resultado": "4 vulnerabilities documented · SIEM/EDR lab in progress",
        "descripcion_es": "Laboratorio casero y aislado donde reproduzco y documento vulnerabilidades críticas de Windows (EternalBlue, DoublePulsar, BlueKeep, SMBGhost) y las traduzco en medidas defensivas.",
        "resultado_es": "4 vulnerabilidades documentadas · laboratorio SIEM/EDR en progreso",
        "repo_url": "https://github.com/krma12/cybersecurity-research-lab",
        "tecnologias": "Kali Linux, Networking, Cybersecurity, SMB, RDP",
        "emoji": "🛡️",
    },
    # ---- Forks: ejercicios de clase (se muestran con la etiqueta "Fork · Coursework") ----
    {
        "titulo": "Pandas & EDA",
        "descripcion": "Coursework on Pandas fundamentals and exploratory data analysis, step by step, using the IMDB movies dataset (2006–2016).",
        "resultado": "Complete EDA notebook",
        "descripcion_es": "Ejercicios de clase sobre fundamentos de Pandas y análisis exploratorio de datos, paso a paso, con el dataset de películas de IMDB (2006–2016).",
        "resultado_es": "Notebook de EDA completo",
        "repo_url": "https://github.com/krma12/Pandas_Introduction",
        "tecnologias": "Python, Pandas, Jupyter",
        "emoji": "🐼",
        "es_fork": True,
    },
    {
        "titulo": "NumPy Practice",
        "descripcion": "Coursework on advanced NumPy: multidimensional arrays, random matrices and basic image analysis.",
        "resultado": "Exercise notebooks",
        "descripcion_es": "Ejercicios de clase de NumPy avanzado: arreglos multidimensionales, matrices aleatorias y análisis básico de imágenes.",
        "resultado_es": "Notebooks de ejercicios",
        "repo_url": "https://github.com/krma12/numpy",
        "tecnologias": "Python, NumPy, Jupyter",
        "emoji": "🧮",
        "es_fork": True,
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
