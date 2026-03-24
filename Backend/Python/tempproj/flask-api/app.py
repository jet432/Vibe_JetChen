
from flask import Flask, jsonify

# Sample static data collection
users = [
	{"id": 1, "name": "Alice", "email": "alice@example.com"},
	{"id": 2, "name": "Bob", "email": "bob@example.com"},
	{"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

app = Flask(__name__)

@app.route('/')
def home():
	return jsonify({"message": "Welcome to the Flask API!"})


# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
	return jsonify(users)

# Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
	user = next((u for u in users if u['id'] == user_id), None)
	if user:
		return jsonify(user)
	return jsonify({"error": "User not found"}), 404


# Create a new user
from flask import request
@app.route('/users', methods=['POST'])
def create_user():
	data = request.get_json()
	if not data or not data.get('name') or not data.get('email'):
		return jsonify({"error": "Name and email are required."}), 400
	new_id = max([u['id'] for u in users], default=0) + 1
	new_user = {
		"id": new_id,
		"name": data['name'],
		"email": data['email']
	}
	users.append(new_user)
	return jsonify(new_user), 201


# Update an existing user (replace all fields)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
	data = request.get_json()
	user = next((u for u in users if u['id'] == user_id), None)
	if not user:
		return jsonify({"error": "User not found"}), 404
	if not data or not data.get('name') or not data.get('email'):
		return jsonify({"error": "Name and email are required."}), 400
	user['name'] = data['name']
	user['email'] = data['email']
	return jsonify(user)


# Partially update a user
@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
	data = request.get_json()
	user = next((u for u in users if u['id'] == user_id), None)
	if not user:
		return jsonify({"error": "User not found"}), 404
	if not data:
		return jsonify({"error": "No data provided."}), 400
	user.update({k: v for k, v in data.items() if k in user and k != 'id'})
	return jsonify(user)


# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	global users
	user = next((u for u in users if u['id'] == user_id), None)
	if not user:
		return jsonify({"error": "User not found"}), 404
	users = [u for u in users if u['id'] != user_id]
	return jsonify({"message": f"User {user_id} deleted."})

if __name__ == '__main__':
	app.run(debug=True)
