from app.dao.label_dao import label_dao

class LabelService:
    @staticmethod
    def get_creator_for_every_label():
        return label_dao.get_creator_for_every_label()
