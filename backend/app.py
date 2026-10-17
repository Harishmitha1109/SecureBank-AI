from flask import Flask
from flask_cors import CORS

from database import db
from routes.auth import auth
from routes.behavior import behavior_api
from routes.transaction import transaction_api
from routes.ai import ai_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth)
app.register_blueprint(behavior_api)
app.register_blueprint(transaction_api)
app.register_blueprint(ai_api)

@app.route("/")
def home():
    return {
        "message": "SecureBank AI Backend Running 🚀"
    }

@app.route("/test-db")
def test_db():
    return {
        "database": db.name,
        "status": "Connected Successfully"
    }

if __name__ == "__main__":
    app.run(debug=True)