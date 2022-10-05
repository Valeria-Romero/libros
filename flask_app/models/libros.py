from ..config.mysqlconnection import connectToMySQL
from flask_app.models import autores

class Libro:
    def __init__(self, data):
        self.id= data['id']
        self.titulo = data['titulo']
        self.num_paginas = data['num_paginas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Lista de autores que guardarono como favorito el libro
        self.favorito_de_autores = []
        
        
    @classmethod
    def mostrar_libros(cls):
        query = "SELECT * FROM libros;"
        results = connectToMySQL('libros').query_db(query)
        libros = []
        for fila in results:
            libros.append(cls(fila))
        return libros
    
    @classmethod
    def guardar_libro(cls, data):
        query = "INSERT INTO libros (titulo, num_paginas) VALUES (%(titulo)s, %(num_paginas)s);"
        results = connectToMySQL('libros').query_db(query, data)
        return results
    

    @classmethod
    def mostrar_libro(cls, data):
        query = "SELECT * FROM libros LEFT JOIN favoritos ON libros.id = favoritos.libro_id LEFT JOIN autores ON autores.id = favoritos.autor_id WHERE libros.id = %(id)s;"
        results = connectToMySQL('libros').query_db(query, data)
        
        libro = cls(results[0])
        
        for fila in results:
            if fila['autores.id'] == None:
                break
            
            data = {
                "id": fila['autores.id'],
                "nombre": fila['nombre'],
                "created_at": fila['autores.created_at'],
                "updated_at": fila['autores.updated_at']
            }
            libro.favorito_de_autores.append(autores.Autor(data))
        return libro
    
    @classmethod
    def libros_no_favoritos(cls, data):
        query = "SELECT * FROM libros WHERE libros.id NOT IN (SELECT libro_id FROM favoritos WHERE autor_id = %(id)s);"
        results = connectToMySQL('libros').query_db(query, data)
        libros = []
        for fila in results:
            libros.append(cls(fila))
        return libros