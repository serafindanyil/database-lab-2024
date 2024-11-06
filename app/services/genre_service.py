from app.dao.genre_dao import GenreDAO

class GenreService:
    @staticmethod
    def get_all_genres():
        return GenreDAO.get_all()

    @staticmethod
    def get_genre_by_id(genre_id):
        return GenreDAO.get_by_id(genre_id)

    @staticmethod
    def create_genre(data):
        return GenreDAO.create(data)

    @staticmethod
    def update_genre(genre_id, data):
        return GenreDAO.update(genre_id, data)

    @staticmethod
    def delete_genre(genre_id):
        return GenreDAO.delete(genre_id)
