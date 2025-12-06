from flask import Blueprint, jsonify, request
from backend.db_connection import db
#from mysql.connector import Error
from flask import current_app

users = Blueprint("users", __name__)

@users.route("/users", methods=["GET"])
def get_all_users():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT userID, username, email, bio, verified, createdAt
        FROM Users
    '''
    cursor.execute(the_query)
    theDATA = cursor.fetchall()
    cursor.close()

    return jsonify(theDATA)

@users.route("/users/create", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO Users (username, email, password, bio, verified)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(the_query, (
            data.get('username'),
            data.get('email'),
            data.get('password'),
            data.get('bio'),
            data.get('verified', False)
        ))
        db.get_db().commit()
        
        new_user_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "User created successfully", "userID": new_user_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

@users.route("/users/<userID>", methods=["GET"])
def get_user(userID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT userID, username, email, bio, verified, createdAt
        FROM Users
        WHERE userID = %s
    '''
    cursor.execute(the_query, (userID,))
    theDATA = cursor.fetchone()
    cursor.close()

    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "User not found"}), 404

@users.route("/users/<userID>", methods=["PUT"])
def update_user(userID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            UPDATE Users
            SET username = %s, email = %s, bio = %s, verified = %s
            WHERE userID = %s
        '''
        cursor.execute(the_query, (
            data.get('username'),
            data.get('email'),
            data.get('bio'),
            data.get('verified'),
            userID
        ))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({"message": "User updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@users.route("/users/<userID>", methods=["DELETE"])
def delete_user(userID):
    try:
        cursor = db.get_db().cursor()
        the_query = '''
            DELETE FROM Users
            WHERE userID = %s
        '''
        cursor.execute(the_query, (userID,))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@users.route("/users/<userID>/statistics", methods=["GET"])
def get_user_statistics(userID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT 
            u.userID,
            u.username,
            COUNT(DISTINCT r.recipeID) as total_recipes,
            AVG(rat.rating) as average_rating,
            COUNT(DISTINCT rat.ratingID) as total_ratings
        FROM Users u
        LEFT JOIN Recipes r ON u.userID = r.userID
        LEFT JOIN Ratings rat ON r.recipeID = rat.recipeID
        WHERE u.userID = %s
        GROUP BY u.userID, u.username
    '''
    cursor.execute(the_query, (userID,))
    theDATA = cursor.fetchone()
    cursor.close()
    
    if theDATA:
        return jsonify(theDATA)
    else:
        return jsonify({"error": "User not found"}), 404