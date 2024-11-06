# app/routes/genre_routes.py

from flask import Blueprint, request, jsonify
from app.services.genre_service import GenreService

bp = Blueprint('genre', __name__, url_prefix='/genres')

@bp.route('/', methods=['GET'])
def get_genres():
    genres = GenreService.get_all_genres()
    return jsonify(genres)

@bp.route('/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    genre = GenreService.get_genre_by_id(genre_id)
    if not genre:
        return jsonify({'message': 'Genre not found'}), 404
    return jsonify(genre)

@bp.route('/', methods=['POST'])
def create_genre():
    data = request.get_json()
    genre = GenreService.create_genre(data)
    return jsonify(genre), 201

@bp.route('/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    data = request.get_json()
    genre = GenreService.update_genre(genre_id, data)
    if not genre:
        return jsonify({'message': 'Genre not found'}), 404
    return jsonify(genre)

@bp.route('/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    result = GenreService.delete_genre(genre_id)
    if not result:
        return jsonify({'message': 'Genre not found'}), 404
    return jsonify({'message': 'Genre deleted successfully'})
