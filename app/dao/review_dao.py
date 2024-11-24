from app import db
from sqlalchemy import text


class review_dao:
    @staticmethod
    def insert_review(song_id, user_id, content, rating):
        try:
            query = text("CALL insert_review(:song_id, :user_id, :content, :rating)")
            db.session.execute(query, {
                'song_id': song_id,
                'user_id': user_id,
                'content': content,
                'rating': rating
            })
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to insert review: {e}")

    @staticmethod
    def insert_user_song_connection(user_name, song_name):
        try:
            query = text("CALL insert_user_song_connection(:user_name, :song_name)")
            db.session.execute(query, {
                'user_name': user_name,
                'song_name': song_name
            })
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to insert user-song connection: {e}")

    @staticmethod
    def insert_multiple_reviews(song_id, user_id):
        try:
            query = text("CALL insert_multiple_reviews(:song_id, :user_id)")
            db.session.execute(query, {
                'song_id': song_id,
                'user_id': user_id
            })
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to insert multiple reviews: {e}")

    @staticmethod
    def calculate_column_stat(table_name, column_name, operation):
        try:
            # Створюємо SQL-запит для виклику збереженої процедури
            query = text("""
                    CALL calculate_column_stat_proc(:table_name, :column_name, :operation, @result);
                """)

            # Виконання запиту для виклику процедури
            db.session.execute(query, {
                'table_name': table_name,
                'column_name': column_name,
                'operation': operation
            })
            db.session.commit()  # Фіксуємо зміни після виклику процедури

            # Виконання другого запиту для отримання результату
            result_query = text("SELECT @result AS result;")
            result = db.session.execute(result_query).fetchone()

            # Повертаємо результат (доступ до кортежу за індексом)
            return result[0] if result else None
        except Exception as e:
            db.session.rollback()  # Виконати rollback у разі помилки
            raise RuntimeError(f"Failed to calculate column stat: {str(e)}")

    @staticmethod
    def distribute_reviews_to_random_tables():
        try:
            query = text("CALL distribute_reviews_to_random_tables()")
            db.session.execute(query)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to distribute reviews to random tables: {e}")
