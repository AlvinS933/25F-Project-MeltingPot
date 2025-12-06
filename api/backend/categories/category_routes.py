# ==================== category_routes.py ====================
from flask import Blueprint, request, jsonify
from backend.db_connection import db

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
def get_all_categories():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Categories')
    return jsonify(cursor.fetchall())

@categories.route('/categories/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Categories WHERE catID = %s', (cat_id,))
    data = cursor.fetchone()
    if not data:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(data)

@categories.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute('INSERT INTO Categories (name, description) VALUES (%s, %s)', 
                      (name, description))
        db.get_db().commit()
        return jsonify({'message': 'Category created', 'catID': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    data = request.get_json()
    updates = []
    values = []
    
    if 'name' in data:
        updates.append('name = %s')
        values.append(data['name'])
    if 'description' in data:
        updates.append('description = %s')
        values.append(data['description'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(cat_id)
    cursor = db.get_db().cursor()
    try:
        cursor.execute(f"UPDATE Categories SET {', '.join(updates)} WHERE catID = %s", values)
        db.get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'message': 'Category updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Categories WHERE catID = %s', (cat_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'message': 'Category deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== tag_routes.py ====================
from flask import Blueprint, request, jsonify
from backend.db_connection import db

tags = Blueprint('tags', __name__)

@tags.route('/tags', methods=['GET'])
def get_all_tags():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Tags')
    return jsonify(cursor.fetchall())

@tags.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Tags WHERE tagID = %s', (tag_id,))
    data = cursor.fetchone()
    if not data:
        return jsonify({'error': 'Tag not found'}), 404
    return jsonify(data)

@tags.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute('INSERT INTO Tags (name, description) VALUES (%s, %s)', 
                      (name, description))
        db.get_db().commit()
        return jsonify({'message': 'Tag created', 'tagID': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tags.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.get_json()
    updates = []
    values = []
    
    if 'name' in data:
        updates.append('name = %s')
        values.append(data['name'])
    if 'description' in data:
        updates.append('description = %s')
        values.append(data['description'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(tag_id)
    cursor = db.get_db().cursor()
    try:
        cursor.execute(f"UPDATE Tags SET {', '.join(updates)} WHERE tagID = %s", values)
        db.get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Tag not found'}), 404
        return jsonify({'message': 'Tag updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tags.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Tags WHERE tagID = %s', (tag_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Tag not found'}), 404
        return jsonify({'message': 'Tag deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ingredient_routes.py ====================
from flask import Blueprint, request, jsonify
from backend.db_connection import db

ingredients = Blueprint('ingredients', __name__)

@ingredients.route('/ingredients', methods=['GET'])
def get_all_ingredients():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ingredients')
    return jsonify(cursor.fetchall())

@ingredients.route('/ingredients/<int:ingr_id>', methods=['GET'])
def get_ingredient(ingr_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ingredients WHERE ingrID = %s', (ingr_id,))
    data = cursor.fetchone()
    if not data:
        return jsonify({'error': 'Ingredient not found'}), 404
    return jsonify(data)

@ingredients.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute('INSERT INTO Ingredients (name, description) VALUES (%s, %s)', 
                      (name, description))
        db.get_db().commit()
        return jsonify({'message': 'Ingredient created', 'ingrID': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredients.route('/ingredients/<int:ingr_id>', methods=['PUT'])
def update_ingredient(ingr_id):
    data = request.get_json()
    updates = []
    values = []
    
    if 'name' in data:
        updates.append('name = %s')
        values.append(data['name'])
    if 'description' in data:
        updates.append('description = %s')
        values.append(data['description'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(ingr_id)
    cursor = db.get_db().cursor()
    try:
        cursor.execute(f"UPDATE Ingredients SET {', '.join(updates)} WHERE ingrID = %s", values)
        db.get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Ingredient not found'}), 404
        return jsonify({'message': 'Ingredient updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredients.route('/ingredients/<int:ingr_id>', methods=['DELETE'])
def delete_ingredient(ingr_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Ingredients WHERE ingrID = %s', (ingr_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Ingredient not found'}), 404
        return jsonify({'message': 'Ingredient deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500