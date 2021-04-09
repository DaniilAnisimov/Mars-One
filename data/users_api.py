import flask
from flask import jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age',
                                    'position', 'speciality', 'address',
                                    'email', 'modified_date', 'city_from')) for item in users]
        }
    )


@blueprint.route('/api/users/<string:users_id>', methods=['GET'])
def get_one_users(users_id):
    db_sess = db_session.create_session()
    if not users_id.isdigit():
        return jsonify({'error': 'Instead of the ID, the string is received'})
    else:
        users_id = int(users_id)
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': users.to_dict(only=('id', 'surname', 'name', 'age',
                                        'position', 'speciality', 'address',
                                        'email', 'modified_date', 'city_from'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    rjs = request.json
    if not rjs:
        return jsonify({'error': 'Empty request'})
    elif not all(key in rjs for key in
                 ['id', 'surname', 'name', 'age',
                  'position', 'speciality', 'address', "password",
                  'email', 'city_from']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == rjs["id"]).first()
    if users:
        return jsonify({'error': 'Id already exists'})
    user = User(id=rjs['id'], surname=rjs['surname'], name=rjs['name'],
                age=rjs['age'], position=rjs['position'], speciality=rjs['speciality'],
                address=rjs['address'], email=rjs['email'], city_from=rjs['city_from'])
    user.set_password(rjs["password"])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# Принимает несколько ключей таблицы Jobs
@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def change_user(user_id):
    rjs = request.json
    keys = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password', 'city_from']
    if not rjs:
        return jsonify({'error': 'Empty request'})
    elif not all(key in keys for key in rjs):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user is None:
        return jsonify({'error': 'Id already exists'})
    for key, value in rjs.items():
        if key == "surname":
            user.surname = value
        elif key == "name":
            user.name = value
        elif key == "age":
            user.age = value
        elif key == "position":
            user.position = value
        elif key == "speciality":
            user.speciality = value
        elif key == "address":
            user.address = value
        elif key == "email":
            user.email = value
        elif key == "password":
            user.set_password(value)
        elif key == "city_from":
            user.city_from = value
    db_sess.commit()
    return jsonify({'success': 'OK'})
