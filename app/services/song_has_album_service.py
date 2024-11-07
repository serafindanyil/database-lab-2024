from app.dao.song_has_album_dao import song_has_album_dao

class SongHasAlbumService:
    @staticmethod
    def add_song_to_album(song_id, album_id):
        return song_has_album_dao.create(song_id, album_id)

    @staticmethod
    def remove_song_from_album(song_id, album_id):
        return song_has_album_dao.delete(song_id, album_id)
