import hmac
from functools import wraps

from flask import current_app, make_response, render_template, request
from flask_restful import Resource, inputs, reqparse

from models import Proyecto, db
import logging

from seguridad import esta_bloqueado, ip_cliente, link_https, registrar_evento, registrar_fallo, texto


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
            registrar_evento('escritura_sin_clave_configurada', logging.WARNING, ip=ip_cliente(), ruta=request.path)
            return {'mensaje': 'La API está en modo solo lectura'}, 403

        # Si esta IP falló la clave demasiadas veces, la frenamos un rato
        ip = ip_cliente()
        espera = esta_bloqueado(ip)
        if espera:
            registrar_evento('peticion_bloqueada', logging.WARNING, ip=ip, metodo=request.method, ruta=request.path)
            return {'mensaje': 'Demasiados intentos. Intenta más tarde.'}, 429, {'Retry-After': str(espera)}

        clave_recibida = request.headers.get('X-API-Key', '')

        # compare_digest compara en tiempo constante: no revela, por lo que
        # tarda en responder, cuántos caracteres de la clave acertaste.
        if not hmac.compare_digest(clave_recibida.encode(), clave_correcta.encode()):
            registrar_evento('clave_invalida', logging.WARNING, ip=ip, metodo=request.method, ruta=request.path)
            registrar_fallo(ip)
            return {'mensaje': 'Clave inválida o faltante'}, 401

        return metodo(*args, **kwargs)
    return envoltura


class PaginaInicio(Resource):
    def get(self):
        # Traemos los proyectos ordenados para pasárselos al HTML
        proyectos = Proyecto.query.order_by(Proyecto.orden, Proyecto.id).all()

        # Tecnologías distintas usadas en todos los proyectos (para las estadísticas)
        tecnologias = {t for p in proyectos for t in p.etiquetas}

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
# Cada campo tiene un largo máximo, y los links solo pueden ser https://
# (así nadie puede guardar un link "javascript:..." que se ejecute al darle clic).
parser.add_argument('titulo', type=texto(120), required=True, help='El título es obligatorio (máx. 120 caracteres)')
parser.add_argument('descripcion', type=texto(500))
parser.add_argument('resultado', type=texto(200))
parser.add_argument('descripcion_es', type=texto(500))
parser.add_argument('resultado_es', type=texto(200))
parser.add_argument('repo_url', type=link_https)
parser.add_argument('demo_url', type=link_https)
parser.add_argument('tecnologias', type=texto(600))   # "Python, Flask, SQLite"
parser.add_argument('emoji', type=texto(16))
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

        registrar_evento('proyecto_creado', id=nuevo.id, ip=ip_cliente())
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
        registrar_evento('proyecto_editado', id=id, ip=ip_cliente())
        return proyecto.to_dict()

    @requiere_clave
    def delete(self, id):
        proyecto = db.session.get(Proyecto, id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404

        db.session.delete(proyecto)
        db.session.commit()
        registrar_evento('proyecto_eliminado', logging.WARNING, id=id, ip=ip_cliente())
        return {'mensaje': 'Proyecto eliminado'}, 200
