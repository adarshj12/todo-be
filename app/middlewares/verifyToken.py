import jwt
from datetime import datetime, timedelta
from flask import request, make_response
from functools import wraps
from app.models import User,db
import os
from dotenv import load_dotenv

load_dotenv()

def create_token(user):
    payload = {
        "userId": str(user.id),
        "username":user.name,
        "email":user.email,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm="HS256")

def verify_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return make_response({"msg": "Missing or invalid token"}, 401)

        token = auth.split(" ")[1]
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
            user_id = payload["sub"]
            user = db.session.get(User, user_id)
            if not user:
                raise Exception("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return make_response({"msg": "Token expired"}, 401)
        except Exception as e:
            return make_response({"msg": f"Invalid token: {str(e)}"}, 401)

    return wrapper