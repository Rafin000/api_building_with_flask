from functools import wraps
from flask import request

from src.api.auth.helpers import verify_token



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            payload = verify_token(token)
        except:
            return {'message': 'Invalid token'}, 401

        return f(payload=payload, *args, **kwargs)

    return decorated
