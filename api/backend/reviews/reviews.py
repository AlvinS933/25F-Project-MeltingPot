from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Recipe routes
recipes = Blueprint("reviews", __name__)

@reviews.route("/reviews", methods=["GET"])
def get_all_reviews():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT recipeID, userID, review
        FROM Reviews
    '''
    cursor.execute(the_query)
    theDATA = cursor.fetchall()
    cursor.close()

    return jsonify(theDATA)

@reviews.route("/reviews/<recipeID>", methods=["PUT"])
def update_reviews(recipeID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        the_query = '''
            UPDATE Reviews
            SET name = %s, description = %s, steps = %s, picture = %s, 
                difficulty = %s, catID = %s
            WHERE recipeID = %s
        '''
        cursor.execute(the_query, (
            data.get('name'),
            data.get('description'),
            data.get('steps'),
            data.get('picture'),
            data.get('difficulty'),
            data.get('catID'),
            recipeID
        ))
        db.get_db().commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Recipe not found"}), 404

        return jsonify({"message": "Recipe updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@reviews.route("/reviews/<recipeID>", methods=["GET"])
def get_reviews(recipeID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT recipeID, userID, review
        FROM Reviews
        WHERE recipeID = %s
    '''
    cursor.execute(the_query, (recipeID,))
    theDATA = cursor.fetchone()
    cursor.close()

    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "Recipe not found"}), 404


@reviews.route("/reviews/<recipeID>", methods=["PUT"])
def update_reviews(recipeID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        the_query = '''
            UPDATE Recipes
            SET name = %s, description = %s, steps = %s, picture = %s, 
                difficulty = %s, catID = %s
            WHERE recipeID = %s
        '''
        cursor.execute(the_query, (
            data.get('name'),
            data.get('description'),
            data.get('steps'),
            data.get('picture'),
            data.get('difficulty'),
            data.get('catID'),
            recipeID
        ))
        db.get_db().commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Recipe not found"}), 404

        return jsonify({"message": "Recipe updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@reviews.route("/reviews/recipe/<recipeID>", methods=["GET"])
def get_reviews(recipeID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT recipeID, userID, review
        FROM Reviews
        WHERE recipeID = %s
    '''
    cursor.execute(the_query, (recipeID,))
    theDATA = cursor.fetchone()
    cursor.close()

    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "Recipe not found"}), 404