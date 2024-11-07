from flask import Blueprint, request, jsonify
from app.services.profile_user_service import ProfileUserService

bp = Blueprint('profile_user', __name__, url_prefix='/profile_users')

@bp.route('/', methods=['GET'])
def get_profile_users():
    profiles = ProfileUserService.get_all_profiles()
    return jsonify(profiles)

@bp.route('/<int:profile_id>', methods=['GET'])
def get_profile_user(profile_id):
    profile = ProfileUserService.get_profile_by_id(profile_id)
    if not profile:
        return jsonify({'message': 'Profile User not found'}), 404
    return jsonify(profile)

@bp.route('/', methods=['POST'])
def create_profile_user():
    data = request.get_json()
    profile = ProfileUserService.create_profile(data)
    return jsonify(profile), 201

@bp.route('/<int:profile_id>', methods=['PUT'])
def update_profile_user(profile_id):
    data = request.get_json()
    profile = ProfileUserService.update_profile(profile_id, data)
    if not profile:
        return jsonify({'message': 'Profile User not found'}), 404
    return jsonify(profile)

@bp.route('/<int:profile_id>', methods=['DELETE'])
def delete_profile_user(profile_id):
    result = ProfileUserService.delete_profile(profile_id)
    if not result:
        return jsonify({'message': 'Profile User not found'}), 404
    return jsonify({'message': 'Profile User deleted successfully'})
