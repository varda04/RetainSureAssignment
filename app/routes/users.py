from flask import Blueprint, request, jsonify, current_app
from app.db import get_db
from app.models import user_to_dict
from app.utils import hash_password, check_password

import sqlite3

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def home():
    return jsonify({"message": "User Management System"}), 200

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    db = get_db()
    cursor = db.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([user_to_dict(user) for user in users]), 200

@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(user_to_dict(user)), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = {"name", "email", "password"}
    if not data or not required_fields.issubset(data):
        return jsonify({"error": "Missing fields"}), 400

    db = get_db()
    hashed = hash_password(data['password'])

    try:
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (data['name'], data['email'], hashed))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    return jsonify({"message": "User created"}), 201

@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    db = get_db()
    fields = []
    values = []

    for key in ['name', 'email']:
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])

    if not fields:
        return jsonify({"error": "Nothing to update"}), 400

    values.append(user_id)
    db.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
    db.commit()

    return jsonify({"message": "User updated"}), 200

@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return jsonify({"message": f"User {user_id} deleted"}), 200

@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400

    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",))
    users = cursor.fetchall()
    return jsonify([user_to_dict(user) for user in users]), 200

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400

    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE email = ?", (data['email'],))
    user = cursor.fetchone()
    if user and check_password(data['password'], user["password"]):
        return jsonify({"status": "success", "user_id": user["id"]}), 200
    return jsonify({"status": "failed"}), 401