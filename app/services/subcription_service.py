from app.dao.subcription_dao import subcription_dao

class SubcriptionService:
    @staticmethod
    def get_all_subcriptions():
        return subcription_dao.get_all()

    @staticmethod
    def get_subcription_by_id(subcription_id):
        return subcription_dao.get_by_id(subcription_id)

    @staticmethod
    def create_subcription(data):
        return subcription_dao.create(data)

    @staticmethod
    def update_subcription(subcription_id, data):
        return subcription_dao.update(subcription_id, data)

    @staticmethod
    def delete_subcription(subcription_id):
        return subcription_dao.delete(subcription_id)
