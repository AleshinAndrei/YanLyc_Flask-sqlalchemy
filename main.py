from data import db_session, users, jobs
from flask import Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_restful import Api
import users_resources
import jobs_resources
import jobs_api
import users_api


db_session.global_init("db/mars.sqlite")
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')
api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resources.JobResource, '/api/v2/jobs/<int:job_id>')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rep_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewJobForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    team_leader = IntegerField('Team leader id', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators')
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def main():
    db_session.global_init("db/mars.sqlite")
    session = db_session.create_session()
    all_jobs = session.query(jobs.Jobs).all()
    team_leaders = [
        session.query(users.User).filter(users.User.id == job.team_leader).first()
        for job in all_jobs
    ]

    return render_template('job_journals.html', jobs=all_jobs, team_leaders=team_leaders)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, message='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.rep_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            hashed_password=form.password.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, message='')


@app.route('/new_job', methods=['GET', 'POST'])
def new_job():
    form = NewJobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.id == form.team_leader.data).first() is None:
            return render_template('new_job.html', form=form,
                                   message="Тимлидера с таким id не существует")
        for col_id in [int(i) for i in form.collaborators.data.split(', ') if i.isdigit()]:
            if session.query(users.User).filter(users.User.id == col_id).first() is None:
                return render_template('new_job.html', form=form,
                                       message="Одного из членов команды с таким id не существует")
        job = jobs.Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('new_job.html', form=form, message='')


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    session = db_session.create_session()
    job = session.query(jobs.Jobs).filter(jobs.Jobs.id == id).first()
    form = NewJobForm(
        team_leader=job.team_leader,
        job=job.job,
        work_size=job.work_size,
        collaborators=job.collaborators,
        is_finished=job.is_finished
    )
    if form.validate_on_submit():
        if session.query(users.User).filter(users.User.id == form.team_leader.data).first() is None:
            return render_template('new_job.html', form=form,
                                   message="Тимлидера с таким id не существует")
        for col_id in [int(i) for i in form.collaborators.data.split(', ') if i.isdigit()]:
            if session.query(users.User).filter(users.User.id == col_id).first() is None:
                return render_template('new_job.html', form=form,
                                       message="Одного из членов команды с таким id не существует")

        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        session.add(job)
        session.commit()
        return redirect('/')
    elif current_user.id not in {job.team_leader, 1}:
            abort(404)
    return render_template('new_job.html', form=form, message='')


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    session = db_session.create_session()
    job = session.query(jobs.Jobs).filter(jobs.Jobs.id == id).first()

    if current_user.id in {job.team_leader, 1}:
        session.delete(job)
        session.commit()
        return redirect('/')
    return abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(debug=True)
