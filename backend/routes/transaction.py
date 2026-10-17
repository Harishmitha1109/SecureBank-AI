from flask import Blueprint, request, jsonify
from database import transactions, accounts
from datetime import datetime
import random

transaction_api = Blueprint("transaction_api", __name__)

# ============================================
# Transfer Money
# ============================================

@transaction_api.route("/transfer", methods=["POST"])
def transfer():

    data = request.get_json()

    email = data.get("email")
    amount = float(data.get("amount"))

    # Check Account
    account = accounts.find_one({"email": email})

    if not account:
        return jsonify({
            "success": False,
            "message": "Account not found"
        }), 404

    # Check Balance
    if account["balance"] < amount:
        return jsonify({
            "success": False,
            "message": "Insufficient Balance"
        }), 400

    now = datetime.now()

    txn_id = "TXN" + str(random.randint(100000, 999999))

    # Save Transaction
    transactions.insert_one({

        "email": email,
        "recipient": data.get("recipient"),
        "account": data.get("account"),
        "ifsc": data.get("ifsc"),
        "amount": amount,
        "remarks": data.get("remarks"),
        "type": "Debit",
        "transaction_id": txn_id,
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%I:%M %p")

    })

    # Update Balance
    accounts.update_one(

        {"email": email},

        {
            "$inc": {
                "balance": -amount
            }
        }

    )

    return jsonify({

        "success": True,
        "message": "Transfer Successful",
        "transaction_id": txn_id,
        "balance": account["balance"] - amount

    }), 201


# ============================================
# Deposit Money
# ============================================

@transaction_api.route("/deposit", methods=["POST"])
def deposit():

    data = request.get_json()

    email = data.get("email")
    amount = float(data.get("amount"))

    now = datetime.now()

    txn_id = "TXN" + str(random.randint(100000, 999999))

    # Save Deposit
    transactions.insert_one({

        "email": email,
        "recipient": "SELF",
        "account": "-",
        "ifsc": "-",
        "amount": amount,
        "remarks": data.get("remarks"),
        "type": "Credit",
        "transaction_id": txn_id,
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%I:%M %p")

    })

    # Update Balance
    accounts.update_one(

        {"email": email},

        {
            "$inc": {
                "balance": amount
            }
        }

    )

    new_balance = accounts.find_one({"email": email})["balance"]

    return jsonify({

        "success": True,
        "message": "Deposit Successful",
        "transaction_id": txn_id,
        "balance": new_balance

    }), 201


# ============================================
# Get Transactions
# ============================================

@transaction_api.route("/transactions/<email>", methods=["GET"])
def get_transactions(email):

    data = list(

        transactions.find(

            {"email": email},

            {"_id": 0}

        )

    )

    return jsonify(data)


# ============================================
# Get Balance
# ============================================

@transaction_api.route("/balance/<email>", methods=["GET"])
def get_balance(email):

    account = accounts.find_one(

        {"email": email},

        {"_id": 0}

    )

    if account:

        return jsonify(account)

    return jsonify({

        "balance": 0

    })