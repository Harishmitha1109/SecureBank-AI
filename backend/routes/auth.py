from flask import Blueprint, request, jsonify
from database import users, accounts

auth = Blueprint("auth", __name__)

# =========================
# REGISTER
# =========================

@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    existing_user = users.find_one({"email": email})

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400

    # Save User
    users.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    # Create Bank Account
    accounts.insert_one({
        "email": email,
        "balance": 154320
    })

    return jsonify({
        "success": True,
        "message": "Registration Successful"
    }), 201


# =========================
# LOGIN
# =========================

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = users.find_one({
        "email": email,
        "password": password
    })

    if user:
        return jsonify({
            "success": True,
            "message": "Login Successful",
            "name": user["name"],
            "email": user["email"]
        }), 200

    return jsonify({
        "success": False,
        "message": "Invalid Email or Password"
    }), 401


# =========================
# GET PROFILE
# =========================

@auth.route("/profile/<email>", methods=["GET"])
def get_profile(email):

    user = users.find_one(
        {"email": email},
        {"_id": 0, "password": 0}
    )

    if user:
        return jsonify(user)

    return jsonify({
        "message": "User not found"
    }), 404


# =========================
# UPDATE PROFILE
# =========================

@auth.route("/profile", methods=["PUT"])
def update_profile():

    data = request.get_json()

    email = data.get("email")

    users.update_one(
        {"email": email},
        {
            "$set": {
                "name": data.get("name"),
                "phone": data.get("phone"),
                "address": data.get("address")
            }
        }
    )

    return jsonify({
        "success": True,
        "message": "Profile Updated Successfully"
    })