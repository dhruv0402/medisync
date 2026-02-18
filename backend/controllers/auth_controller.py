from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from services.auth_service import (
    create_user,
    get_user_by_email
)

auth_bp = Blueprint("auth", __name__)


# ----------------------------------------
# Register Endpoint
# ----------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")  # patient / doctor / admin

        if not all([name, email, password, role]):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        hashed_password = generate_password_hash(password)

        new_user = create_user(
            name=name,
            email=email,
            password=hashed_password,
            role=role
        )

        return jsonify({
            "message": "User registered successfully",
            "user_id": new_user.id,
            "role": new_user.role
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------
# Login Endpoint
# ----------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = get_user_by_email(email)

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Create JWT token
        access_token = create_access_token(
    identity=str(user.id),
    additional_claims={"role": user.role},
    expires_delta=timedelta(hours=2)
)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500