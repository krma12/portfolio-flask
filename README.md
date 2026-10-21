# Hugo Maldonado — Portfolio

Personal portfolio website built with Flask, SQLAlchemy, and a REST API for managing projects. The project list on the site is not hardcoded — it's stored in a real database and served dynamically through a CRUD API.

Live projects shown on the site are pulled from `proyectos.db` and rendered with Jinja2.

## Features

- Responsive landing page (hero, about, skills, projects, contact) with light/dark mode.
- REST API (`/proyectos`) with full CRUD: list, create, update, and delete projects.
- Projects section renders dynamically from the database — no hardcoded HTML per project.
- Contact form and accessible navigation (skip link, reduced-motion support).

## Tech stack

- **Backend:** Python, Flask, Flask-RESTful
- **Database:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, Jinja2 (no JS framework)

## Project structure

```
Servicios_Web/
├── app.py              # Flask app setup and database config
├── routes.py           # Maps URLs to resource classes
├── resources.py        # Route logic (GET/POST/PUT/DELETE)
├── models.py           # Proyecto model (SQLAlchemy)
├── seed.py             # Script to populate the database with real projects
├── requirements.txt    # Project dependencies
├── Templates/
│   └── landing_page.html
└── static/
    └── foto.jpg
```

## Installation

1. Clone the repository and enter the folder:
   ```
   git clone https://github.com/krma12/portfolio-flask.git
   cd portfolio-flask
   ```

2. Create and activate a virtual environment:
   ```
   # Windows (PowerShell)
   py -m venv mi_entorno
   .\mi_entorno\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Seed the database with the real projects:
   ```
   python seed.py
   ```

## Usage

```
python app.py
```

Open `http://127.0.0.1:8000/` in your browser.

## API endpoints

| Method | Endpoint          | Description              |
|--------|-------------------|---------------------------|
| GET    | `/proyectos`      | List all projects         |
| POST   | `/proyectos`      | Create a new project      |
| GET    | `/proyectos/<id>` | Get a single project      |
| PUT    | `/proyectos/<id>` | Update a project          |
| DELETE | `/proyectos/<id>` | Delete a project          |

## Author

Hugo Maldonado ([@krma12](https://github.com/krma12)) — AI Engineering student building projects in Python, data, and computer vision.
