from ..config.mysqlconnection import connectToMySQL
from flask_app.models import libros

class Autor:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.libros_favoritos = []
    
    @classmethod
    def mostrar_autores(cls):
        query = "SELECT * FROM autores;"
        results = connectToMySQL('libros').query_db(query)
        autores = []
        for fila in results:
            autores.append(cls(fila))
        return autores
    
    @classmethod
    def guardar_autor(cls, data):
        query= "INSERT INTO autores (nombre) VALUES (%(nombre)s);"
        results = connectToMySQL('libros').query_db(query, data)
        return results
    
    @classmethod
    def mostrar_autor(cls, data):
        query = "SELECT * FROM autores LEFT JOIN favoritos ON autores.id = favoritos.autor_id LEFT JOIN libros ON libros.id = favoritos.libro_id WHERE autores.id = %(id)s"
        
        results = connectToMySQL('libros').query_db(query, data)
        
        autor = cls(results[0])
        
        for fila in results:
            if fila['libros.id'] == None:
                break
            data = {
                "id": fila['libros.id'],
                "titulo": fila['titulo'],
                "num_paginas": fila['num_paginas'],
                "created_at": fila['libros.created_at'],
                "updated_at": fila['libros.updated_at']
            }
            
            autor.libros_favoritos.append(libros.Libro(data))
        
        return autor
    
    @classmethod
    def autores_no_favoritos(cls, data):
        query = "SELECT * FROM autores WHERE autores.id NOT IN (SELECT autor_id FROM favoritos WHERE libro_id = %(id)s);"
        results = connectToMySQL('libros').query_db(query, data)
        autores = []
        for fila in results:
            autores.append(cls(fila))
        return autores
    
    @classmethod
    def nuevo_favorito(cls, data):
        query = "INSERT INTO favoritos (autor_id, libro_id) VALUES (%(autor_id)s, %(libro_id)s);"
        results = connectToMySQL('libros').query_db(query, data)
        return results
        