from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    # Get the user data from the request
    data = request.get_json()

    # Perform validation on the user data
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid user data'}), 400

    # Create a new user in the database
    # Replace this with your own logic to store the user data

    # Return a success response
    return jsonify({'message': 'User registered successfully'}), 200

if __name__ == '__main__':
    app.run()
