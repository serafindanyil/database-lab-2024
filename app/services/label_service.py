from app.dao.label_dao import label_dao

class LabelService:
    @staticmethod
    def get_all_labels():
        return label_dao.get_all()

    @staticmethod
    def get_label_by_id(label_id):
        return label_dao.get_by_id(label_id)

    @staticmethod
    def create_label(data):
        return label_dao.create(data)

    @staticmethod
    def update_label(label_id, data):
        return label_dao.update(label_id, data)

    @staticmethod
    def delete_label(label_id):
        return label_dao.delete(label_id)
