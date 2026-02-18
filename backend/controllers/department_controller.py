from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.department_service import (
    create_department_service,
    get_all_departments_service,
    get_department_by_id_service
)

department_bp = Blueprint("department", __name__)


# -----------------------------------------
# Create Department (Admin Only)
# POST /api/departments/
# -----------------------------------------
@department_bp.route("/", methods=["POST"])
@jwt_required()
def create_department():
    try:
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()

        name = data.get("name")
        description = data.get("description")

        if not name:
            return jsonify({"error": "Department name is required"}), 400

        result = create_department_service(name, description)

        return jsonify({
            "message": "Department created successfully",
            "department": result
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# -----------------------------------------
# Get All Departments
# GET /api/departments/
# -----------------------------------------
@department_bp.route("/", methods=["GET"])
@jwt_required()
def get_departments():
    try:
        departments = get_all_departments_service()

        return jsonify({
            "departments": departments
        }), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# -----------------------------------------
# Get Department by ID
# GET /api/departments/<id>
# -----------------------------------------
@department_bp.route("/<int:department_id>", methods=["GET"])
@jwt_required()
def get_department(department_id):
    try:
        department = get_department_by_id_service(department_id)

        return jsonify(department), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    except Exception:
        return jsonify({"error": "Internal server error"}), 500