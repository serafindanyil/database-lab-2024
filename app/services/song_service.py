from app.dao.song_dao import song_dao

class SongService:
    @staticmethod
    def get_all_songs():
        return song_dao.get_all()

    @staticmethod
    def get_song_by_id(song_id):
        return song_dao.get_by_id(song_id)

    @staticmethod
    def create_song(data):
        return song_dao.create(data)

    @staticmethod
    def update_song(song_id, data):
        return song_dao.update(song_id, data)

    @staticmethod
    def delete_song(song_id):
        return song_dao.delete(song_id)
