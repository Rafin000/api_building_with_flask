from flask_restx import Api

from src.api.ping import ping_namespace  
from src.api.users.views import users_namespace  
from src.api.jobs.views import jobs_namespace

api = Api(prefix="/api")



api.add_namespace(ping_namespace, path="/ping")  
api.add_namespace(users_namespace, path="/users")  
api.add_namespace(jobs_namespace, path="/jobs")  