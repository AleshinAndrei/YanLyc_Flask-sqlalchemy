from data import db_session, users, jobs
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.sqlite")
    session = db_session.create_session()

    user = users.User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap12345"

    session.add(user)
    session.commit()

    app.run()


if __name__ == '__main__':
    main()


