from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

from services.availability_slot_service import (
    create_slot_service,
    create_bulk_slots_service,
    create_weekly_slots_service
)

slot_bp = Blueprint("slots", __name__)


# -----------------------------------------
# Create Slot (Admin Only)
# POST /api/slots/
# -----------------------------------------
@slot_bp.route("/", methods=["POST"])
@jwt_required()
def create_slot():
    try:
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()

        doctor_id = data.get("doctor_id")
        date = data.get("date")  # YYYY-MM-DD
        start_time = data.get("start_time")  # HH:MM:SS
        end_time = data.get("end_time")

        if not all([doctor_id, date, start_time, end_time]):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert strings to proper types
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

        result = create_slot_service(
            doctor_id,
            date_obj,
            start_time_obj,
            end_time_obj
        )

        return jsonify({
            "message": "Slot created successfully",
            "slot": result
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# -----------------------------------------
# Create Bulk Slots (Admin Only)
# POST /api/slots/bulk
# -----------------------------------------
@slot_bp.route("/bulk", methods=["POST"])
@jwt_required()
def create_bulk_slots():
    try:
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()

        doctor_id = data.get("doctor_id")
        date = data.get("date")  # YYYY-MM-DD
        start_time = data.get("start_time")  # HH:MM
        end_time = data.get("end_time")      # HH:MM
        slot_duration = data.get("slot_duration_minutes")

        if not all([doctor_id, date, start_time, end_time, slot_duration]):
            return jsonify({"error": "Missing required fields"}), 400

        result = create_bulk_slots_service(
            doctor_id,
            date,
            start_time,
            end_time,
            slot_duration
        )

        return jsonify({
            "message": "Bulk slots created successfully",
            "slots": result
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# -----------------------------------------
# Create Weekly Recurring Slots (Admin Only)
# POST /api/slots/weekly
# -----------------------------------------
@slot_bp.route("/weekly", methods=["POST"])
@jwt_required()
def create_weekly_slots():
    try:
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()

        doctor_id = data.get("doctor_id")
        weekday = data.get("weekday")  # 0=Monday, 6=Sunday
        start_time = data.get("start_time")  # HH:MM
        end_time = data.get("end_time")      # HH:MM
        slot_duration = data.get("slot_duration_minutes")
        weeks = data.get("number_of_weeks")

        if not all([doctor_id, weekday is not None, start_time, end_time, slot_duration, weeks]):
            return jsonify({"error": "Missing required fields"}), 400

        result = create_weekly_slots_service(
            doctor_id=doctor_id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            number_of_weeks=weeks
        )

        return jsonify({
            "message": "Weekly slots created successfully",
            "slots": result
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500