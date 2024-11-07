from app.dao.genre_dao import genre_dao

class GenreService:
    @staticmethod
    def get_all_genres():
        return genre_dao.get_all()

    @staticmethod
    def get_genre_by_id(genre_id):
        return genre_dao.get_by_id(genre_id)

    @staticmethod
    def create_genre(data):
        return genre_dao.create(data)

    @staticmethod
    def update_genre(genre_id, data):
        return genre_dao.update(genre_id, data)

    @staticmethod
    def delete_genre(genre_id):
        return genre_dao.delete(genre_id)
