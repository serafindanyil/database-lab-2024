from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.download_model import Download
from app.models.review_model import Review
from app.models.song_model import Song
from app.models.user_model import User


class review_dao:
    @staticmethod
    def _using_mysql() -> bool:
        bind = db.session.bind
        return bool(bind and bind.dialect.name.startswith("mysql"))

    @staticmethod
    def insert_review(song_id, user_id, content, rating):
        try:
            if review_dao._using_mysql():
                query = text("CALL insert_review(:song_id, :user_id, :content, :rating)")
                db.session.execute(
                    query,
                    {
                        "song_id": song_id,
                        "user_id": user_id,
                        "content": content,
                        "rating": rating,
                    },
                )
            else:
                song = Song.query.get(song_id)
                if song is None:
                    raise ValueError("Song not found")
                user = User.query.get(user_id)
                if user is None:
                    raise ValueError("User not found")
                review = Review(
                    song_id=song.id,
                    user_id=user.id,
                    content=content,
                    rating=rating,
                )
                db.session.add(review)
            db.session.commit()
        except ValueError:
            db.session.rollback()
            raise
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RuntimeError(f"Failed to insert review: {exc}") from exc

    @staticmethod
    def insert_user_song_connection(user_name, song_name):
        try:
            if review_dao._using_mysql():
                query = text("CALL insert_user_song_connection(:user_name, :song_name)")
                db.session.execute(query, {"user_name": user_name, "song_name": song_name})
            else:
                user = (
                    User.query.filter(func.lower(User.name) == user_name.lower())
                    .order_by(User.id)
                    .first()
                )
                if user is None:
                    raise ValueError("User not found")
                song = (
                    Song.query.filter(func.lower(Song.name) == song_name.lower())
                    .order_by(Song.id)
                    .first()
                )
                if song is None:
                    raise ValueError("Song not found")
                existing = (
                    Download.query.filter_by(user_id=user.id, song_id=song.id)
                    .order_by(Download.id)
                    .first()
                )
                if existing is not None:
                    return existing
                download = Download(song_id=song.id, user_id=user.id)
                db.session.add(download)
            db.session.commit()
        except ValueError:
            db.session.rollback()
            raise
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RuntimeError(f"Failed to insert user-song connection: {exc}") from exc

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
