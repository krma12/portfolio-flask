# Hugo Maldonado — Portfolio

**Live:** [hugoportfolio.pythonanywhere.com](https://hugoportfolio.pythonanywhere.com) · **Project report (Spanish):** [docs/REPORTE.md](docs/REPORTE.md)

Personal portfolio built with Flask, SQLAlchemy and a REST API. The project list isn't hardcoded: it lives in a database, is managed through a key-protected CRUD API, and syncs itself every day with my GitHub repositories.

## Features

- Responsive landing page (hero, about, skills, projects, contact) with light/dark mode and English/Spanish.
- REST API (`/proyectos`) with full CRUD. Writes require an API key.
- Projects render dynamically from the database, with technology filters, a live JSON view and an interactive terminal (`help`, `projects --tag security`, `theme light`…).
- Daily GitHub sync: new repositories are added, and the description, website and topics of existing ones are filled in without overwriting hand-written content.
- Contact form (Formspree) with an anti-spam honeypot.
- Hardened security (see [Security](#security)) and 45 automated tests.

## Tech stack

- **Backend:** Python, Flask, Flask-RESTful
- **Database:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, Jinja2, vanilla JavaScript
- **Testing & CI:** pytest, GitHub Actions, pip-audit, Dependabot
- **Hosting:** PythonAnywhere (HTTPS)

## Project structure

```
portfolio-flask/
├── app.py              # Flask app setup and configuration (env variables)
├── routes.py           # Maps URLs to resource classes
├── resources.py        # API logic (GET/POST/PUT/DELETE) + input validation
├── models.py           # Proyecto model (SQLAlchemy)
├── seguridad.py        # Security headers, rate limiting, validators
├── etiquetas.py        # Clean technology tag names (AI, API, LLM…)
├── sync_github.py      # Syncs the portfolio with my GitHub repositories
├── seed.py             # Populates the database with the initial projects
├── templates/
│   └── landing_page.html
├── static/             # main.js, portfolio.js, images, favicon
├── tests/              # API, sync and security tests
├── docs/REPORTE.md     # Project report: purpose, history, concepts
└── .github/            # CI workflow + Dependabot
```

## Installation

```bash
git clone https://github.com/krma12/portfolio-flask.git
cd portfolio-flask
python -m venv mi_entorno
.\mi_entorno\Scripts\Activate.ps1      # Windows (PowerShell)
pip install -r requirements.txt
python seed.py                         # optional: load the initial projects
```

## Usage

```bash
# The API key protects create/update/delete. Without it the API is read-only.
$env:PORTFOLIO_API_KEY = "<your-secret-key>"   # PowerShell
python app.py
```

Open `http://127.0.0.1:8000/`. Debug mode is off unless you set `FLASK_DEBUG=1`.

## Tests

```bash
python -m pytest -v
```

GitHub Actions runs the tests and a dependency audit on every push.

## API endpoints

| Method | Endpoint          | Description         | Auth |
|--------|-------------------|---------------------|------|
| GET    | `/proyectos`      | List all projects   | —    |
| POST   | `/proyectos`      | Create a project    | `X-API-Key` |
| GET    | `/proyectos/<id>` | Get one project     | —    |
| PUT    | `/proyectos/<id>` | Replace a project   | `X-API-Key` |
| DELETE | `/proyectos/<id>` | Delete a project    | `X-API-Key` |

`PUT` replaces the whole project, so send every field, not just the one that changes.

## Security

| Area | What's in place |
|---|---|
| **Authentication** | Writes require an `X-API-Key` header. The key comes from an environment variable and is compared in constant time (`hmac.compare_digest`). With no key configured, the API fails closed and becomes read-only. |
| **Brute-force protection** | 5 failed key attempts within 10 minutes block that IP for 15 minutes (`429 Too Many Requests` + `Retry-After`). Reading is never blocked. |
| **Input validation** | `repo_url` and `demo_url` only accept `https://` links (`javascript:`, `data:` and `http:` are rejected), and every field has a maximum length. |
| **XSS** | Jinja2 auto-escaping on the server, and HTML escaping in the terminal and JSON view on the client. |
| **Content-Security-Policy** | Scripts only from the site itself (no inline scripts or event handlers), fonts only from Google Fonts, the form only posts to Formspree, `object-src 'none'`, `base-uri 'self'`. |
| **Transport** | HTTPS enforced + `Strict-Transport-Security`. |
| **Clickjacking** | `frame-ancestors 'none'` + `X-Frame-Options: DENY`. |
| **Other headers** | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (no camera, mic or location). |
| **Production config** | Debug mode off by default. Secrets only in environment variables and GitHub Secrets, never in the repo. Keys are rotated if exposed. |
| **Spam** | Honeypot field in the contact form. |
| **Dependencies** | `pip-audit` in CI on every push + weekly Dependabot updates. |
| **Regression tests** | 16 security tests check headers, link validation, escaping and rate limiting, so a protection can't silently disappear. |

Found a security issue? Please contact me privately through [LinkedIn](https://www.linkedin.com/in/hugo-maldonado-a20445201) instead of opening a public issue.

## Author

Hugo Maldonado ([@krma12](https://github.com/krma12)) — AI Engineering student focused on cybersecurity, building projects in Python, data and computer vision.
