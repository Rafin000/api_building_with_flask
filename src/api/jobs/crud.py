from src.api.jobs.models import Job
from src import db
from sqlalchemy.exc import SQLAlchemyError


def get_all_jobs_by_user_id(user_id):
    return Job.query.filter_by(user_id=user_id).order_by(Job.start_date.desc()).all()


def get_current_job_by_user_id(user_id):
    response_object = {}
    current_job = Job.query.filter_by(user_id=user_id, end_date=None).first()
    if not current_job:
        response_object['message'] = f"No current Job for User {user_id}"
        return response_object, 404
    return current_job


def get_job_by_title_company_start_date(title, company, start_date, user_id):
    return Job.query.filter_by(title=title,company=company,start_date=start_date, user_id=user_id).first()


def update_job_end_date(end_date, user_id):
    print("Im in update")
    try:
        job = Job.query.filter_by(end_date = None, user_id = user_id).first()
        print("current job", job)
        if job and job.end_date is None:
            job.end_date = end_date
            db.session.commit()
            print("my update done")
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
    
    


