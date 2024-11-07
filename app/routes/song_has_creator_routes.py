from flask import Blueprint, request, jsonify
from app.services.song_has_creator_service import SongHasCreatorService

bp = Blueprint('song_has_creator', __name__, url_prefix='/song_creators')

@bp.route('/', methods=['POST'])
def add_creator_to_song():
    data = request.get_json()
    result = SongHasCreatorService.add_creator_to_song(data['song_id'], data['creator_id'])
    return jsonify({'message': 'Creator added to song'}), 201

@bp.route('/', methods=['DELETE'])
def remove_creator_from_song():
    data = request.get_json()
    result = SongHasCreatorService.remove_creator_from_song(data['song_id'], data['creator_id'])
    if not result:
        return jsonify({'message': 'Creator or Song not found'}), 404
    return jsonify({'message': 'Creator removed from song'})
