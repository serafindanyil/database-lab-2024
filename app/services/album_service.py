from app.dao.album_dao import album_dao

class AlbumService:
    @staticmethod
    def get_all_albums():
        return album_dao.get_all()

    @staticmethod
    def get_album_by_id(album_id):
        return album_dao.get_by_id(album_id)

    @staticmethod
    def create_album(data):
        return album_dao.create(data)

    @staticmethod
    def update_album(album_id, data):
        return album_dao.update(album_id, data)

    @staticmethod
    def delete_album(album_id):
        return album_dao.delete(album_id)
