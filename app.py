import os

# Nos permite convertir nuestra PC en servidor
from flask import Flask
# Nos permite crear una API RESTful de manera sencilla
from flask_restful import Api
# db es el objeto que conecta Flask con la base de datos (definido en models.py)
from models import db
# Importamos rutas para poder inicializar las rutas de la API
from routes import Administrador_de_rutas

# Creamos un servidor y lo guardamos en la variable app.
# Flask busca las plantillas en la carpeta "templates" (en minúscula):
# en Windows da igual, pero en un servidor Linux "Templates" no la encuentra.
app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuración
# Los datos sensibles o que cambian entre tu PC y el servidor NO van escritos
# en el código: se leen de "variables de entorno". Así la clave de la API
# nunca termina subida a GitHub.
# ---------------------------------------------------------------------------

# Dónde vive la base de datos. Por defecto: instance/proyectos.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///proyectos.db')
# Apagamos una función de tracking que no usamos y solo consume memoria.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave que protege crear/editar/borrar proyectos (ver resources.py).
# Si no está definida, la API queda en "solo lectura": es más seguro fallar
# cerrado que dejar la API abierta por olvido.
app.config['API_KEY'] = os.environ.get('PORTFOLIO_API_KEY')

# ID del formulario de Formspree (https://formspree.io). No es secreto: de todas
# formas aparece en el HTML de la página. Si lo dejas vacío (FORMSPREE_ID=""),
# la página muestra botones de correo y LinkedIn en lugar del formulario.
app.config['FORMSPREE_ID'] = os.environ.get('FORMSPREE_ID', 'mkjjjwkd')

# Conectamos el objeto db (de models.py) con esta app específica.
db.init_app(app)

# Creamos las tablas que falten al arrancar. Va aquí (y no solo dentro de
# __main__) porque en un servidor como PythonAnywhere la app se importa,
# no se ejecuta con "python app.py".
with app.app_context():
    db.create_all()

# Creamos el motor que hace funcionar nuestra API y lo guardamos en la variable api
api = Api(app)

# Objeto que controla todas mis rutas.
rutas = Administrador_de_rutas()
rutas.inicializar_rutas(api)

if __name__ == "__main__":
    # El modo debug muestra errores detallados y una consola interactiva en el
    # navegador. Es útil en tu PC, pero en internet permitiría ejecutar código
    # en el servidor, así que solo se activa si tú lo pides: FLASK_DEBUG=1
    modo_debug = os.environ.get('FLASK_DEBUG') == '1'
    app.run(debug=modo_debug, port=8000)
