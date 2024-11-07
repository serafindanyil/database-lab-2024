from flask import Blueprint, request, jsonify
from app.services.album_service import AlbumService

bp = Blueprint('album', __name__, url_prefix='/albums')

@bp.route('/', methods=['GET'])
def get_albums():
    albums = AlbumService.get_all_albums()
    return jsonify(albums)

@bp.route('/<int:album_id>', methods=['GET'])
def get_album(album_id):
    album = AlbumService.get_album_by_id(album_id)
    if not album:
        return jsonify({'message': 'Album not found'}), 404
    return jsonify(album)

@bp.route('/', methods=['POST'])
def create_album():
    data = request.get_json()
    album = AlbumService.create_album(data)
    return jsonify(album), 201

@bp.route('/<int:album_id>', methods=['PUT'])
def update_album(album_id):
    data = request.get_json()
    album = AlbumService.update_album(album_id, data)
    if not album:
        return jsonify({'message': 'Album not found'}), 404
    return jsonify(album)

@bp.route('/<int:album_id>', methods=['DELETE'])
def delete_album(album_id):
    result = AlbumService.delete_album(album_id)
    if not result:
        return jsonify({'message': 'Album not found'}), 404
    return jsonify({'message': 'Album deleted successfully'})
