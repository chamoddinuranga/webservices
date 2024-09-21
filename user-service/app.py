from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    user = {"id": len(users) + 1, "username": username}
    users.append(user)
    return jsonify(user), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
