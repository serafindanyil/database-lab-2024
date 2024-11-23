from flask import Blueprint, request, jsonify
from app.services.authorization_service import AuthorizationService

bp = Blueprint('authorization', __name__, url_prefix='/authorization')

@bp.route('/', methods=['GET'])
def get_authorizations():
    authorizations = AuthorizationService.get_all_authorizations()
    return jsonify(authorizations)

@bp.route('/<int:auth_id>', methods=['GET'])
def get_authorization(auth_id):
    authorization = AuthorizationService.get_authorization_by_id(auth_id)
    if not authorization:
        return jsonify({'message': 'Authorization not found'}), 404
    return jsonify(authorization)

@bp.route('/', methods=['POST'])
def create_authorization():
    data = request.get_json()
    authorization = AuthorizationService.create_authorization(data)
    return jsonify(authorization), 201

@bp.route('/<int:auth_id>', methods=['PUT'])
def update_authorization(auth_id):
    data = request.get_json()
    authorization = AuthorizationService.update_authorization(auth_id, data)
    if not authorization:
        return jsonify({'message': 'Authorization not found'}), 404
    return jsonify(authorization)

@bp.route('/<int:auth_id>', methods=['DELETE'])
def delete_authorization(auth_id):
    result = AuthorizationService.delete_authorization(auth_id)
    if not result:
        return jsonify({'message': 'Authorization not found'}), 404
    return jsonify({'message': 'Authorization deleted successfully'})

