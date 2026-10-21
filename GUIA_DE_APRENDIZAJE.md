# Guía de aprendizaje — Portfolio con Flask

Este documento explica, paso a paso, todo lo que construimos en este proyecto y **por qué** hicimos cada cosa. La idea es que lo uses para repasar antes de una entrevista de trabajo — no solo para recordar qué comandos corriste, sino para poder explicar el razonamiento detrás de cada uno.

---

## 1. La estructura del proyecto

```
Servicios_Web/
├── app.py              # Arranca el servidor
├── routes.py           # Mapea URLs a la lógica que las maneja
├── resources.py        # La lógica real (qué hace cada ruta)
├── models.py           # Define las tablas de la base de datos
├── requirements.txt    # Lista de librerías que el proyecto necesita
├── .gitignore           # Qué archivos NO subir a GitHub
├── Templates/
│   └── landing_page.html
└── instance/
    └── proyectos.db     # La base de datos (no se sube a GitHub)
```

**¿Por qué separar en varios archivos en vez de poner todo en uno?** Esto se llama "separación de responsabilidades" (*separation of concerns*). Cada archivo tiene un trabajo específico. Si una entrevista te pregunta "¿por qué organizaste tu código así?", la respuesta es: facilita mantener, probar y entender el código — si algo falla en las rutas, sabes que el problema está en `resources.py`, no tienes que buscar en un archivo de 500 líneas.

---

## 2. Flask y Flask-RESTful

**Flask** es un *microframework* de Python para construir servidores web. "Micro" no significa que sea limitado — significa que viene con lo esencial (recibir peticiones HTTP, responder) y tú agregas el resto según lo necesites (base de datos, autenticación, etc.), a diferencia de frameworks más "todo incluido" como Django.

**Flask-RESTful** es una extensión que facilita construir **APIs REST** sobre Flask. En vez de escribir funciones sueltas con `@app.route`, defines **clases** (`Resource`) donde cada método HTTP (`get`, `post`, `put`, `delete`) es un método de la clase. Esto mapea naturalmente al estilo REST.

### ¿Qué es REST?

REST (*Representational State Transfer*) es un estilo de arquitectura para APIs donde:

- Cada "cosa" que manejas (un proyecto, un usuario, etc.) es un **recurso**, con su propia URL (ej. `/proyectos`, `/proyectos/1`).
- Usas los **métodos HTTP** para decir qué quieres hacer con ese recurso, en vez de tener URLs distintas para cada acción.

| Método   | Uso                          | Ejemplo en este proyecto              |
|----------|-------------------------------|----------------------------------------|
| `GET`    | Leer / obtener datos          | `GET /proyectos` → lista todos         |
| `POST`   | Crear algo nuevo               | `POST /proyectos` → crea un proyecto   |
| `PUT`    | Actualizar algo que ya existe  | `PUT /proyectos/1` → edita el proyecto 1 |
| `DELETE` | Borrar algo                    | `DELETE /proyectos/1` → borra el proyecto 1 |

Esto es una pregunta **muy común** en entrevistas: "¿qué es REST?" o "¿cuál es la diferencia entre PUT y POST?". La respuesta corta: `POST` crea algo nuevo (no sabes el ID todavía), `PUT` actualiza algo que ya existe (sí sabes el ID, porque va en la URL).

---

## 3. Entornos virtuales (venv)

Un **entorno virtual** es una copia aislada de Python con sus propias librerías instaladas, separada del Python "global" de tu computadora.

**¿Por qué se usa?** Sin un entorno virtual, todas las librerías que instalas con `pip install` se instalan globalmente, compartidas entre todos tus proyectos. Eso genera conflictos: un proyecto necesita la versión 1 de una librería, otro necesita la versión 2, y no pueden coexistir. Con un entorno virtual, cada proyecto tiene sus propias versiones, sin pisarse entre sí.

```
python -m venv mi_entorno          # crea el entorno
.\mi_entorno\Scripts\Activate.ps1  # lo activa (en Windows)
pip install -r requirements.txt    # instala las librerías DENTRO del entorno
```

