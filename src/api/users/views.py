from flask import request
from flask_restx import Resource, fields , Namespace
from src.api.users.crud import add_user, delete_user, get_all_users, get_user_by_id, update_user, get_user_by_username
from src.api.users.crud import add_user

users_namespace = Namespace("users") 


user = users_namespace.model('User', {
    'id': fields.Integer(readOnly=True),
    'fname': fields.String(required=True),
    'lname': fields.String(required=True),
    'username': fields.String(required=True),
    'password': fields.String(required=True), 
    'created_date': fields.DateTime,
    'updated_date': fields.DateTime,
})


class UsersList(Resource):
    @users_namespace.expect(user, validate=True)
    def post(self):

        """Creates a new user."""

        post_data = request.get_json()
        fname = post_data.get('fname')
        lname = post_data.get('lname')
        username = post_data.get('username')
        password = post_data.get('password')

        user = get_user_by_username(username)  
        if user:
            users_namespace.abort(400, 'Sorry. That username already exists.')

        add_user(fname, lname, username, password) 
        return {'message' : f'{username} was added!'}, 201
    

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):

        """Returns all users.""" 

        return get_all_users(), 200  

class Users(Resource):
    @users_namespace.marshal_with(user) 
    def get(self, user_id):

        """Returns a single user.""" 

        user = get_user_by_id(user_id)  
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200
    


    @users_namespace.expect(user, validate=False)
    def put(self, user_id):

        """Updates a user."""  

        post_data = request.get_json()
        fname = post_data.get("fname")
        lname = post_data.get("lname")
        username = post_data.get("username")
        password = post_data.get("password") 

        user = get_user_by_id(user_id)  
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_username(username):
            users_namespace.abort(400, "Sorry. That username already exists.") 

        update_user(user, fname, lname, username, password)  
        return {"message": f"{user.id} was updated!"}, 200



    def delete(self, user_id):

        """Deletes a user."""  

        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        delete_user(user)       
        return {"message" : f"{user.username} was removed!"}, 200
    
    

users_namespace.add_resource(UsersList, "")  
users_namespace.add_resource(Users, "/<int:user_id>")

