from flask import request
from flask_restx import Namespace, fields, Resource
from src.api.decorators import token_required
from src.api.jobs.crud import add_job, get_all_jobs_by_user_id, get_current_job_by_user_id, get_job_by_title_company_start_date, update_job_end_date
from src.api.jobs.helpers import convert_string_to_date, is_valid_start_and_end_date
from src.api.jobs.models import Job
from src.api.users.crud import get_user_by_id

jobs_namespace = Namespace("jobs")

job = jobs_namespace.model('Job', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True),
    'company': fields.String(required=True),
    'user_id': fields.String,
    'start_date': fields.String(required=True),
    'end_date': fields.String,
})


class Jobs(Resource):
    @token_required
    @jobs_namespace.expect(job, validate=True)
    def post(self, payload):

        """Creates a new job of a user."""

        user_id = payload['user_id']
        if not user_id:
            jobs_namespace.abort(404, 'User ID not found in token')
        
        post_data = request.get_json()
        title = post_data.get('title')
        company = post_data.get('company')
        start_date,end_date = convert_string_to_date(post_data.get('start_date'),post_data.get('end_date') )

        user = get_user_by_id(user_id=user_id)
        if not user:
            jobs_namespace.abort(400, 'Sorry. That user does not exist.')
        
        if get_job_by_title_company_start_date(title=title, company=company, start_date=start_date, user_id=user_id):
            jobs_namespace.abort(400, 'There already exist job with same name and company and start date for this user')

        if is_valid_start_and_end_date(start_date=start_date,end_date=end_date,user_id=user_id): 
            add_job(title=title, company=company, user_id=user_id, start_date=start_date, end_date=end_date)
            return {'message' : f'Job {title} was added for user with id {user_id}!'}, 201
    

class CurrentJob(Resource):
    @token_required
    @jobs_namespace.marshal_with(job, as_list=True)
    def get(self,payload):

        """Returns current job of the authenticated user."""

        user_id = payload['user_id']
        if not user_id:
            jobs_namespace.abort(404, 'User ID not found in token')
        
        user = get_user_by_id(user_id)
        if not user:
            jobs_namespace.abort(400, 'Sorry. That user does not exist.')
        
        current_job = get_current_job_by_user_id(user_id)
        if not current_job:
            jobs_namespace.abort(404, f"User {user_id} has no current job") 

        return current_job, 200



class JobList(Resource):
    @token_required
    @jobs_namespace.marshal_with(job, as_list=True)
    def get(self, payload):

        """get all jobs of a user"""

        user_id = payload['user_id']
        if not user_id:
            jobs_namespace.abort(404, 'User ID not found in token')
        
        user = get_user_by_id(user_id=user_id)
        if not user:
            jobs_namespace.abort(400, 'Sorry. That user does not exist.')

        return get_all_jobs_by_user_id(user_id), 200



jobs_namespace.add_resource(Jobs, "/")    
jobs_namespace.add_resource(CurrentJob, "/current")    
jobs_namespace.add_resource(JobList, "/history")    



