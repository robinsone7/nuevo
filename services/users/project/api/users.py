# services/users/project/api/users.py

from flask import Blueprint, jsonify, request
from project import db
from project.api.models import User
from sqlalchemy import exc

users_blueprint = Blueprint('users',__name__)

@users_blueprint.route('/users/ping', methods=['GET'])


def ping_pong():
        return jsonify({
                'status': 'success',
                'message': 'pong!'
                })

@users_blueprint.route('/users', methods=['POST'])

def add_user():
        post_data = request.get_json()
        response_object={
                'status': 'falló',
                'message': 'Carga invalida'
        }
        if not post_data:
                return jsonify(response_object), 400

        username = post_data.get('username')
        email = post_data.get('email')
        try:
                user = User.query.filter_by(email=email).first()
                if not user:
                        db.session.add(User(username=username, email=email))
                        db.session.commit()
                        response_object['status'] = 'success',
                        response_object['message'] = f'{email} ha sido agregado'
                        return jsonify(response_object), 201
                else:
                        response_object['message'] = 'Lo siento. EL email ya exite'
                        return jsonify(response_object), 400
        except exc.IntegrityError:
                db.session.rollback()
                return jsonify(response_object), 400



@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obtener detalles de usuario único """
    response_object = {
        'estado': 'fallo',
        'mensaje': 'El usuario no existe'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Obteniendo todos los usuarios"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200
