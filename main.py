from data import db_session, users, jobs
from flask import Flask
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.sqlite")
    session = db_session.create_session()

    job = jobs.Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False

    session.add(job)
    session.commit()

    app.run()


if __name__ == '__main__':
    main()


