from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
import re 
bcrypt = Bcrypt(app)
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller
@app.route('/create', methods=['POST'])
def create_person():
    if not User.validate_user(request.form):
        # redirect to the appropriate route.
        return redirect('/')
    # else no errors:
    email_data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email_data)
    # user is not registered in the db
    if user_in_db:
        flash("That email is already being used")
        return redirect("/")
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    User.save(data)
    print(f"********{request.form}***************")
    email_data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email_data)
    session['user_id'] = user_in_db.id
    # store user id into session
    session.update(request.form)
    print(session)
    return redirect("/dashboard")


# Read Users Controller
@app.route('/')
@app.route('/reg/log')
def index():
    return render_template('reg_log.html')

@app.route('/dashboard')
def show_dashboard():
    if not session:
        return redirect('/')
    session_user_id = session['user_id']  
    return render_template("dashboard.html", recipes = Recipe.get_all_recipes_with_user(), session_user_id=session_user_id)

@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/log/out')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dojo/<int:dojo_id>')
def show_user_with_recipes(user_id):
    session['user_id'] = user_id
    user = User.get_user_with_recipes(user_id)
    return render_template("show_one_dojo.html", user = user)


# Update Users Controller



# Delete Users Controller