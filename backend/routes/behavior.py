from flask import Blueprint, request, jsonify
from database import behavior

behavior_api = Blueprint("behavior_api", __name__)


# ===========================
# Save Behavioral Data
# ===========================

@behavior_api.route("/behavior", methods=["POST"])
def save_behavior():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No behavior data received"
        }), 400

    email = data.get("email")

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required"
        }), 400

    behavior.insert_one({

        "email": email,

        "device": data.get("device"),

        "mouse_distance": data.get("mouse_distance", 0),

        "clicks": data.get("clicks", 0),

        "scroll_distance": data.get("scroll_distance", 0),

        "session_duration": data.get("session_duration", 0),

        "timestamp": data.get("timestamp")

    })

    return jsonify({
        "success": True,
        "message": "Behavior Saved"
    }), 201