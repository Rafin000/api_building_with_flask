from flask_restx import Api
  
from src.api.users.views import users_namespace  
from src.api.jobs.views import jobs_namespace
from src.api.auth.views import auth_namespace

api = Api(prefix="/api")


api.add_namespace(users_namespace, path="/users")  
api.add_namespace(jobs_namespace, path="/jobs") 
api.add_namespace(auth_namespace, path="/login") 