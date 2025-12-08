from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

collections = Blueprint("collections", __name__)

@collections.route("/collections/<userID>", methods=["GET"])
def get_user_collections(userID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT collectID, userID, title, description
        FROM Collections
        WHERE userID = %s
    '''
    cursor.execute(the_query, (userID))
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@collections.route("/collections/<userID>/create", methods=["POST"])
def create_collection(userID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO Collections (userID, name, description)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(the_query, (
            userID,
            data.get('name'),
            data.get('description')
        ))
        db.get_db().commit()
        
        new_collect_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Collection created successfully", "collectID": new_collect_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

@collections.route("/collections/<collectID>", methods=["GET"])
def get_collection(collectID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT collectID, userID, name, description, createdAt
        FROM Collections
        WHERE collectID = %s
    '''
    cursor.execute(the_query, (collectID,))
    theDATA = cursor.fetchone()
    cursor.close()
    
    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "Collection not found"}), 404

@collections.route("/collections/<collectID>", methods=["PUT"])
def update_collection(collectID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            UPDATE Collections
            SET name = %s, description = %s
            WHERE collectID = %s
        '''
        cursor.execute(the_query, (
            data.get('name'),
            data.get('description'),
            collectID
        ))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Collection not found"}), 404
            
        return jsonify({"message": "Collection updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@collections.route("/collections/<collectID>", methods=["DELETE"])
def delete_collection(collectID):
    try:
        cursor = db.get_db().cursor()
        the_query = '''
            DELETE FROM Collections
            WHERE collectID = %s
        '''
        cursor.execute(the_query, (collectID,))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Collection not found"}), 404
            
        return jsonify({"message": "Collection deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@collections.route("/collections/<collectID>/recipes", methods=["GET"])
def get_collection_recipes(collectID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT r.recipeID, r.name, r.description, r.difficulty
        FROM CollectionRecipes cr
        JOIN Recipes r ON cr.recipeID = r.recipeID
        WHERE cr.collectID = %s
    '''
    cursor.execute(the_query, (collectID,))
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@collections.route("/collections/<collectID>/recipes", methods=["POST"])
def add_recipe_to_collection(collectID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO CollectionRecipes (collectID, recipeID)
            VALUES (%s, %s)
        '''
        cursor.execute(the_query, (
            collectID,
            data.get('recipeID')
        ))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Recipe added to collection successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

@collections.route("/collections/<collectID>/recipes", methods=["DELETE"])
def remove_recipe_from_collection(collectID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            DELETE FROM CollectionRecipes
            WHERE collectID = %s AND recipeID = %s
        '''
        cursor.execute(the_query, (
            collectID,
            data.get('recipeID')
        ))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Recipe not found in collection"}), 404
            
        return jsonify({"message": "Recipe removed from collection successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400