from flask import Blueprint, request, jsonify
from app.services.song_has_album_service import SongHasAlbumService

bp = Blueprint('song_has_album', __name__, url_prefix='/song_albums')

@bp.route('/', methods=['POST'])
def add_song_to_album():
    data = request.get_json()
    result = SongHasAlbumService.add_song_to_album(data['song_id'], data['album_id'])
    return jsonify({'message': 'Song added to album'}), 201

@bp.route('/', methods=['DELETE'])
def remove_song_from_album():
    data = request.get_json()
    result = SongHasAlbumService.remove_song_from_album(data['song_id'], data['album_id'])
    if not result:
        return jsonify({'message': 'Song or Album not found'}), 404
    return jsonify({'message': 'Song removed from album'})
