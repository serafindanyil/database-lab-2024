from app.dao.review_dao import review_dao


class ReviewService:
    @staticmethod
    def insert_review(song_id, user_id, content, rating):
        return review_dao.insert_review(song_id, user_id, content, rating)

    @staticmethod
    def insert_user_song_connection(user_name, song_name):
        return review_dao.insert_user_song_connection(user_name, song_name)

    @staticmethod
    def insert_multiple_reviews(song_id, user_id):
        return review_dao.insert_multiple_reviews(song_id, user_id)

    @staticmethod
    def calculate_column_stat(table_name, column_name, operation):
        return review_dao.calculate_column_stat(table_name, column_name, operation)

    @staticmethod
    def distribute_reviews_to_random_tables():
        return review_dao.distribute_reviews_to_random_tables()
