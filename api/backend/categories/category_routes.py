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

# Top 5 categories
@categories.route('/categories/top', methods=['GET'])
def top_cats():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Categories.name, COUNT(*) AS RecipeCount FROM Categories JOIN Recipes ON Categories.catID = Recipes.catID GROUP BY Categories.catID ORDER BY RecipeCount DESC LIMIT 5')
    return jsonify(cursor.fetchall())