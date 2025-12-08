from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

ratings = Blueprint('ratings', __name__)

# Get all ratings
@ratings.route('/ratings', methods=['GET'])
def get_all_ratings():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ratings')
    ratings_data = cursor.fetchall()
    return jsonify(ratings_data)

# Get ratings for a specific recipe
@ratings.route('/ratings/recipe/<int:recipe_id>', methods=['GET'])
def get_ratings_by_recipe(recipe_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ratings WHERE recipeID = %s', (recipe_id,))
    ratings_data = cursor.fetchall()
    return jsonify(ratings_data)

# Get ratings by a specific user
@ratings.route('/ratings/user/<int:user_id>', methods=['GET'])
def get_ratings_by_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ratings WHERE userID = %s', (user_id,))
    ratings_data = cursor.fetchall()
    return jsonify(ratings_data)

# Create or update a rating
@ratings.route('/ratings', methods=['POST'])
def create_rating():
    data = request.get_json()
    recipe_id = data.get('recipeID')
    user_id = data.get('userID')
    rating = data.get('rating')
    
    if not all([recipe_id, user_id]) or rating is None:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    cursor = db.get_db().cursor()
    
    # Try to insert, if it exists, update
    query = '''
        INSERT INTO Ratings (recipeID, userID, rating)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE rating = %s
    '''
    
    try:
        cursor.execute(query, (recipe_id, user_id, rating, rating))
        db.get_db().commit()
        return jsonify({'message': 'Rating saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a rating
@ratings.route('/ratings/<int:recipe_id>/<int:user_id>', methods=['PUT'])
def update_rating(recipe_id, user_id):
    data = request.get_json()
    rating = data.get('rating')
    
    if rating is None:
        return jsonify({'error': 'Rating is required'}), 400
    
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Ratings 
        SET rating = %s
        WHERE recipeID = %s AND userID = %s
    '''
    
    try:
        cursor.execute(query, (rating, recipe_id, user_id))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Rating not found'}), 404
        
        return jsonify({'message': 'Rating updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a rating
@ratings.route('/ratings/<int:recipe_id>/<int:user_id>', methods=['DELETE'])
def delete_rating(recipe_id, user_id):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM Ratings WHERE recipeID = %s AND userID = %s'
    
    try:
        cursor.execute(query, (recipe_id, user_id))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Rating not found'}), 404
        
        return jsonify({'message': 'Rating deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Get top 5 ratings
@ratings.route('/ratings/topRated', methods=['GET'])
def topRated():
    cursor = db.get_db().cursor()
    cursor.execute("SELECT Ratings.recipeID, AVG(rating) as avgRating FROM Ratings JOIN Recipes ON Ratings.recipeID = Recipes.recipeID GROUP BY Ratings.recipeID ORDER BY avgRating DESC LIMIT 5")
    ratings_data = cursor.fetchall()
    return jsonify(ratings_data)