from flask_app import app
from flask import redirect, render_template, request
from ..models.autores import Autor
from flask_app.models.libros import Libro

@app.route('/')
def index():
    return redirect('/autores')

@app.route('/autores')
def autores():
    autores = Autor.mostrar_autores()
    return render_template('autores.html', autores = autores)

@app.route('/guardar/autor', methods= ['POST'])
def guardar_autor():
    data = {
        "nombre": request.form['nombre']
    }
    nuevo_autor = Autor.guardar_autor(data)
    return redirect('/autores')

@app.route('/autor/<int:id>')
def mostrar_autor(id):
    data={
        "id": id
    }
    autor = Autor.mostrar_autor(data)
    libros_no_favoritos = Libro.libros_no_favoritos(data)
    return render_template('mostrar_autor.html', autor = autor, libros_no_favoritos = libros_no_favoritos)

@app.route('/guardar/favoritos', methods= ['POST'])
def guardar_libro_favorito():
    data = {
        'autor_id': request.form['autor_id'],
        'libro_id': request.form['libro_id']
    }
    
    Autor.nuevo_favorito(data)
    return redirect(f"/autor/{request.form['autor_id']}")