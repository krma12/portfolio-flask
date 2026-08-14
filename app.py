import random
#Nos  permite convertir nuestra PC en servidor
from flask import Flask
# Nos permite crear una API RESTful de manera sencilla
from flask_restful import Api
# db es el objeto que conecta Flask con la base de datos (definido en models.py)
from models import db
#Importamos rutas para poder inicializar las rutas de la API
from routes import Administrador_de_rutas

# Creamos un servidor y lo guardamos en la variable app
app = Flask(__name__)

# Le decimos a Flask dónde vivirá la base de datos.
# sqlite:///proyectos.db crea un archivo proyectos.db en esta misma carpeta.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyectos.db'
# Apagamos una función de tracking que no usamos y solo consume memoria.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conectamos el objeto db (de models.py) con esta app específica.
db.init_app(app)

# Creamos el motor que hace funcionar nuestra API y lo guardamos en la variable api
api = Api(app)

#Objeto que controle todas mis rutas.
rutas = Administrador_de_rutas()
rutas.inicializar_rutas(api)

if __name__ == "__main__":
    # app_context() le avisa a SQLAlchemy "estamos dentro de la app",
    # necesario para poder tocar la base de datos fuera de una petición HTTP.
    with app.app_context():
        db.create_all()  # Crea las tablas que falten, según los modelos definidos.

    # Solicitamos al servidor que se ejecute en modo debug y en el puerto 8000
    app.run(debug=True, port=8000)
