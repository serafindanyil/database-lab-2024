from app.dao.profile_user_dao import profile_user_dao

class ProfileUserService:
    @staticmethod
    def get_all_profiles():
        return profile_user_dao.get_all()

    @staticmethod
    def get_profile_by_id(profile_id):
        return profile_user_dao.get_by_id(profile_id)

    @staticmethod
    def create_profile(data):
        return profile_user_dao.create(data)

    @staticmethod
    def update_profile(profile_id, data):
        return profile_user_dao.update(profile_id, data)

    @staticmethod
    def delete_profile(profile_id):
        return profile_user_dao.delete(profile_id)
