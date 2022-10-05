from flask_app import app
from flask_app.controllers import autores_controller, libros_controller

if __name__ == "__main__":
    app.run(debug=True)