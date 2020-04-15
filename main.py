from data import db_session, users, jobs
from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def main():
    db_session.global_init("db/mars.sqlite")
    session = db_session.create_session()
    jobs_data = []

    for job in session.query(jobs.Jobs).all():
        team_leader = session.query(users.User).filter(users.User.id == job.team_leader).first()
        is_finised = "Is finished" if job.is_finished else "Is not finished"
        jobs_data.append([
            job.job,
            team_leader.surname + " " + team_leader.name,
            str(job.work_size) + " hours",
            job.collaborators,
            is_finised
        ])

    return render_template('job_journals.html', jobs_data=jobs_data)


if __name__ == '__main__':
    app.run()


