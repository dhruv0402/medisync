from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
        user_id = get_jwt_identity()

        # Strict admin check
        if claims.get("role") != "admin":
            return jsonify({
                "error": "Access denied",
                "message": "Only admin users can create departments"
            }), 403

        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        name = data.get("name")
        description = data.get("description")

        if not name or not isinstance(name, str):
            return jsonify({"error": "Department name must be a string"}), 400

        result = create_department_service(name.strip(), description)

        return jsonify({
            "message": "Department created successfully",
            "created_by": user_id,
            "department": result
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


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
            "count": len(departments),
            "departments": departments
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


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

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500