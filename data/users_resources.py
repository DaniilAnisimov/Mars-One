from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.users import User
from data.user_parser import *


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=("id", "surname", "name", "age", 'position', 'speciality', 'address',
                  "email", 'modified_date', 'city_from'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=("id", "surname", "name", "age", 'position', 'speciality', 'address',
                  "email", 'modified_date', 'city_from')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(id=args['id'], surname=args['surname'], name=args['name'],
                    age=args['age'], position=args['position'], speciality=args['speciality'],
                    address=args['address'], email=args['email'], city_from=args['city_from'])
        user.set_password(args["password"])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
