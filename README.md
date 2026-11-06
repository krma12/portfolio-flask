# Hugo Maldonado — Portfolio

**Live:** [hugoportfolio.pythonanywhere.com](https://hugoportfolio.pythonanywhere.com) · **Project report (Spanish):** [docs/REPORTE.md](docs/REPORTE.md)

[![Mozilla HTTP Observatory: A+](https://img.shields.io/badge/Mozilla_Observatory-A%2B_%28110%2F100%29-brightgreen)](https://developer.mozilla.org/en-US/observatory/analyze?host=hugoportfolio.pythonanywhere.com)

Personal portfolio built with Flask, SQLAlchemy and a REST API. The project list isn't hardcoded: it lives in a database, is managed through a key-protected CRUD API, and syncs itself every day with my GitHub repositories.

## Features

- Responsive landing page (hero, about, skills, projects, contact) with light/dark mode and English/Spanish.
- REST API (`/proyectos`) with full CRUD. Writes require an API key.
- Projects render dynamically from the database, with technology filters, a live JSON view and an interactive terminal (`help`, `projects --tag security`, `theme light`…).
- Daily GitHub sync: new repositories are added, and the description, website and topics of existing ones are filled in without overwriting hand-written content.
- Contact form (Formspree) with an anti-spam honeypot.
- Hardened security (see [Security](#security)), security event logging, daily backups and 50 automated tests.

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
├── respaldo.py         # Daily backup of all projects + restore script
├── seed.py             # Populates the database with the initial projects
├── templates/
│   └── landing_page.html
├── static/             # main.js, portfolio.js, images, favicon
├── tests/              # API, sync, backup and security tests
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

**Result:** A+ on [Mozilla HTTP Observatory](https://developer.mozilla.org/en-US/observatory/analyze?host=hugoportfolio.pythonanywhere.com) — 110/100, 12/12 tests passed (November 2026).

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
| **Logging** | Security events (invalid keys, blocked IPs, created/edited/deleted projects) are written to the server log with IP and route — never the key itself. |
| **Backups** | A daily GitHub Actions job downloads every project to JSON and keeps it for 90 days; `respaldo.py restaurar` rebuilds the portfolio from a backup. |
| **Regression tests** | 18 security tests check headers, link validation, escaping, rate limiting and logging, so a protection can't silently disappear. |

### Security model: CIA triad & ISC2 CC domains

How each control in this project maps to the CIA triad and to the five domains of the ISC2 Certified in Cybersecurity (CC) exam:

| CIA | Controls in this project |
|---|---|
| **Confidentiality** | Secrets only in environment variables / GitHub Secrets · HTTPS + HSTS · `Referrer-Policy` · the key is never logged |
| **Integrity** | Only the key holder can write · input validation (https-only links, length limits) · output escaping + CSP against XSS · tests that fail if a control disappears |
| **Availability** | Read access is always public · rate limiting stops brute force without blocking readers · daily backups with a restore script · dependency updates |

| ISC2 CC domain | How it's applied |
|---|---|
| **1. Security Principles** | Least privilege (public read, keyed write) · fail closed (no key configured = read-only) · defense in depth (validation + escaping + CSP) |
| **2. Business Continuity, DR & Incident Response** | Daily backups kept 90 days and a tested restore script (recovery) · an exposed key was rotated immediately (incident response) |
| **3. Access Control Concepts** | API-key authentication · constant-time comparison · lockout after repeated failures (`429`) |
| **4. Network Security** | HTTPS enforced · HSTS · CSP · clickjacking protection (`frame-ancestors`, `X-Frame-Options`) |
| **5. Security Operations** | Security event logging · CI tests on every push · `pip-audit` + Dependabot · secrets management · debug mode off in production |

**Known limits:** the database is SQLite on a single server, rate limiting is kept in memory (it resets when the app reloads), and logs live in the hosting provider's server log rather than a central SIEM.

Found a security issue? Please contact me privately through [LinkedIn](https://www.linkedin.com/in/hugo-maldonado-a20445201) instead of opening a public issue.

## Author

Hugo Maldonado ([@krma12](https://github.com/krma12)) — AI Engineering student focused on cybersecurity, building projects in Python, data and computer vision.
