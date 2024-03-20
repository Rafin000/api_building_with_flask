from flask import request
from flask_restx import Namespace, Resource, fields

from src.api.auth.helpers import authenticate_user, generate_token

auth_namespace = Namespace("auth") 

auth = auth_namespace.model('Auth', {
    'username': fields.String(required=True),
    'password': fields.String(required=True), 
})
class Login(Resource):
    @auth_namespace.expect(auth, validate=True)
    def post(self):
        """Login"""
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        user = authenticate_user(username, password)
        if not user:
            return {'message': 'Authentication failed'}, 401
        token = generate_token(user.id)
        return {'token': token}, 200

auth_namespace.add_resource(Login, "")