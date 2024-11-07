from flask import Blueprint, request, jsonify
from app.services.label_service import LabelService

bp = Blueprint('label', __name__, url_prefix='/labels')

@bp.route('/', methods=['GET'])
def get_labels():
    labels = LabelService.get_all_labels()
    return jsonify(labels)

@bp.route('/<int:label_id>', methods=['GET'])
def get_label(label_id):
    label = LabelService.get_label_by_id(label_id)
    if not label:
        return jsonify({'message': 'Label not found'}), 404
    return jsonify(label)

@bp.route('/', methods=['POST'])
def create_label():
    data = request.get_json()
    label = LabelService.create_label(data)
    return jsonify(label), 201

@bp.route('/<int:label_id>', methods=['PUT'])
def update_label(label_id):
    data = request.get_json()
    label = LabelService.update_label(label_id, data)
    if not label:
        return jsonify({'message': 'Label not found'}), 404
    return jsonify(label)

@bp.route('/<int:label_id>', methods=['DELETE'])
def delete_label(label_id):
    result = LabelService.delete_label(label_id)
    if not result:
        return jsonify({'message': 'Label not found'}), 404
    return jsonify({'message': 'Label deleted successfully'})
