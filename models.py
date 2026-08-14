# Aquí vive el objeto "db" que conecta Flask con SQLAlchemy.
# Lo separamos de app.py para que resources.py (donde irán los
# modelos y el CRUD) pueda importarlo sin crear un import circular.

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
    resultado = db.Column(db.String(200))   # ej. "92% accuracy"
    repo_url = db.Column(db.String(300))

    def to_dict(self):
        """Igual que en tu clase Proyecto anterior: lo convierte a
        diccionario para poder devolverlo como JSON desde la API."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'resultado': self.resultado,
            'repo_url': self.repo_url,
        }
