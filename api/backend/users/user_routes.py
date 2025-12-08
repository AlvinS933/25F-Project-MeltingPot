from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

users = Blueprint('users', __name__)

# Get all users
@users.route('/users', methods=['GET'])
def get_all_users():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT userID, username, bio, verified FROM Users')
    users_data = cursor.fetchall()
    return jsonify(users_data)

# Get all administrators
@users.route('/admins', methods=['GET'])
def get_all_admins():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT adminID, username FROM Administrators')
    admins_data = cursor.fetchall()
    return jsonify(admins_data)

# Get all data analysts
@users.route('/analysts', methods=['GET'])
def get_all_analysts():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT analystID, username FROM DataAnalysts')
    analysts_data = cursor.fetchall()
    return jsonify(analysts_data)

# Get a specific user by ID
@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT userID, username, bio, verified FROM Users WHERE userID = %s', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user_data)

# Create a new user
@users.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    bio = data.get('bio', '')
    verified = data.get('verified', 0)
    
    if not all([username, password]):
        return jsonify({'error': 'Username and password are required'}), 400
    
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Users (username, password, bio, verified)
        VALUES (%s, %s, %s, %s)
    '''
    
    try:
        cursor.execute(query, (username, password, bio, verified))
        db.get_db().commit()
        
        new_user_id = cursor.lastrowid
        return jsonify({
            'message': 'User created successfully',
            'userID': new_user_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a user
@users.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    # Build dynamic update query
    updates = []
    values = []
    
    if 'username' in data:
        updates.append('username = %s')
        values.append(data['username'])
    
    if 'bio' in data:
        updates.append('bio = %s')
        values.append(data['bio'])
    
    if 'verified' in data:
        updates.append('verified = %s')
        values.append(data['verified'])
    
    if 'password' in data:
        updates.append('password = %s')
        values.append(data['password'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(user_id)
    
    cursor = db.get_db().cursor()
    query = f"UPDATE Users SET {', '.join(updates)} WHERE userID = %s"
    
    try:
        cursor.execute(query, values)
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a user
@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM Users WHERE userID = %s'
    
    try:
        cursor.execute(query, (user_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Top 5 Highest Rated Users
@users.route('/users/top', methods=['GET'])
def get_highest_rated():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Ratings.userID, AVG(rating) as avgRating FROM Ratings JOIN Users On Ratings.userID = Users.userID GROUP BY Ratings.userID ORDER BY avgRating DESC LIMIT 5')
    users_data = cursor.fetchall()
    return jsonify(users_data)

# get recipe reports by admin id
@users.route('/admins/rr/<int:admin_id>', methods=['GET'])
def get_all_admins(admin_id):
    cursor = db.get_db().cursor()
    query = 'SELECT recipeID, reason FROM Administrators JOIN RecipeReports ON Administrators.adminID = RecipeReports.adminID WHERE RecipeReports.adminID = %s'
    cursor.execute(query, (admin_id,))
    admins_data = cursor.fetchall()
    return jsonify(admins_data)



