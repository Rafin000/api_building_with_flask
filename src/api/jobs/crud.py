from src.api.jobs.models import Job
from src import db
from sqlalchemy.exc import SQLAlchemyError


def get_all_jobs_by_user_id(user_id):
    jobs = Job.query.filter_by(user_id=user_id).order_by(Job.start_date.desc()).all()
    job_history = []
    for job in jobs:
        job_history.append(job)
    return job_history


def get_current_job_by_user_id(user_id):
    response_object = {}
    current_job = Job.query.filter_by(user_id=user_id, end_date=None).first()
    if not current_job:
        response_object['message'] = f"No current Job for User {user_id}"
        return response_object, 404
    return current_job


def get_job_by_title_company_start_date(title, company, start_date, user_id):
    return Job.query.filter_by(title=title,company=company,start_date=start_date, user_id=user_id).first()


def update_job_end_date(end_date):
    try:
        job = Job.query.filter_by(end_date = None).first()
        if job and job.end_date is None:
            job.end_date = end_date
            db.session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        print(f"Failed to update end date for job that is currenly Null: {e}")
        db.session.rollback()
        return False


def add_job(title, company, user_id, start_date, end_date):
    response_object = {}
    try:
        job = Job(title=title, company=company,user_id=user_id,start_date=start_date,end_date=end_date)
        db.session.add(job)
        db.session.commit()
        db.session.close()
    except SQLAlchemyError as e:
        response_object['message'] = f'Failed to add the Job! {e}'
        return response_object, 500
    
    
#         if end_year:
#             jobs = get_all_job_by_user_id(user_id=user_id)
#             temp_job= JobModel(title=title, company=company, start_year=start_year, end_year=end_year, user_id=user_id)
#             jobs.append(temp_job)
#             sorted_jobs = sorted(jobs, key=lambda x: x.start_year)
#             flag = False
#             time = sorted_jobs[0].end_year
#             conflict_company= None
#             for j in sorted_jobs[1::]:
#                 #print(f"Job ID: {j.id}, Title: {j.title}, Company: {j.company}, Start Year: {j.start_year}, End Year: {j.end_year}, User ID: {j.user_id}")
#                 if time > j.start_year:
#                     flag = True
#                     conflict_company= j.company
#                     break
#                 time = j.end_year
#             if  flag:
#                 response['message'] = f'during this time you were woring with {conflict_company}' 
#                 return response, 400
            
#         if not end_year:
#             last_job = get_job_by_user_id_start_year_desc(user_id=user_id)
#             if last_job and last_job.end_year and  last_job.end_year > start_year:
#                 response['message'] = f'your starting time clash with recent job {last_job.company}' 
#                 return response, 400
#             elif  last_job and not last_job.end_year:
#                 response['message'] = f'give end_year to your last job' 
#                 return response, 400


