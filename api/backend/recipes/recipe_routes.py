from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Recipe routes
recipes = Blueprint("recipes", __name__)

@recipes.route("/recipes", methods=["GET"])
def get_all_recipes():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT userID, catID, name, description, steps, picture, difficulty, recipeID
        FROM Recipes
    '''
    cursor.execute(the_query)
    theDATA = cursor.fetchall()
    cursor.close()

    return jsonify(theDATA)

@recipes.route("/recipes/<recipeID>", methods=["GET"])
def get_recipe(recipeID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT userID, catID, name, description, steps, picture, difficulty, recipeID
        FROM Recipes
        WHERE recipeID = %s
    '''
    cursor.execute(the_query, (recipeID,))
    theDATA = cursor.fetchone()
    cursor.close()

    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "Recipe not found"}), 404

