from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Recipe:
    db = "users_and_recipes" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.user_id = data['user_id']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?


    @classmethod
    def save_recipe(cls, data):
        query = """INSERT INTO recipes (name, under_30, description, instructions, user_id, date_made)
                VALUES (%(name)s, %(under_30)s, %(description)s, %(instructions)s, %(user_id)s, %(date_made)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_and_recipes').query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    

    @classmethod
    def get_all_recipes_with_user(cls):
        # Get all tweets, and their one associated User that created it
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL('users_and_recipes').query_db(query)
        all_recipes = []
        for row in results:
            # Create a Tweet class instance from the information from each db row
            one_recipe = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_recipes_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = user.User(one_recipes_author_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_recipe.user = author
            # Append the Tweet containing the associated User to your list of tweets
            all_recipes.append(one_recipe)
        return all_recipes
    
    @classmethod
    def get_one_recipe_with_user(cls, id):
        # Get all tweets, and their one associated User that created it
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('users_and_recipes').query_db(query, {"id":id})
        all_recipes = []
        for row in results:
            # Create a Tweet class instance from the information from each db row
            one_recipe = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_recipes_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = user.User(one_recipes_author_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_recipe.user = author
            # Append the Tweet containing the associated User to your list of tweets
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def update_recipe(cls,user_data):
        query = """UPDATE recipes 
                SET name=%(name)s, under_30=%(under_30)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s
                WHERE id = %(id)s
                ;"""
        return connectToMySQL(cls.db).query_db(query,user_data)
    
    @classmethod
    def delete_recipe(cls, id):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, {"id":id})
        return result
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True # we assume this is true
        if len(data['name']) < 3:
            flash("Name can't be less than 3 characters.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description can't be less than 3 characters.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions can't be less than 3 characters.")
            is_valid = False
        if 'under_30' not in data:
            flash("under 30 field cant be blank.")
            is_valid = False
        if len(data['date_made']) < 1:
            flash("date made cant be blank")
            is_valid = False
        return is_valid