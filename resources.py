from flask_restful import Resource, reqparse
from flask import render_template, make_response
from models import db, Proyecto


class PrimerRecurso(Resource):
    def get(self):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        

class NombreAleatorio(Resource):
    def get(self):
        stock = 40
        vendidos = 30
        faltantes = 10 

        return {'Vendidos': vendidos, 'Faltantes': faltantes, 'Stock': stock}

class PaginaInicio(Resource):
     # Renderizamos la plantilla HTML y la guardamos en la variable html
    def get(self):
        # Traemos todos los proyectos guardados para pasárselos al HTML
        proyectos = Proyecto.query.all()
        # render_template puede recibir variables (aquí "proyectos") que
        # quedan disponibles dentro del archivo .html gracias a Jinja2
        sitio_web_renderizado = render_template('landing_page.html', proyectos=proyectos)
        # Creamos una respuesta HTTP con el contenido
        # del sitio web renderizado y la devolvemos al cliente
        return make_response(sitio_web_renderizado)


# reqparse valida los datos que llegan en el body de un POST/PUT,
# en vez de leerlos "a mano". Si falta 'titulo', responde solo con
# un error 400 automáticamente, sin que tengamos que revisarlo nosotros.
parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, required=True, help='El título es obligatorio')
parser.add_argument('descripcion', type=str)
parser.add_argument('resultado', type=str)
parser.add_argument('repo_url', type=str)


class ListaProyectos(Resource):
    """Maneja /proyectos -> la colección completa (listar y crear)."""

    def get(self):
        # Proyecto.query.all() -> SELECT * FROM proyecto, pero en Python puro
        proyectos = Proyecto.query.all()
        return [p.to_dict() for p in proyectos]

    def post(self):
        datos = parser.parse_args()

        nuevo = Proyecto(
            titulo=datos['titulo'],
            descripcion=datos['descripcion'],
            resultado=datos['resultado'],
            repo_url=datos['repo_url'],
        )

        db.session.add(nuevo)   # lo prepara para guardar
        db.session.commit()     # lo guarda de verdad en proyectos.db

        return nuevo.to_dict(), 201   # 201 = "Created"


class ProyectoIndividual(Resource):
    """Maneja /proyectos/<id> -> un proyecto específico (leer, actualizar, borrar)."""

    def get(self, id):
        proyecto = Proyecto.query.get(id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404
        return proyecto.to_dict()

    def put(self, id):
        proyecto = Proyecto.query.get(id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404

        datos = parser.parse_args()
        proyecto.titulo = datos['titulo']
        proyecto.descripcion = datos['descripcion']
        proyecto.resultado = datos['resultado']
        proyecto.repo_url = datos['repo_url']

        db.session.commit()
        return proyecto.to_dict()

    def delete(self, id):
        proyecto = Proyecto.query.get(id)
        if proyecto is None:
            return {'mensaje': 'Proyecto no encontrado'}, 404

        db.session.delete(proyecto)
        db.session.commit()
        return {'mensaje': 'Proyecto eliminado'}, 200
