from flask import current_app
import jwt
from datetime import datetime, timedelta

from src.api.users.crud import get_user_by_username


def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {'message': "Signature has expired"}
    except jwt.InvalidTokenError:
        return {'message': "Invalid token"}



def generate_token(user_id):
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1) 
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        return e


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if not user or not user.check_password(password):
        return {'message' : "Authentication Failed"}
    return user