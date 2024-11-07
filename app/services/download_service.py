from app.dao.download_dao import download_dao

class DownloadService:
    @staticmethod
    def get_all_downloads():
        return download_dao.get_all()

    @staticmethod
    def get_download_by_id(download_id):
        return download_dao.get_by_id(download_id)

    @staticmethod
    def create_download(data):
        return download_dao.create(data)

    @staticmethod
    def delete_download(download_id):
        return download_dao.delete(download_id)