**Nota importante que vivimos en este proyecto:** los entornos virtuales guardan **rutas absolutas** internamente (dónde está `python.exe` exactamente). Si mueves o copias la carpeta del entorno a otro lugar, se rompe — por eso tuvimos que borrar y recrear `mi_entorno` cuando lo copiamos desde otra carpeta. Esto es una buena anécdota para contar en una entrevista si preguntan sobre debugging: muestra que entiendes cómo funciona el sistema, no solo cómo copiar comandos.

**`requirements.txt`** es la lista de librerías que tu proyecto necesita (Flask, Flask-RESTful, Flask-SQLAlchemy). Sirve para que cualquier otra persona (o tú, en otra computadora) pueda recrear exactamente el mismo entorno con un solo comando: `pip install -r requirements.txt`. Es clave para que un proyecto sea "reproducible".

---

## 4. Bases de datos y ORM (SQLAlchemy)

**ORM** = *Object-Relational Mapper*. Es una herramienta que te permite trabajar con una base de datos usando objetos y clases de Python normales, **en vez de escribir SQL a mano**.

Sin ORM, para guardar un dato escribirías SQL directamente:
```sql
INSERT INTO proyecto (titulo, descripcion) VALUES ('Mi App', 'Descripción');
```

Con SQLAlchemy (el ORM que usamos), escribes Python puro:
```python
nuevo = Proyecto(titulo="Mi App", descripcion="Descripción")
db.session.add(nuevo)
db.session.commit()
```
Y SQLAlchemy genera el SQL por debajo, automáticamente.

### Cómo se ve un modelo

```python
class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(300))
```

- Heredar de `db.Model` le dice a SQLAlchemy "esta clase es una tabla".
- Cada `db.Column(...)` es una columna de esa tabla.
- `primary_key=True` en el `id` significa que SQLAlchemy genera ese número automáticamente (1, 2, 3...), no lo escribes tú.
- `nullable=False` significa que ese campo es obligatorio.

### `db.session.add()` + `db.session.commit()`

Esto sigue el mismo patrón que usar Git: primero "preparas" el cambio (`add`, como `git add`), y luego lo "confirmas" de verdad (`commit`, como `git commit`). Nada se guarda permanentemente en la base de datos hasta que haces `commit()`.

### `Proyecto.query.all()` / `Proyecto.query.get(id)`

Estas son formas de **consultar** datos:
- `.query.all()` = "tráeme todas las filas" (equivalente a `SELECT * FROM proyecto`).
- `.query.get(id)` = "tráeme la fila con este ID específico" (equivalente a `SELECT * FROM proyecto WHERE id = ...`).

### SQLite y la carpeta `instance/`

Usamos **SQLite**, una base de datos que vive en un solo archivo (`proyectos.db`) — no necesita un servidor de base de datos aparte, ideal para proyectos pequeños o de aprendizaje. Flask, por convención, guarda ese archivo dentro de una carpeta llamada `instance/`, que contiene datos específicos de tu máquina y normalmente **no se sube a GitHub** (por eso está en `.gitignore`).

---

## 5. `reqparse`: validar datos de entrada

Cuando alguien envía un `POST` o `PUT`, manda datos en el "cuerpo" (*body*) de la petición. `reqparse` (de Flask-RESTful) valida esos datos antes de que lleguen a tu código:

```python
parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, required=True, help='El título es obligatorio')
```

Si alguien intenta crear un proyecto sin `titulo`, `reqparse` responde automáticamente con un error — no tienes que escribir ese `if` a mano.

---

## 6. Jinja2: mezclar Python con HTML

Flask usa **Jinja2** para renderizar HTML con datos dinámicos. Es lo que usamos para que la sección de proyectos del portfolio muestre datos reales de la base de datos, en vez de HTML escrito a mano.

```html
{% for proyecto in proyectos %}
  <h3>{{ proyecto.titulo }}</h3>
{% else %}
  <p>No hay proyectos todavía.</p>
{% endfor %}
```

- `{{ ... }}` imprime un valor (como un `print()`, pero dentro del HTML).
- `{% for ... %} ... {% endfor %}` repite un bloque de HTML una vez por cada elemento de una lista.
- `{% else %}` dentro de un `for` es un detalle poco conocido: ese bloque se muestra **solo si la lista está vacía**.

En el backend, esto se conecta así:
```python
proyectos = Proyecto.query.all()
return render_template('landing_page.html', proyectos=proyectos)
```
`render_template` recibe variables de Python (`proyectos=proyectos`) y las hace disponibles dentro del archivo `.html`.

