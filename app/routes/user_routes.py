from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify(users)


@bp.route('/download', methods=['GET'])
def get_download():
    users = UserService.get_download()
    return jsonify(users)


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserService.create_user(data)
    return jsonify(user), 201


@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = UserService.update_user(user_id, data)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserService.delete_user(user_id)
    if not result:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'})
