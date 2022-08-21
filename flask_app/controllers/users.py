from flask_app import app
from flask import render_template, request, session, flash, redirect
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')

    password = bcrypt.generate_password_hash(request.form['password']) 

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": password
    }
    id = User.save(formulario) 
    session['id'] = id 
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user: 
        flash("e-mail no encontrado", 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", 'login')
        return redirect('/')
    
    session['id'] = user.id

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')

    formulario = {
        "id": session['id']
    }

    user = User.get_by_id(formulario)

    recipes = Recipe.get_all() 

    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')