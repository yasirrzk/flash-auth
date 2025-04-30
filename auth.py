from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import users, apikeys
from utils import hash_password, verify_password
import uuid

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = hash_password(data["password"])
    api_key = str(uuid.uuid4())

    if users.find_one({"username": username}):
        return jsonify({"msg": "User already exists"}), 400

    users.insert_one({
        "username": username,
        "password": password,
    })

    apikeys.insert_one({
        "username": username,
        "api_key": api_key
    })

    return jsonify({"msg": "Registered successfully", "api_key": api_key})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"username": data["username"]})

    if user and verify_password(data["password"], user["password"]):
        token = create_access_token(identity=data["username"])
        return jsonify({"access_token": token})
    return jsonify({"msg": "Invalid credentials"}), 401

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity() 
    user = users.find_one({'username': current_user}, {'_id': 0, 'password': 0})  
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify(user), 200
