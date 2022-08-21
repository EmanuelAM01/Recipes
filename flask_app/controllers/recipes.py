from flask import render_template, redirect, session, request, flash 
from flask_app import app


from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/new/recipe')
def new_recipe():
    if 'id' not in session: 
        return redirect('/')

    formulario = {
        "id": session['id']
    }

    user = User.get_by_id(formulario)
    
    return render_template('new_recipe.html', user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'id' not in session: 
        return redirect('/')

    if not Recipe.valida_receta(request.form): 
        return redirect('/new/recipe')

    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>') 
def edit_recipe(id):
    if 'id' not in session: 
        return redirect('/')
    
    formulario = {
        "id": session['id']
    }

    user = User.get_by_id(formulario) 

    formulario_receta = { "id": id }
    
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'id' not in session:
        return redirect('/')
    
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id'])

    Recipe.update(request.form)

    return redirect('/dashboard')

@app.route('/show/recipe/<int:id>') 
def show_recipe(id):
    if 'id' not in session: 
        return redirect('/')

    formulario = {
        "id": session['id']
    }

    user = User.get_by_id(formulario) 


    formulario_receta = { "id": id }

    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user=user, recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'id' not in session: 
        return redirect('/')
    
    formulario = {"id": id}
    Recipe.delete(formulario)

    return redirect('/dashboard')