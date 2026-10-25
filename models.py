# Aquí vive el objeto "db" que conecta Flask con SQLAlchemy.
# Lo separamos de app.py para que resources.py pueda importarlo
# sin crear un import circular.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Proyecto(db.Model):
    """
    Cada atributo db.Column(...) se convierte en una columna
    de la tabla 'proyecto' dentro de proyectos.db.
    """

    # primary_key=True -> SQLAlchemy genera el ID automáticamente (1, 2, 3...)
    id = db.Column(db.Integer, primary_key=True)

    # nullable=False -> este campo es obligatorio, no se puede guardar vacío
    titulo = db.Column(db.String(120), nullable=False)

    descripcion = db.Column(db.String(300))
    resultado = db.Column(db.String(200))      # ej. "Full CRUD working"
    # Versiones en español (la página tiene interruptor EN / ES)
    descripcion_es = db.Column(db.String(300))
    resultado_es = db.Column(db.String(200))
    repo_url = db.Column(db.String(300))       # link al repositorio en GitHub
    demo_url = db.Column(db.String(300))       # link a la versión en vivo (si existe)
    tecnologias = db.Column(db.String(200))    # separadas por coma: "Python, Flask, SQLite"
    emoji = db.Column(db.String(8))            # ícono de la tarjeta, ej. "🎮"
    orden = db.Column(db.Integer, default=0)   # para decidir qué proyecto sale primero

    @property
    def lista_tecnologias(self):
        """Convierte "Python, Flask" en ["Python", "Flask"] para mostrarlas como etiquetas."""
        if not self.tecnologias:
            return []
        return [t.strip() for t in self.tecnologias.split(',') if t.strip()]

    def to_dict(self):
        """Lo convierte a diccionario para poder devolverlo como JSON desde la API."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'resultado': self.resultado,
            'descripcion_es': self.descripcion_es,
            'resultado_es': self.resultado_es,
            'repo_url': self.repo_url,
            'demo_url': self.demo_url,
            'tecnologias': self.lista_tecnologias,
            'emoji': self.emoji,
            'orden': self.orden,
        }
