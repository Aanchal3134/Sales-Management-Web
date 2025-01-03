from database import db
from models import Sale, Product, User, Region, Team


from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from models import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'user_id': user.user_id, 'username': user.username, 'email': user.email, 'role': user.role} for user in users])

@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='bcrypt')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User added successfully!"}, 201
