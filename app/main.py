from flask import Flask, request, jsonify, send_from_directory
from mongoapp import init_db, get_items, add_item, delete_item, register_user, login_user

app = Flask(__name__, static_folder="static")
db = init_db()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/items", methods=["GET"])
def read_items():
    return jsonify(get_items(db))

@app.route("/items", methods=["POST"])
def add_items():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    return jsonify(add_item(db, data)), 201

@app.route("/items/<item_id>", methods=["DELETE"])
def delete_items(item_id):
    return jsonify(delete_item(db, item_id))

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return jsonify(register_user(db, data["name"], data["password"]))

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = login_user(db, data["name"], data["password"])
    if not result:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
