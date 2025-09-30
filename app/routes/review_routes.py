from flask import Blueprint, request, jsonify
from app.services.review_service import ReviewService

bp = Blueprint('review', __name__, url_prefix='/review')


@bp.route('/', methods=['POST'])
def insert_review():
    data = request.get_json()
    # ОНОВЛЕНО: Валідація
    required_fields = ['song_id', 'user_id', 'content', 'rating']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400

    try:
        ReviewService.insert_review(
            data['song_id'], data['user_id'], data['content'], data['rating']
        )
        return jsonify({'message': 'Review inserted successfully!'}), 201
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ... (інші роути з процедурами залишаються, але варто додати валідацію)

@bp.route('/song', methods=['POST'])
def insert_user_song_connection():
    data = request.get_json()
    if not data or 'user_name' not in data or 'song_name' not in data:
        return jsonify({'error': 'user_name and song_name are required'}), 400

    try:
        ReviewService.insert_user_song_connection(data['user_name'], data['song_name'])
        return jsonify({'message': 'User-song connection created!'}), 201
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ... і так далі для решти роутів