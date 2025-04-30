from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["auth_db"]
users = db["users"]
apikeys = db["apikeys"]
