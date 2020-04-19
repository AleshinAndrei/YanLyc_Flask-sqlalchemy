from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, users, jobs
import job_argparser
User = users.User
Jobs = jobs.Jobs


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict()})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict() for item in jobs]})

    def post(self):
        args = job_argparser.parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.id == args['team_leader']).first() is None:
            return jsonify({'error': 'Bad request (Incorrect teamlider`s id)'})
        for col_id in [int(i) for i in args['collaborators'] if i.isdigit()]:
            if session.query(users.User).filter(users.User.id == col_id).first() is None:
                return jsonify({'error': 'Bad request (Incorrect collaborators` id)'})
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
        )
        if all(map(lambda key: key in args, ['start_date', 'end_date'])):
            jobs.start_date = args['start_date']
            jobs.end_date = args['end_date']
        try:
            session.add(job)
        except Exception as error:
            print(error)
        session.commit()
        return jsonify({'success': 'OK'})
