from app.dao.authorization_dao import authorization_dao


class AuthorizationService:
    @staticmethod
    def get_all_authorizations():
        return authorization_dao.get_all()

    @staticmethod
    def get_authorization_by_id(auth_id):
        return authorization_dao.get_by_id(auth_id)

    @staticmethod
    def create_authorization(data):
        required_fields = {"email", "password"}
        missing = required_fields - data.keys()
        if missing:
            field_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required fields: {field_list}")
        return authorization_dao.create(data)

    @staticmethod
    def update_authorization(auth_id, data):
        return authorization_dao.update(auth_id, data)

    @staticmethod
    def delete_authorization(auth_id):
        return authorization_dao.delete(auth_id)
