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

@recipes.route("/recipes/create", methods=["POST"])
def create_recipe():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO Recipes (userID, catID, name, description, steps, picture, difficulty)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(the_query, (
            data.get('userID'),
            data.get('catID'),
            data.get('name'),
            data.get('description'),
            data.get('steps'),
            data.get('picture'),
            data.get('difficulty')
        ))
        db.get_db().commit()
        
        new_recipe_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Recipe created successfully", "recipeID": new_recipe_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

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

@recipes.route("/recipes/<recipeID>", methods=["PUT"])
def update_recipe(recipeID):
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

@recipes.route("/recipes/<recipeID>", methods=["DELETE"])
def delete_recipe(recipeID):
    try:
        cursor = db.get_db().cursor()
        the_query = '''
            DELETE FROM Recipes
            WHERE recipeID = %s
        '''
        cursor.execute(the_query, (recipeID,))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Recipe not found"}), 404
            
        return jsonify({"message": "Recipe deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@recipes.route("/recipes/search", methods=["GET"])
def search_recipes():
    name = request.args.get('name')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    cursor = db.get_db().cursor()
    
    conditions = []
    params = []
    
    if name:
        conditions.append("name LIKE %s")
        params.append(f"%{name}%")
    if category:
        conditions.append("catID = %s")
        params.append(category)
    if difficulty:
        conditions.append("difficulty = %s")
        params.append(difficulty)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    the_query = f'''
        SELECT userID, catID, name, description, steps, picture, difficulty, recipeID
        FROM Recipes
        WHERE {where_clause}
    '''
    
    cursor.execute(the_query, tuple(params))
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@recipes.route("/recipes/user/<userID>", methods=["GET"])
def get_user_recipes(userID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT userID, catID, name, description, steps, picture, difficulty, recipeID
        FROM Recipes
        WHERE userID = %s
    '''
    cursor.execute(the_query, (userID,))
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@recipes.route("/recipes/<recipeID>/ingredients", methods=["GET"])
def get_recipe_ingredients(recipeID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT ri.ingrID, i.name, ri.quantity, ri.unit
        FROM RecipeIngredients ri
        JOIN Ingredients i ON ri.ingrID = i.ingrID
        WHERE ri.recipeID = %s
    '''
    cursor.execute(the_query, (recipeID,))
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@recipes.route("/recipes/<recipeID>/ingredients", methods=["POST"])
def add_recipe_ingredients(recipeID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO RecipeIngredients (recipeID, ingrID, quantity, unit)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(the_query, (
            recipeID,
            data.get('ingrID'),
            data.get('quantity'),
            data.get('unit')
        ))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Ingredient added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

@recipes.route("/recipes/<recipeID>/ingredients", methods=["PUT"])
def update_recipe_ingredients(recipeID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            UPDATE RecipeIngredients
            SET quantity = %s, unit = %s
            WHERE recipeID = %s AND ingrID = %s
        '''
        cursor.execute(the_query, (
            data.get('quantity'),
            data.get('unit'),
            recipeID,
            data.get('ingrID')
        ))
        db.get_db().commit()
        cursor.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Ingredient not found for this recipe"}), 404
            
        return jsonify({"message": "Ingredient updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400

@recipes.route("/recipes/<recipeID>/tags", methods=["GET"])
def get_recipe_tags(recipeID):
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT rt.tagID, t.name
        FROM RecipeTags rt
        JOIN Tags t ON rt.tagID = t.tagID
        WHERE rt.recipeID = %s
    '''
    cursor.execute(the_query, (recipeID,))
    theDATA = cursor.fetchall()
    cursor.close()
    
    return jsonify(theDATA)

@recipes.route("/recipes/<recipeID>/tags", methods=["POST"])
def add_recipe_tag(recipeID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        the_query = '''
            INSERT INTO RecipeTags (recipeID, tagID)
            VALUES (%s, %s)
        '''
        cursor.execute(the_query, (recipeID, data.get('tagID')))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Tag added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400