from flask_app import app
from flask import redirect, render_template, request
from ..models.autores import Autor
from ..models.libros import Libro

@app.route('/libros')
def libros():
    todos_libros = Libro.mostrar_libros()
    return render_template('libros.html', libros = todos_libros)

@app.route('/guardar/libro', methods=['POST'])
def guardar_libro():
    data = {
        "titulo": request.form['titulo'],
        "num_paginas": request.form['num_paginas']
    }
    
    nuevo_libro = Libro.guardar_libro(data)
    return redirect('/libros')

@app.route('/libro/<int:id>')
def mostrar_libro(id):
    data = {
        "id": id
    }
    libro = Libro.mostrar_libro(data)
    autor_no_favorito = Autor.autores_no_favoritos(data)
    return render_template('mostrar_libro.html', libro = libro, autor_no_favorito = autor_no_favorito)

