from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Recipe routes
ratings = Blueprint("ratings", __name__)

@ratings.route("/ratings", methods=["GET"])
def get_all_ratings():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT recipeID, userID, reason
        FROM Ratings
    '''
    cursor.execute(the_query)
    theDATA = cursor.fetchall()
    cursor.close()

    return jsonify(theDATA)

@ratings.route("/ratings/<recipeID>", methods=["GET"])
def get_ratings(recipeID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT recipeID, userID, reason
        FROM Ratings
        WHERE recipeID = %s
    '''
    cursor.execute(the_query, (recipeID,))
    theDATA = cursor.fetchone()
    cursor.close()

    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "Recipe not found"}), 404


@ratings.route("/ratings/<recipeID>", methods=["PUT"])
def update_ratings(recipeID):
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


@ratings.route("/ratings/<userID>", methods=["GET"])
def get_user_ratings(userID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT recipeID, userID, reason
        FROM Ratings
        WHERE userID = %s
    '''
    cursor.execute(the_query, (userID,))
    theDATA = cursor.fetchall()
    cursor.close()

    return jsonify(theDATA)