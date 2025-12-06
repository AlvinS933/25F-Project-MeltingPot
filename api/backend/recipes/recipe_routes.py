from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

recipes = Blueprint('recipes', __name__)

# Get all recipes
@recipes.route('/recipes', methods=['GET'])
def get_all_recipes():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Recipes')
    recipes_data = cursor.fetchall()
    return jsonify(recipes_data)

# Get recipes by user
@recipes.route('/recipes/user/<int:user_id>', methods=['GET'])
def get_recipes_by_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Recipes WHERE userID = %s', (user_id,))
    recipes_data = cursor.fetchall()
    return jsonify(recipes_data)

# Get a specific recipe by ID
@recipes.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Recipes WHERE recipeID = %s', (recipe_id,))
    recipe_data = cursor.fetchone()
    
    if not recipe_data:
        return jsonify({'error': 'Recipe not found'}), 404
    
    return jsonify(recipe_data)

# Create a new recipe
@recipes.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    user_id = data.get('userID')
    cat_id = data.get('catID')
    name = data.get('name')
    description = data.get('description', '')
    steps = data.get('steps', '')
    picture = data.get('picture')
    difficulty = data.get('difficulty', 3)
    
    if not all([user_id, cat_id, name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Recipes (userID, catID, name, description, steps, picture, difficulty)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    
    try:
        cursor.execute(query, (user_id, cat_id, name, description, steps, picture, difficulty))
        db.get_db().commit()
        
        new_recipe_id = cursor.lastrowid
        return jsonify({
            'message': 'Recipe created successfully',
            'recipeID': new_recipe_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a recipe
@recipes.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    
    updates = []
    values = []
    
    if 'name' in data:
        updates.append('name = %s')
        values.append(data['name'])
    
    if 'description' in data:
        updates.append('description = %s')
        values.append(data['description'])
    
    if 'steps' in data:
        updates.append('steps = %s')
        values.append(data['steps'])
    
    if 'difficulty' in data:
        updates.append('difficulty = %s')
        values.append(data['difficulty'])
    
    if 'catID' in data:
        updates.append('catID = %s')
        values.append(data['catID'])
    
    if 'picture' in data:
        updates.append('picture = %s')
        values.append(data['picture'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(recipe_id)
    
    cursor = db.get_db().cursor()
    query = f"UPDATE Recipes SET {', '.join(updates)} WHERE recipeID = %s"
    
    try:
        cursor.execute(query, values)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Recipe not found'}), 404
        
        return jsonify({'message': 'Recipe updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a recipe
@recipes.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM Recipes WHERE recipeID = %s'
    
    try:
        cursor.execute(query, (recipe_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Recipe not found'}), 404
        
        return jsonify({'message': 'Recipe deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get ingredients for a recipe
@recipes.route('/recipes/<int:recipe_id>/ingredients', methods=['GET'])
def get_recipe_ingredients(recipe_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT i.ingrID, i.name, i.description
        FROM Ingredients i
        JOIN RecipeIngredients ri ON i.ingrID = ri.ingrID
        WHERE ri.recipeID = %s
    '''
    cursor.execute(query, (recipe_id,))
    ingredients = cursor.fetchall()
    return jsonify(ingredients)

# Add ingredient to recipe
@recipes.route('/recipes/ingredients', methods=['POST'])
def add_recipe_ingredient():
    data = request.get_json()
    recipe_id = data.get('recipeID')
    ingr_id = data.get('ingrID')
    
    if not all([recipe_id, ingr_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    cursor = db.get_db().cursor()
    query = 'INSERT INTO RecipeIngredients (recipeID, ingrID) VALUES (%s, %s)'
    
    try:
        cursor.execute(query, (recipe_id, ingr_id))
        db.get_db().commit()
        return jsonify({'message': 'Ingredient added to recipe'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get tags for a recipe
@recipes.route('/recipes/<int:recipe_id>/tags', methods=['GET'])
def get_recipe_tags(recipe_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT t.tagID, t.name, t.description
        FROM Tags t
        JOIN RecipeTags rt ON t.tagID = rt.tagID
        WHERE rt.recipeID = %s
    '''
    cursor.execute(query, (recipe_id,))
    tags = cursor.fetchall()
    return jsonify(tags)

# Add tag to recipe
@recipes.route('/recipes/tags', methods=['POST'])
def add_recipe_tag():
    data = request.get_json()
    recipe_id = data.get('recipeID')
    tag_id = data.get('tagID')
    
    if not all([recipe_id, tag_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    cursor = db.get_db().cursor()
    query = 'INSERT INTO RecipeTags (recipeID, tagID) VALUES (%s, %s)'
    
    try:
        cursor.execute(query, (recipe_id, tag_id))
        db.get_db().commit()
        return jsonify({'message': 'Tag added to recipe'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500