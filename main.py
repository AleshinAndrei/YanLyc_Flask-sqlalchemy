from data import db_session, users, jobs
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


db_session.global_init("db/mars.sqlite")
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        print("checking")
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            print("ok")
            return redirect("/")
        print("not ok")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Не Авторизация', form=form)


if __name__ == '__main__':
    app.run()


