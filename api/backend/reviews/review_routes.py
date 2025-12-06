from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

reviews = Blueprint('reviews', __name__)

# Get all reviews
@reviews.route('/reviews', methods=['GET'])
def get_all_reviews():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Reviews')
    reviews_data = cursor.fetchall()
    return jsonify(reviews_data)

# Get reviews for a specific recipe
@reviews.route('/reviews/recipe/<int:recipe_id>', methods=['GET'])
def get_reviews_by_recipe(recipe_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Reviews WHERE recipeID = %s', (recipe_id,))
    reviews_data = cursor.fetchall()
    return jsonify(reviews_data)

# Get reviews by a specific user
@reviews.route('/reviews/user/<int:user_id>', methods=['GET'])
def get_reviews_by_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Reviews WHERE userID = %s', (user_id,))
    reviews_data = cursor.fetchall()
    return jsonify(reviews_data)

# Create a new review
@reviews.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    recipe_id = data.get('recipeID')
    user_id = data.get('userID')
    review = data.get('review')
    
    if not all([recipe_id, user_id, review]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Reviews (recipeID, userID, review)
        VALUES (%s, %s, %s)
    '''
    
    try:
        cursor.execute(query, (recipe_id, user_id, review))
        db.get_db().commit()
        return jsonify({'message': 'Review created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a review
@reviews.route('/reviews/<int:recipe_id>/<int:user_id>', methods=['PUT'])
def update_review(recipe_id, user_id):
    data = request.get_json()
    review = data.get('review')
    
    if not review:
        return jsonify({'error': 'Review text is required'}), 400
    
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Reviews 
        SET review = %s
        WHERE recipeID = %s AND userID = %s
    '''
    
    try:
        cursor.execute(query, (review, recipe_id, user_id))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Review not found'}), 404
        
        return jsonify({'message': 'Review updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a review
@reviews.route('/reviews/<int:recipe_id>/<int:user_id>', methods=['DELETE'])
def delete_review(recipe_id, user_id):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM Reviews WHERE recipeID = %s AND userID = %s'
    
    try:
        cursor.execute(query, (recipe_id, user_id))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Review not found'}), 404
        
        return jsonify({'message': 'Review deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500