from flask import Blueprint, request, jsonify
from app.services.profile_creator_service import ProfileCreatorService

bp = Blueprint('profile_creator', __name__, url_prefix='/profile_creators')

@bp.route('/', methods=['GET'])
def get_profile_creators():
    profiles = ProfileCreatorService.get_all_profiles()
    return jsonify(profiles)

@bp.route('/<int:profile_id>', methods=['GET'])
def get_profile_creator(profile_id):
    profile = ProfileCreatorService.get_profile_by_id(profile_id)
    if not profile:
        return jsonify({'message': 'Profile Creator not found'}), 404
    return jsonify(profile)

@bp.route('/', methods=['POST'])
def create_profile_creator():
    data = request.get_json()
    profile = ProfileCreatorService.create_profile(data)
    return jsonify(profile), 201

@bp.route('/<int:profile_id>', methods=['PUT'])
def update_profile_creator(profile_id):
    data = request.get_json()
    profile = ProfileCreatorService.update_profile(profile_id, data)
    if not profile:
        return jsonify({'message': 'Profile Creator not found'}), 404
    return jsonify(profile)

@bp.route('/<int:profile_id>', methods=['DELETE'])
def delete_profile_creator(profile_id):
    result = ProfileCreatorService.delete_profile(profile_id)
    if not result:
        return jsonify({'message': 'Profile Creator not found'}), 404
    return jsonify({'message': 'Profile Creator deleted successfully'})
