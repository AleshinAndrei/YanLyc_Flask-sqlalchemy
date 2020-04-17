from flask import Blueprint, jsonify
from data import db_session, users, jobs
User = users.User
Jobs = jobs.Jobs


blueprint = Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': job.to_dict()
        }
    )

