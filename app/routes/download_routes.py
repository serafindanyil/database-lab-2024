from flask import Blueprint, request, jsonify
from app.services.download_service import DownloadService

bp = Blueprint('download', __name__, url_prefix='/downloads')

@bp.route('/', methods=['GET'])
def get_downloads():
    downloads = DownloadService.get_all_downloads()
    return jsonify(downloads)

@bp.route('/<int:download_id>', methods=['GET'])
def get_download(download_id):
    download = DownloadService.get_download_by_id(download_id)
    if not download:
        return jsonify({'message': 'Download not found'}), 404
    return jsonify(download)

@bp.route('/', methods=['POST'])
def create_download():
    data = request.get_json()
    download = DownloadService.create_download(data)
    return jsonify(download), 201

@bp.route('/<int:download_id>', methods=['DELETE'])
def delete_download(download_id):
    result = DownloadService.delete_download(download_id)
    if not result:
        return jsonify({'message': 'Download not found'}), 404
    return jsonify({'message': 'Download deleted successfully'})
