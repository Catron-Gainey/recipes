from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller
@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        # redirect to the appropriate route 
        return redirect('/add/recipe')
    Recipe.save_recipe({
        **request.form,
        'user_id': session['user_id']
    })
    return redirect('/dashboard')

@app.route('/add/recipe')
def add_recipe():
    user_id = session['user_id']
    return render_template('add_recipe.html', user_id=user_id)

@app.route('/view/one/recipe/<int:id>')
def view_one_recipe_with_user(id):
    user_id = session['user_id']
    recipe = Recipe.get_one_recipe_with_user(id)
    return render_template('view_one_recipe.html', recipe=recipe)

@app.route('/edit/<int:id>')
def edit(id):
    recipe = Recipe.get_one_recipe_with_user(id)
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/update/<int:id>',methods=['POST'])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        # redirect to the appropriate route.
        return redirect(f'/edit/{id}')
    recipe_dict = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions":request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30":request.form["under_30"],
        "id":id
        }
    Recipe.update_recipe(recipe_dict)
    return redirect("/dashboard")

@app.route('/delete/<int:id>')
def remove_recipe(id):
    Recipe.delete_recipe(id)
    return redirect("/dashboard")
