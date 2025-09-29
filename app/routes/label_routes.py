from flask import Blueprint, request, jsonify
from app.services.label_service import LabelService

bp = Blueprint('label', __name__, url_prefix='/label')

@bp.route('/label_to_creators', methods=['GET'])
def get_creator_for_every_label():
    authorizations = LabelService.get_creator_for_every_label()
    return jsonify(authorizations)


