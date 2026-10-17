from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["securebank_ai"]

# Collections
users = db["users"]

behavior = db["behavior"]

transactions = db["transactions"]

accounts = db["accounts"]      # NEW