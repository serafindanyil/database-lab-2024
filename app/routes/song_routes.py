from flask import Blueprint, request, jsonify
from app.services.song_service import SongService

bp = Blueprint('song', __name__, url_prefix='/songs')

@bp.route('/', methods=['GET'])
def get_songs():
    songs = SongService.get_all_songs()
    return jsonify(songs)

@bp.route('/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = SongService.get_song_by_id(song_id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404
    return jsonify(song)

@bp.route('/', methods=['POST'])
def create_song():
    data = request.get_json()
    song = SongService.create_song(data)
    return jsonify(song), 201

@bp.route('/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()
    song = SongService.update_song(song_id, data)
    if not song:
        return jsonify({'message': 'Song not found'}), 404
    return jsonify(song)

@bp.route('/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    result = SongService.delete_song(song_id)
    if not result:
        return jsonify({'message': 'Song not found'}), 404
    return jsonify({'message': 'Song deleted successfully'})
