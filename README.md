# Hugo Maldonado — Portfolio

Personal portfolio website built with Flask, SQLAlchemy, and a REST API for managing projects. The project list on the site is not hardcoded: it's stored in a real database and served dynamically through a CRUD API **protected with an API key**.

## Features

- **Interactive terminal** in the hero: visitors type commands (`whoami`, `projects --tag security`, `skills`, `contact`, `sudo hire-hugo`…). `projects` calls the site's own REST API live. Includes command history (↑/↓), Tab autocomplete and clickable suggestions.
- **Filter projects by technology** (Python, Computer Vision, Web, Data, Security, Games), with counts.
- **"View as JSON"** toggle: shows the real response of `GET /proyectos`, syntax-highlighted, with status code and response time.
- **English / Spanish** toggle for the whole page and the terminal. Project descriptions are stored in both languages in the database.
- Responsive landing page (hero, about, skills, projects, contact) with light/dark mode.
- Projects render dynamically from the database, each with its technologies, key result, GitHub link and live demo (when there is one). Forked coursework repos are labeled "Fork · Coursework".
- Stats calculated automatically from the data (number of projects and tools used).
- REST API (`/proyectos`) with full CRUD. **Reading is public; creating, editing and deleting require an API key.**
- Contact form powered by [Formspree](https://formspree.io), with a honeypot field against spam bots. Without a Formspree ID it falls back to email and LinkedIn buttons.
- Link preview (Open Graph image) for WhatsApp, LinkedIn, etc., and a custom favicon.
- Accessible navigation (skip link, reduced-motion support, ARIA labels).
- Automated tests with pytest.

## Security decisions

| Decision | Why |
|---|---|
| API key in the `X-API-Key` header for POST/PUT/DELETE | Anyone can view the portfolio, but only I can change it. |
| Key read from an environment variable | The secret never lives in the code or on GitHub. |
| No key configured → API is read-only (403) | **Fail closed**: forgetting to configure it can't leave the API open. |
| `hmac.compare_digest` to check the key | Constant-time comparison, so response timing doesn't leak the key. |
| `debug` off unless `FLASK_DEBUG=1` | Flask's debug console allows running code on the server. |

## Tech stack

- **Backend:** Python, Flask, Flask-RESTful
- **Database:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, Jinja2 and vanilla JavaScript (no framework)
- **Testing:** pytest

## Project structure

```
portfolio-flask/
├── app.py              # Flask app setup and configuration (environment variables)
├── routes.py           # Maps URLs to resource classes
├── resources.py        # Route logic (GET/POST/PUT/DELETE) + API key check
├── models.py           # Proyecto model (SQLAlchemy)
├── seed.py             # Loads my real projects into the database
├── requirements.txt    # Pinned dependencies
├── tests/
│   └── test_api.py     # Automated tests for the API and the page
├── templates/
│   └── landing_page.html
└── static/
    ├── portfolio.js    # Terminal, filters, JSON view and EN/ES toggle
    ├── foto.jpg
    ├── favicon.svg
    └── og-image.jpg    # Image shown when the link is shared
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

4. Load the projects into the database:
   ```
   python seed.py
   ```

## Usage

```
python app.py
```

Open `http://127.0.0.1:8000/` in your browser.

### Environment variables

| Variable | What it does | Required |
|---|---|---|
| `PORTFOLIO_API_KEY` | Secret key for POST/PUT/DELETE. Without it, the API is read-only. | To edit projects |
| `FORMSPREE_ID` | Formspree form ID (the part after `/f/`). Defaults to mine; set it to an empty string to show email/LinkedIn buttons instead. | No |
| `FLASK_DEBUG` | Set to `1` to enable debug mode locally. Never in production. | No |
| `DATABASE_URL` | Database location. Defaults to `sqlite:///proyectos.db`. | No |

In PowerShell (only for the current window):
```
$env:PORTFOLIO_API_KEY = "a-long-random-secret"
python app.py
```

## API endpoints

| Method | Endpoint          | Description         | Key required |
|--------|-------------------|---------------------|:---:|
| GET    | `/proyectos`      | List all projects   | — |
| POST   | `/proyectos`      | Create a project    | ✓ |
| GET    | `/proyectos/<id>` | Get one project     | — |
| PUT    | `/proyectos/<id>` | Update a project    | ✓ |
| DELETE | `/proyectos/<id>` | Delete a project    | ✓ |

Example (PowerShell):
```
$headers = @{ "X-API-Key" = $env:PORTFOLIO_API_KEY }
$body = @{ titulo = "New project"; tecnologias = "Python, Flask"; emoji = "🚀" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/proyectos -Headers $headers -Body $body -ContentType "application/json"
```

Without the key, the API answers `401 Unauthorized`.

## Tests

```
python -m pytest
```

16 tests cover public reads, the API key protection (missing, wrong and correct key), validation, the read-only fallback, the contact section, the bilingual content and terminal, and fork badges. They use an in-memory database, so they never touch `proyectos.db`.

## More about me

Read the story behind the code in my logbook: [krma12.github.io/mi-bitacora](https://krma12.github.io/mi-bitacora/)

## Author

Hugo Maldonado ([@krma12](https://github.com/krma12)) — AI Engineering student building projects in Python, data, computer vision and cybersecurity.
