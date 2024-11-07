from flask import Blueprint, request, jsonify
from app.services.creator_service import CreatorService

bp = Blueprint('creator', __name__, url_prefix='/creators')

@bp.route('/', methods=['GET'])
def get_creators():
    creators = CreatorService.get_all_creators()
    return jsonify(creators)

@bp.route('/<int:creator_id>', methods=['GET'])
def get_creator(creator_id):
    creator = CreatorService.get_creator_by_id(creator_id)
    if not creator:
        return jsonify({'message': 'Creator not found'}), 404
    return jsonify(creator)

@bp.route('/', methods=['POST'])
def create_creator():
    data = request.get_json()
    creator = CreatorService.create_creator(data)
    return jsonify(creator), 201

@bp.route('/<int:creator_id>', methods=['PUT'])
def update_creator(creator_id):
    data = request.get_json()
    creator = CreatorService.update_creator(creator_id, data)
    if not creator:
        return jsonify({'message': 'Creator not found'}), 404
    return jsonify(creator)

@bp.route('/<int:creator_id>', methods=['DELETE'])
def delete_creator(creator_id):
    result = CreatorService.delete_creator(creator_id)
    if not result:
        return jsonify({'message': 'Creator not found'}), 404
    return jsonify({'message': 'Creator deleted successfully'})
