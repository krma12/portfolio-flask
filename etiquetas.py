"""
Cómo se escriben bonito las etiquetas de tecnologías.

GitHub guarda los topics en minúsculas y con guiones ("ai-agents", "gemini-api"),
y al convertirlos quedaban cosas como "Ai Agents" o "Llm". Aquí se arreglan las
siglas y algunos nombres propios. Lo usan models.py (al mostrar) y sync_github.py
(al guardar), así que arregla tanto lo nuevo como lo que ya estaba guardado.
"""

# Palabras que siempre van en mayúsculas
SIGLAS = {
    "ai", "ia", "api", "apis", "llm", "llms", "cve", "smb", "rdp", "eda", "oop", "poo",
    "crud", "sql", "rest", "json", "html", "css", "edr", "siem", "nlp", "ml", "cli",
    "ui", "ux", "gpu", "cpu", "csv", "ocr", "os", "aws", "gcp", "jwt", "http", "https",
}

# Nombres con una forma especial
ESPECIALES = {
    "python": "Python", "flask": "Flask", "sqlite": "SQLite", "sqlalchemy": "SQLAlchemy",
    "opencv": "OpenCV", "mediapipe": "Mediapipe", "numpy": "NumPy", "pandas": "Pandas",
    "jupyter": "Jupyter", "pygame": "Pygame", "javascript": "JavaScript", "typescript": "TypeScript",
    "pytest": "pytest", "github": "GitHub", "github-actions": "GitHub Actions", "leaflet": "Leaflet",
    "kali-linux": "Kali Linux", "scikit-learn": "scikit-learn", "openai": "OpenAI",
    "eternalblue": "EternalBlue", "bluekeep": "BlueKeep", "smbghost": "SMBGhost",
    "doublepulsar": "DoublePulsar", "powershell": "PowerShell", "fastapi": "FastAPI",
    "rest-api": "REST API", "chatgpt": "ChatGPT", "ollama": "Ollama", "groq": "Groq",
    "telegram": "Telegram", "jupyter-notebook": "Jupyter",
}


def etiqueta_bonita(texto):
    """'ai-agents' o 'Ai Agents' -> 'AI Agents' ; 'Llm' -> 'LLM' ; 'Pytest' -> 'pytest'"""
    texto = (texto or "").strip()
    if not texto:
        return ""
    clave = texto.lower().replace(" ", "-")
    if clave in ESPECIALES:
        return ESPECIALES[clave]
    palabras = texto.replace("-", " ").replace("_", " ").split()
    salida = []
    for p in palabras:
        b = p.lower()
        if b in SIGLAS:
            salida.append(b.upper())
        elif b in ESPECIALES:
            salida.append(ESPECIALES[b])
        elif p.isupper() or any(c.isupper() for c in p[1:]):
            salida.append(p)            # ya venía con su forma (ej. "SQLite")
        else:
            salida.append(p.capitalize())
    return " ".join(salida)
