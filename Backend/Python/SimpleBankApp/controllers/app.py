
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample user collection for registration and login
users = {
	'alice': {'username': 'alice', 'password': 'password123'},
	'bob': {'username': 'bob', 'password': 'securepass'},
}

# Register a new user
@app.route('/api/register', methods=['POST'])
def register():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')
	if not username or not password:
		return jsonify({'error': 'username and password are required'}), 400
	if username in users:
		return jsonify({'error': 'Username already exists'}), 400
	users[username] = {'username': username, 'password': password}
	return jsonify({'message': 'User registered successfully'}), 201

# Login user
@app.route('/api/login', methods=['POST'])
def login():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')
	user = users.get(username)
	if not user or user['password'] != password:
		return jsonify({'error': 'Invalid username or password'}), 401
	return jsonify({'message': 'Login successful', 'username': username}), 200

# In-memory data storage

# Sample premade accounts
accounts = {
	'1': {'userId': 1, 'accountType': 'SAVINGS', 'balance': 500.0},
	'2': {'userId': 2, 'accountType': 'CHECKING', 'balance': 1200.0},
	'3': {'userId': 3, 'accountType': 'BUSINESS', 'balance': 3000.0}
}
transactions = {
	'1': [
		{'type': 'deposit', 'amount': 500.0}
	],
	'2': [
		{'type': 'deposit', 'amount': 1200.0}
	],
	'3': [
		{'type': 'deposit', 'amount': 3000.0}
	]
}

# Helper to generate new account IDs
def generate_account_id():
	return str(len(accounts) + 1)


# Create a new account
@app.route('/api/accounts', methods=['POST'])
def createAccount():
	data = request.get_json()
	userId = data.get('userId')
	accountType = data.get('accountType')
	if userId is None or not accountType:
		return jsonify({'error': 'userId and accountType are required'}), 400
	# Ensure userId is a string for key consistency
	account_id = str(userId)
	if account_id in accounts:
		return jsonify({'error': 'Account with this userId already exists'}), 400
	accounts[account_id] = {
		'userId': userId,
		'accountType': accountType,
		'balance': 0.0
	}
	transactions[account_id] = []
	return jsonify(accounts[account_id]), 201


# Get account details
@app.route('/api/accounts/<account_id>', methods=['GET'])
def getAccount(account_id):
	account = accounts.get(account_id)
	if not account:
		return jsonify({'error': 'Account not found'}), 404
	# Find username by userId
	username = None
	userId = str(account.get('userId'))
	for user in users.values():
		if str(user.get('userId', '')) == userId or user.get('username') == userId:
			username = user.get('username')
			break
	response = {
		'accountID': account_id,
		'username': username,
		'balance': account.get('balance')
	}
	return jsonify(response)


# Deposit money
@app.route('/api/accounts/<account_id>/deposit', methods=['POST'])
def deposit(account_id):
	data = request.get_json()
	amount = data.get('amount', 0)
	return _deposit(account_id, amount)

def _deposit(account_id, amount):
	account = accounts.get(account_id)
	if not account:
		return jsonify({'error': 'Account not found'}), 404
	if amount <= 0:
		return jsonify({'error': 'Deposit amount must be positive'}), 400
	account['balance'] += amount
	transactions[account_id].append({'type': 'deposit', 'amount': amount})
	return jsonify(account)


# Withdraw money
@app.route('/api/accounts/<account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
	data = request.get_json()
	amount = data.get('amount', 0)
	return _withdraw(account_id, amount)

def _withdraw(account_id, amount):
	account = accounts.get(account_id)
	if not account:
		return jsonify({'error': 'Account not found'}), 404
	if amount <= 0:
		return jsonify({'error': 'Withdraw amount must be positive'}), 400
	if account['balance'] < amount:
		return jsonify({'error': 'Insufficient funds'}), 400
	account['balance'] -= amount
	transactions[account_id].append({'type': 'withdraw', 'amount': amount})
	return jsonify(account)


# View transaction history
import datetime
@app.route('/api/accounts/<account_id>/transactions', methods=['GET'])
def getTransactions(account_id):
	if account_id not in accounts:
		return jsonify({'error': 'Account not found'}), 404
	formatted = []
	for tx in transactions.get(account_id, []):
		# Add a date if not present (for demo, use now)
		date = tx.get('date')
		if not date:
			now = datetime.datetime.now()
			date = now.strftime('%Y-%m-%d')
		formatted.append({
			'type': tx.get('type'),
			'amount': tx.get('amount'),
			'date': date
		})
	return jsonify(formatted)

if __name__ == '__main__':
	app.run(debug=True)
