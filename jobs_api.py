from flask import Blueprint, jsonify, request
from data import db_session, jobs, users
Jobs = jobs.Jobs
User = users.User


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


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).filter(User.id == request.json['team_leader']).first() is None:
        return jsonify({'error': 'Bad request (Incorrect teamlider`s id)'})
    for col_id in [int(i) for i in request.json['collaborators'] if i.isdigit()]:
        if session.query(users.User).filter(users.User.id == col_id).first() is None:
            return jsonify({'error': 'Bad request (Incorrect collaborators` id)'})
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
    )
    if all(key in request.json for key in ['start_date', 'end_date']):
        jobs.start_date = request.json['start_date']
        jobs.end_date = request.json['end_date']

    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    if session.query(User).filter(User.id == request.json['team_leader']).first() is None:
        return jsonify({'error': 'Bad request (Incorrect teamlider`s id)'})
    for col_id in [int(i) for i in request.json['collaborators'] if i.isdigit()]:
        if session.query(users.User).filter(users.User.id == col_id).first() is None:
            return jsonify({'error': 'Bad request (Incorrect collaborators` id)'})
    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    if all(key in request.json for key in ['start_date', 'end_date']):
        job.start_date = request.json['start_date']
        job.end_date = request.json['end_date']

    session.commit()
    return jsonify({'success': 'OK'})
