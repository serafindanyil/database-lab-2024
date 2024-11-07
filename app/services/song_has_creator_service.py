from app.dao.song_has_creator_dao import song_has_creator_dao

class SongHasCreatorService:
    @staticmethod
    def add_creator_to_song(song_id, creator_id):
        return song_has_creator_dao.create(song_id, creator_id)

    @staticmethod
    def remove_creator_from_song(song_id, creator_id):
        return song_has_creator_dao.delete(song_id, creator_id)
