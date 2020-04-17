from flask import Blueprint, jsonify, request
from data import db_session, users
User = users.User


blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users': [item.to_dict() for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': user.to_dict()
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
    )

    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})

    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.hashed_password = request.json['hashed_password']
    if 'modified_date' in request.json:
        user.modified_date = request.json['modified_date']

    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})
