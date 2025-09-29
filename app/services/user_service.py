from app.dao.user_dao import user_dao

class UserService:
    @staticmethod
    def get_all_users():
        return user_dao.get_all()

    @staticmethod
    def get_download():
        return user_dao.get_download()

    @staticmethod
    def get_user_by_id(user_id):
        return user_dao.get_by_id(user_id)

    @staticmethod
    def create_user(data):
        return user_dao.create(data)

    @staticmethod
    def update_user(user_id, data):
        return user_dao.update(user_id, data)

    @staticmethod
    def delete_user(user_id):
        return user_dao.delete(user_id)



