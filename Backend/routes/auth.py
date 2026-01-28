from flask import Blueprint, request, jsonify
from models.user import create_user, find_user_by_email
from utils.password import hash_password
from utils.password import verify_password
from flask_jwt_extended import create_access_token
import extensions
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if find_user_by_email(email):
        return jsonify({"error": "User already exists"}), 409

    create_user(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    return jsonify({"message": "User created successfully"}), 201



@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = find_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]))

    return jsonify({
        "access_token": access_token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }), 200



@auth_bp.route("/auth/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = extensions.db.users.find_one(
        {"_id": ObjectId(user_id)},
        {"password_hash": 0}
    )

    return jsonify({
        "name": user["name"],
        "email": user["email"]
    }), 200