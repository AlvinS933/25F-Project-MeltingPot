from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Tags Blueprint
tags = Blueprint("tags", __name__)

@tags.route("/tags", methods=["GET"])
def get_all_tags():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT tagID, name
        FROM Tags
    '''
    cursor.execute(the_query)
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@tags.route("/tags/create", methods=["POST"])
def create_tag():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO Tags (name)
            VALUES (%s)
        '''
        cursor.execute(the_query, (data.get('name'),))
        db.get_db().commit()
        
        new_tag_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Tag created successfully", "tagID": new_tag_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400