---

## 7. Git y GitHub

**Git** es un sistema de control de versiones: guarda el historial de cambios de tu código, permite volver atrás, y es la base para colaborar con otros. **GitHub** es una plataforma donde alojas repositorios de Git en la nube, y es prácticamente un requisito para cualquier puesto de programación — es tu "portafolio de código".

### El flujo básico que usamos

```
git init                          # convierte la carpeta en un repositorio de Git
git add .                         # marca los archivos para el próximo commit
git commit -m "mensaje"           # guarda ese conjunto de cambios en el historial
git branch -M main                # renombra la rama principal a "main"
git remote add origin <URL>       # conecta tu repo local con uno en GitHub
git push -u origin main           # sube tus commits a GitHub
```

**¿Por qué `add` y luego `commit`, en dos pasos?** `add` te deja elegir exactamente qué cambios quieres incluir en el próximo commit (puedes tener cambios en 5 archivos pero solo hacer commit de 2). `commit` es el que realmente guarda esa "foto" del proyecto en el historial, con un mensaje que explica qué cambió.

### `.gitignore`

Un archivo que le dice a Git qué **no** debe rastrear ni subir. En este proyecto ignoramos:
- `mi_entorno/` — el entorno virtual, porque es grande y se puede recrear con `requirements.txt`.
- `__pycache__/` — archivos generados automáticamente por Python, no son código fuente.
- `instance/` — la base de datos local, que contiene datos de prueba, no código.

Esto es una buena práctica que muchos entrevistadores buscan: saber qué **no** debe estar en un repositorio es tan importante como saber qué sí.

### `git config user.email` / `user.name`

Git necesita saber quién eres para asociar cada commit con un autor. Se configura una sola vez por computadora (`--global`).

---

## 8. Problemas que resolvimos (buenas historias para entrevistas)

Los entrevistadores a veces preguntan "cuéntame de un bug que resolviste" — aquí tienes varios ejemplos reales de este mismo proyecto:

1. **El entorno virtual roto:** al copiar `mi_entorno` de una carpeta a otra, `pip` dejó de funcionar porque el entorno guarda rutas absolutas internamente. Solución: recrearlo en el lugar correcto en vez de tratar de repararlo.

2. **`python` no reconocido en PowerShell:** el comando no estaba en el PATH del sistema, pero el lanzador `py` sí. Aprendimos a diagnosticar con `where.exe` para confirmar qué comandos existen y dónde.

3. **`curl` en PowerShell no es el curl real:** PowerShell tiene un alias `curl` que en realidad ejecuta `Invoke-WebRequest`, con una sintaxis distinta. Hubo que usar `curl.exe` explícitamente, o mejor, cambiar a `Invoke-RestMethod` (el comando nativo de PowerShell), que evita problemas de comillas anidadas.

4. **`instance/proyectos.db` "no aparecía":** en realidad sí se había creado, pero Flask lo puso en una subcarpeta `instance/` por convención — solo había que saber dónde buscar.

---

## 9. Preguntas típicas de entrevista relacionadas con este proyecto

- ¿Qué es una API REST y cómo la implementaste?
- ¿Cuál es la diferencia entre `GET`, `POST`, `PUT` y `DELETE`?
- ¿Qué es un ORM y por qué usarlo en vez de SQL directo?
- ¿Qué es un entorno virtual y por qué es importante?
- ¿Qué hace `.gitignore` y qué pondrías en él?
- ¿Cómo estructuras un proyecto Flask para que sea mantenible?
- ¿Qué es Jinja2 y cómo se conecta el backend con el HTML?
- Describe el flujo completo de un `POST`: desde que el cliente envía datos, hasta que quedan guardados en la base de datos.

---

## 10. Lo que sigue

Este proyecto es la base (etapa 1) de un roadmap más largo hacia AI engineering: después de esto, el siguiente escalón es aprender Python para datos (NumPy, Pandas), seguido de machine learning clásico (scikit-learn), servir modelos con una API (como ya sabes hacer aquí), deep learning, y finalmente LLMs/RAG. Cada etapa reutiliza lo que ya aprendiste — este CRUD, por ejemplo, es exactamente el mismo patrón que usarás para servir un modelo de IA más adelante.
