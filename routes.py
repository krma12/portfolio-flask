# Regla de oro: toda ruta que vayamos a crear debe estar en el archivo routes.py,
# no en app.py
from resources import ListaProyectos, PaginaInicio, ProyectoIndividual


class Administrador_de_rutas:
    # Este método le da funcionalidad a la clase Administrador_de_rutas,
    # permitiendo inicializar las rutas de la API
    def inicializar_rutas(self, aplicacion):
        # / -> Ruta raíz: la página del portfolio
        aplicacion.add_resource(PaginaInicio, '/')

        # CRUD de proyectos:
        # /proyectos          -> listar todos (GET) y crear uno nuevo (POST)
        # /proyectos/<id>     -> leer (GET), actualizar (PUT) o borrar (DELETE) uno específico
        # POST, PUT y DELETE piden la clave en el header X-API-Key (ver resources.py)
        aplicacion.add_resource(ListaProyectos, '/proyectos')
        aplicacion.add_resource(ProyectoIndividual, '/proyectos/<int:id>')
