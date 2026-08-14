# regla de oro: toda ruta que vayamos a crear debe estar en el archivo routes.py, 
# no en app.py
from resources import *
class Administrador_de_rutas:
#Este metodo le dara funcionalidad a la clase Administrador_de_rutas, 
# permitiendo inicializar las rutas de la API
    def inicializar_rutas(self, aplicacion):
        aplicacion.add_resource(PrimerRecurso, '/primero')
        aplicacion.add_resource(NombreAleatorio, '/segundo')
        # / -> Ruta raiz, es decir, la primera ruta que se ejecuta cuando se ingresa a la API
        aplicacion.add_resource(PaginaInicio, '/')

        # CRUD de proyectos:
        # /proyectos          -> listar todos (GET) y crear uno nuevo (POST)
        # /proyectos/<id>     -> leer (GET), actualizar (PUT) o borrar (DELETE) uno específico
        aplicacion.add_resource(ListaProyectos, '/proyectos')
        aplicacion.add_resource(ProyectoIndividual, '/proyectos/<int:id>')
        

