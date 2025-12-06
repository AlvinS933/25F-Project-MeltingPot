from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Ingredients Blueprint
ingredients = Blueprint("ingredients", __name__)

@ingredients.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT ingrID, name, category
        FROM Ingredients
    '''
    cursor.execute(the_query)
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@ingredients.route("/ingredients/create", methods=["POST"])
def create_ingredient():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO Ingredients (name, category)
            VALUES (%s, %s)
        '''
        cursor.execute(the_query, (
            data.get('name'),
            data.get('category')
        ))
        db.get_db().commit()
        
        new_ingr_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Ingredient created successfully", "ingrID": new_ingr_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

@ingredients.route("/ingredients/<ingrID>", methods=["GET"])
def get_ingredient(ingrID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT ingrID, name, category
        FROM Ingredients
        WHERE ingrID = %s
    '''
    cursor.execute(the_query, (ingrID,))
    theDATA = cursor.fetchone()
    cursor.close()
    
    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "Ingredient not found"}), 404

@ingredients.route("/ingredients/<ingrID>", methods=["PUT"])
def update_ingredient(ingrID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            UPDATE Ingredients
            SET name = %s, category = %s
            WHERE ingrID = %s
        '''
        cursor.execute(the_query, (
            data.get('name'),
            data.get('category'),
            ingrID
        ))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Ingredient not found"}), 404
            
        return jsonify({"message": "Ingredient updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400