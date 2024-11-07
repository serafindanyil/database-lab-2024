from flask import Blueprint, request, jsonify
from app.services.subcription_service import SubcriptionService

bp = Blueprint('subcription', __name__, url_prefix='/subcriptions')

@bp.route('/', methods=['GET'])
def get_subcriptions():
    subcriptions = SubcriptionService.get_all_subcriptions()
    return jsonify(subcriptions)

@bp.route('/<int:subcription_id>', methods=['GET'])
def get_subcription(subcription_id):
    subcription = SubcriptionService.get_subcription_by_id(subcription_id)
    if not subcription:
        return jsonify({'message': 'Subcription not found'}), 404
    return jsonify(subcription)

@bp.route('/', methods=['POST'])
def create_subcription():
    data = request.get_json()
    subcription = SubcriptionService.create_subcription(data)
    return jsonify(subcription), 201

@bp.route('/<int:subcription_id>', methods=['PUT'])
def update_subcription(subcription_id):
    data = request.get_json()
    subcription = SubcriptionService.update_subcription(subcription_id, data)
    if not subcription:
        return jsonify({'message': 'Subcription not found'}), 404
    return jsonify(subcription)

@bp.route('/<int:subcription_id>', methods=['DELETE'])
def delete_subcription(subcription_id):
    result = SubcriptionService.delete_subcription(subcription_id)
    if not result:
        return jsonify({'message': 'Subcription not found'}), 404
    return jsonify({'message': 'Subcription deleted successfully'})
