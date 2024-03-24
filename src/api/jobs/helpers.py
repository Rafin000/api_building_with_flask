from datetime import datetime

from flask import abort
from src.api.jobs.crud import get_all_jobs_by_user_id, update_job_end_date

def convert_string_to_date(str_start_date, str_end_date):
    start_date = datetime.strptime(str_start_date, '%Y-%m-%d').date()
    if str_end_date is not None:
        end_date = datetime.strptime(str_end_date, '%Y-%m-%d').date()
    else:
        end_date = None
    
    return (start_date,end_date)



def is_valid_start_and_end_date(start_date, end_date, user_id):
    if end_date is not None and start_date > end_date:
        abort(400, {'message': 'Start date cannot be greater than End date'})
        
    jobs = get_all_jobs_by_user_id(user_id=user_id)
    if end_date: 
        for job in jobs:
            if job.start_date and job.end_date:
                if (job.start_date < end_date and job.end_date > start_date) or (job.end_date < end_date and job.start_date > start_date):
                    abort(400, {'message': 'Conflict With Another Job'})
    else: 
        if jobs:
            last_job = jobs[0]
            if last_job.end_date is None:
                if last_job.start_date > start_date:
                    abort(400, {'message': "Your current job start date can't start before your previous current job start date"})
                else:
                    update_job_end_date(end_date=start_date, user_id=user_id)
            elif last_job.end_date > start_date:
                abort(400, {'message': "Your current job must start after your last job end year"})
    return True

