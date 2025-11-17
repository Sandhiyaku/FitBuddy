from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'])
    role = data['role']

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(name=name, email=email, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully"}), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
    identity=str(user.id),
    additional_claims={"role": user.role}
)
    return jsonify({"token": token, "role": user.role, "name": user.name})

