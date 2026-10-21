"""
Script to fill the database with your real GitHub projects.
Run this ONCE (with the virtual environment activated):

    python seed.py

It deletes whatever projects currently exist and replaces them with this
list, so you can re-run it any time you want to update the info.
"""

from app import app
from models import db, Proyecto

proyectos = [
    {
        "titulo": "TaskFlow",
        "descripcion": "Productivity app (task manager) built in Python + Flask + SQLite, with full CRUD and a modern interface.",
        "resultado": "Full CRUD working",
        "repo_url": "https://github.com/krma12/Task_Flow",
    },
    {
        "titulo": "Space Invaders",
        "descripcion": "Space Invaders clone built in Python with Pygame, featuring power-ups, a leaderboard, and enemies that shoot back.",
        "resultado": "Fully playable game",
        "repo_url": "https://github.com/krma12/Space_Invaders",
    },
    {
        "titulo": "Portfolio + Flask API",
        "descripcion": "This same portfolio: built with Flask, SQLAlchemy, and a REST API for managing projects.",
        "resultado": "Full CRUD working",
        "repo_url": "https://github.com/krma12/portfolio-flask",
    },
    {
        "titulo": "Face Filter",
        "descripcion": "Real-time augmented reality filter application built with Python, OpenCV, and Mediapipe.",
        "resultado": "Real-time face detection",
        "repo_url": "https://github.com/krma12/Filtro_Facial",
    },
    {
        "titulo": "Mexico Crime Data Analysis",
        "descripcion": "Data cleaning, transformation, and exploratory data analysis of state-level crime incidence in Mexico, using the National Crime Incidence Registry (RNID).",
        "resultado": "Full exploratory analysis",
        "repo_url": "https://github.com/krma12/analisis-rnid-mexico",
    },
    {
        "titulo": "Image Processing with NumPy",
        "descripcion": "Image processing and multidimensional array manipulation using NumPy and Jupyter.",
        "resultado": "Interactive notebooks",
        "repo_url": "https://github.com/krma12/Image-Processing-with-NumPy",
    },
    {
        "titulo": "Kali/Win7 Pentest Lab",
        "descripcion": "Isolated cybersecurity lab environment for certification practice.",
        "resultado": "Functional lab",
        "repo_url": "https://github.com/krma12/kali-win7-pentest-labs",
    },
    {
        "titulo": "Kali/Win7 DoublePulsar Lab",
        "descripcion": "Isolated cybersecurity lab environment for certification practice.",
        "resultado": "Functional lab",
        "repo_url": "https://github.com/krma12/kali-win7-doublepulsar-lab",
    },
]

with app.app_context():
    db.create_all()  # in case the table doesn't exist yet

    Proyecto.query.delete()  # clear whatever is there

    for datos in proyectos:
        db.session.add(Proyecto(**datos))

    db.session.commit()
    print(f"Added {len(proyectos)} projects to the database.")
