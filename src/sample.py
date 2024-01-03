from flask import Flask, request, jsonify
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create a list to store user data
users = []

# Route to create a new user
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    val = (data['name'], data['email'])
    cursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'User created successfully'})

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    users = []
    for user in result:
        user_data = {
            'id': user[0],
            'name': user[1],
            'email': user[2]
        }
        users.append(user_data)
    return jsonify(users)

# Route to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    sql = "SELECT * FROM users WHERE id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        user_data = {
            'id': result[0],
            'name': result[1],
            'email': result[2]
        }
        return jsonify(user_data)
    return jsonify({'message': 'User not found'})

# Route to update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    val = (data['name'], data['email'], user_id)
    cursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'User updated successfully'})

# Route to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    sql = "DELETE FROM users WHERE id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
def create_user():
    data = request.get_json()
    users.append(data)
    return jsonify({'message': 'User created successfully'})

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Route to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({'message': 'User not found'})

# Route to update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Check if the username and password are valid
    if username == 'admin' and password == 'password':
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'})

if __name__ == '__main__':
    app.run(debug=True)

# Route to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)
