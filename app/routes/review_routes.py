from flask import Blueprint, request, jsonify
from app.services.review_service import ReviewService
import logging

bp = Blueprint('review', __name__, url_prefix='/review')


# Вставка нового відгуку
@bp.route('/', methods=['POST'])
def insert_review():
    data = request.get_json()
    ReviewService.insert_review(
        data['song_id'],
        data['user_id'],
        data['content'],
        data['rating']
    )
    return jsonify({'message': 'Review inserted successfully!'}), 201


# Вставка зв'язку між користувачем і піснею
@bp.route('/song', methods=['POST'])
def insert_user_song_connection():
    data = request.get_json()
    ReviewService.insert_user_song_connection(
        data['user_name'],
        data['song_name']
    )
    return jsonify({'message': 'User-song connection created!'}), 201


# Вставка 10 записів у таблицю `review`
@bp.route('/batch', methods=['POST'])
def insert_multiple_reviews():
    data = request.get_json()
    ReviewService.insert_multiple_reviews(
        data['song_id'],
        data['user_id']
    )
    return jsonify({'message': '10 reviews inserted successfully!'}), 201


@bp.route('/stat', methods=['GET'])
def calculate_column_stat():
    try:
        # Отримуємо параметри з запиту
        table_name = request.args.get('table_name')
        column_name = request.args.get('column_name')
        operation = request.args.get('operation')

        # Перевірка наявності всіх параметрів
        if not table_name or not column_name or not operation:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Викликаємо сервіс для обчислення статистики
        result = ReviewService.calculate_column_stat(table_name, column_name, operation)

        # Якщо результат відсутній, повертаємо помилку
        if result is None:
            return jsonify({'error': 'Calculation failed or no data found'}), 404

        # Повертаємо результат користувачу
        return jsonify({'result': result}), 200

    except Exception as e:
        # Обробка непередбачених помилок
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


# Розподіл даних по випадковим таблицям
@bp.route('/distribute', methods=['POST'])
def distribute_reviews_to_random_tables():
    ReviewService.distribute_reviews_to_random_tables()
    return jsonify({'message': 'Reviews distributed into random tables!'}), 201
