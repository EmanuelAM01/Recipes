from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, session

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX=re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('recetas').query_db(query, formulario) 
        return result 

    @staticmethod
    def valida_usuario(formulario):
        es_valido = True
        
        if len(formulario['first_name']) < 3:
            flash('Nombre debe de tener al menos 3 caracteres', 'register')
            es_valido = False
        
        if len(formulario['last_name']) < 3:
            flash('Apellido debe de tener al menos 3 caracteres', 'register')
            es_valido = False
        
        if not EMAIL_REGEX.match(formulario['email']): 
            flash('Email invalido', 'register')
            es_valido = False

        if not PWD_REGEX.match(formulario['password']):
            flash('Contraseña debe tener al menos 8 caracteres, un caracter especial, un número, una mayúscula y una minúscula', 'register')
            es_valido = False

        
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coiniciden', 'register')
            es_valido = False
        
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recetas').query_db(query, formulario)
        if len(results) >= 1:
            flash('e-mail registrado previamente', 'register')
            es_valido = False

        return es_valido

    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        if len(result) < 1:
            return False
        else:
            user = cls(result[0]) 
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario) #Select recibe lista
        user = cls(result[0])
        return user