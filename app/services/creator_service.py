from app.dao.creator_dao import creator_dao

class CreatorService:
    @staticmethod
    def get_all_creators():
        return creator_dao.get_all()

    @staticmethod
    def get_creator_by_id(creator_id):
        return creator_dao.get_by_id(creator_id)

    @staticmethod
    def create_creator(data):
        return creator_dao.create(data)

    @staticmethod
    def update_creator(creator_id, data):
        return creator_dao.update(creator_id, data)

    @staticmethod
    def delete_creator(creator_id):
        return creator_dao.delete(creator_id)
