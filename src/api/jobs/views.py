from datetime import datetime
from flask import request
from flask_restx import Namespace, fields, Resource
from src.api.jobs.crud import add_job, get_all_jobs_by_user_id, get_current_job_by_user_id, get_job_by_title_company_start_date, update_job_end_date
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
    @jobs_namespace.expect(job, validate=True)
    def post(self,user_id):
        """Creates a new job of a user."""
        post_data = request.get_json()
        title = post_data.get('title')
        company = post_data.get('company')
        str_start_date = post_data.get('start_date')
        str_end_date = post_data.get('end_date') 
        response_object = {}

        start_date = datetime.strptime(str_start_date, '%Y-%m-%d').date()
        if str_end_date is not None:
            end_date = datetime.strptime(str_end_date, '%Y-%m-%d').date()
        else:
            end_date = None
        user = get_user_by_id(user_id=user_id)
        if not user:
            response_object['message'] = 'Sorry. That user does not exists.'
            return response_object, 400
        
        if get_job_by_title_company_start_date(title=title, company=company, start_date=start_date):
            response_object['message'] = 'There already exist job with same name and company and start date for this user'
            return response_object, 400
        
        if end_date is not None and start_date > end_date:
            response_object['message'] = 'Start date cant be greater than End date'
            return response_object, 400
        
        if end_date is None:
            update_job_end_date(end_date=start_date)

        add_job(title=title, company=company, user_id=user_id, start_date=start_date, end_date=end_date)
        response_object['message'] = f'Job {title} was added for user with id {user_id}!'
        return response_object, 201

    

class CurrentJob(Resource):
    @jobs_namespace.marshal_with(job, as_list=True)
    def get(self, user_id):
        """Returns current job of a user."""  
        user = get_user_by_id(user_id=user_id)
        response_object = {}

        if not user:
            response_object['message'] = 'Sorry. That user does not exists.'
            return response_object, 400
        
        current_job = get_current_job_by_user_id(user_id)
        if not current_job:
            jobs_namespace.abort(404, f"User {user_id} has no current job") 

        return current_job, 200



class JobList(Resource):
    @jobs_namespace.marshal_with(job, as_list=True)
    def get(self, user_id):
        """get all jobs of a user"""
        response_object = {}
        user = get_user_by_id(user_id=user_id)
        if not user:
            response_object['message'] = 'Sorry. That user does not exists.'
            return response_object, 400
        
        return get_all_jobs_by_user_id(user_id), 200
    


jobs_namespace.add_resource(Jobs, "/<int:user_id>")    
jobs_namespace.add_resource(CurrentJob, "/current/<int:user_id>")    
jobs_namespace.add_resource(JobList, "/history/<int:user_id>")    



