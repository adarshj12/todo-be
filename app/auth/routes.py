from flask import Blueprint,make_response,request
from app.models import db,User
from werkzeug.security import generate_password_hash, check_password_hash
from app.middlewares.verifyToken import create_token


auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.json
    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return make_response({
            "message":"Required credentials were not provided"
        },401)
    hashed_password = generate_password_hash(data['password'])
    user = User(
        name = data['name'],
        email=data['email'],
        password = hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return make_response({"msg": "User registered"}, 201)

@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return make_response({
            "message":"Required credentials were not provided"
        },401)
    user = User.query.filter_by(email=data.get("email")).first()
    if not user:
        return make_response({
            "message":"Please create an account"
        },401)
    if check_password_hash(user.password,data.get('password')):
        token = create_token(user)
        return make_response({'token':token},200)
    return make_response({
        "message":"Please check your credentials"
    },401)