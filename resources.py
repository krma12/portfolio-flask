import hmac
from functools import wraps

from flask import current_app, make_response, render_template, request
from flask_restful import Resource, inputs, reqparse

from models import Proyecto, db


# ---------------------------------------------------------------------------
# Seguridad: solo quien tenga la clave puede crear, editar o borrar.
# Leer (GET) sigue siendo público, porque el portfolio es para mostrarse.
# ---------------------------------------------------------------------------
def requiere_clave(metodo):
    """
    Decorador: envuelve un método (post, put, delete) y, antes de ejecutarlo,
    revisa que la petición traiga el header  X-API-Key  con la clave correcta.
    """
    @wraps(metodo)
    def envoltura(*args, **kwargs):
        clave_correcta = current_app.config.get('API_KEY')

        # Si el servidor no tiene clave configurada, nadie puede escribir.
        # (Fallar "cerrado" es más seguro que dejar la API abierta por olvido.)
        if not clave_correcta:
            return {'mensaje': 'La API está en modo solo lectura'}, 403

        clave_recibida = request.headers.get('X-API-Key', '')

        # compare_digest compara en tiempo constante: no revela, por lo que
        # tarda en responder, cuántos caracteres de la clave acertaste.
        if not hmac.compare_digest(clave_recibida.encode(), clave_correcta.encode()):
            return {'mensaje': 'Clave inválida o faltante'}, 401

        return metodo(*args, **kwargs)
    return envoltura


class PaginaInicio(Resource):
    def get(self):
        # Traemos los proyectos ordenados para pasárselos al HTML
        proyectos = Proyecto.query.order_by(Proyecto.orden, Proyecto.id).all()

        # Tecnologías distintas usadas en todos los proyectos (para las estadísticas)
        tecnologias = {t for p in proyectos for t in p.lista_tecnologias}

        # render_template puede recibir variables que quedan disponibles
        # dentro del archivo .html gracias a Jinja2
        sitio_web_renderizado = render_template(
            'landing_page.html',
            proyectos=proyectos,
            total_tecnologias=len(tecnologias),
            formspree_id=current_app.config.get('FORMSPREE_ID'),
        )
        return make_response(sitio_web_renderizado)


# reqparse valida los datos que llegan en el body de un POST/PUT.
# Si falta 'titulo', responde solo con un error 400 automáticamente.
parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, required=True, help='El título es obligatorio')
parser.add_argument('descripcion', type=str)
parser.add_argument('resultado', type=str)
parser.add_argument('descripcion_es', type=str)
parser.add_argument('resultado_es', type=str)
parser.add_argument('repo_url', type=str)
parser.add_argument('demo_url', type=str)
parser.add_argument('tecnologias', type=str)   # "Python, Flask, SQLite"
parser.add_argument('emoji', type=str)
parser.add_argument('orden', type=int, default=0)
parser.add_argument('es_fork', type=inputs.boolean, default=False)   # acepta true/false

CAMPOS = ['titulo', 'descripcion', 'resultado', 'descripcion_es', 'resultado_es', 'repo_url', 'demo_url', 'tecnologias', 'emoji', 'orden', 'es_fork']


class ListaProyectos(Resource):
    """Maneja /proyectos -> la colección completa (listar y crear)."""

    def get(self):
        proyectos = Proyecto.query.order_by(Proyecto.orden, Proyecto.id).all()
        return [p.to_dict() for p in proyectos]

    @requiere_clave
    def post(self):
        datos = parser.parse_args()
        nuevo = Proyecto(**{campo: datos[campo] for campo in CAMPOS})

        db.session.add(nuevo)   # lo prepara para guardar
        db.session.commit()     # lo guarda de verdad en proyectos.db

        return nuevo.to_dict(), 201   # 201 = "Created"


class ProyectoIndividual(Resource):
    """Maneja /proyectos/<id> -> un proyecto específico (leer, actualizar, borrar)."""

    def get(self, id):
        # db.session.get() es la forma actual de SQLAlchemy 2
        # (Proyecto.query.get() quedó marcado como obsoleto)
        proyecto = db.session.get(Proyecto, id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404
        return proyecto.to_dict()

    @requiere_clave
    def put(self, id):
        proyecto = db.session.get(Proyecto, id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404

        datos = parser.parse_args()
        for campo in CAMPOS:
            setattr(proyecto, campo, datos[campo])

        db.session.commit()
        return proyecto.to_dict()

    @requiere_clave
    def delete(self, id):
        proyecto = db.session.get(Proyecto, id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404

        db.session.delete(proyecto)
        db.session.commit()
        return {'mensaje': 'Proyecto eliminado'}, 200
