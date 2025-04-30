from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import apikeys
from auth import auth_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "supersecret"
jwt = JWTManager(app)

app.register_blueprint(auth_bp)

def check_api_key(api_key, username):
    record = apikeys.find_one({"username": username, "api_key": api_key})
    return bool(record)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    username = get_jwt_identity()
    api_key = request.headers.get("X-API-KEY")

    if not api_key or not check_api_key(api_key, username):
        return jsonify({"msg": "Invalid or missing API Key"}), 403

    return jsonify({"msg": f"Welcome {username}, access granted."})

if __name__ == "__main__":
    app.run(debug=True)
