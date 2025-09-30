from flask import Blueprint, request, jsonify
from app.services.authorization_service import AuthorizationService

bp = Blueprint("authorization", __name__, url_prefix="/authorization")


@bp.route("/", methods=["GET"])
def get_authorizations():
    authorizations = AuthorizationService.get_all_authorizations()
    # Конвертуємо кожен об'єкт у списку
    return jsonify([auth.to_dict() for auth in authorizations])


@bp.route("/<int:auth_id>", methods=["GET"])
def get_authorization(auth_id):
    authorization = AuthorizationService.get_authorization_by_id(auth_id)
    if not authorization:
        return jsonify({"message": "Authorization not found"}), 404
    return jsonify(authorization.to_dict())


@bp.route("/", methods=["POST"])
def create_authorization():
    data = request.get_json() or {}
    try:
        authorization = AuthorizationService.create_authorization(data)
    except ValueError as error:
        return jsonify({"message": str(error)}), 400
    return jsonify(authorization.to_dict()), 201


@bp.route("/<int:auth_id>", methods=["PUT"])
def update_authorization(auth_id):
    data = request.get_json() or {}
    if not data:
        return jsonify({"message": "No data provided"}), 400
    authorization = AuthorizationService.update_authorization(auth_id, data)
    if not authorization:
        return jsonify({"message": "Authorization not found"}), 404
    return jsonify(authorization.to_dict())


@bp.route("/<int:auth_id>", methods=["DELETE"])
def delete_authorization(auth_id):
    success = AuthorizationService.delete_authorization(auth_id)
    if not success:
        return jsonify({"message": "Authorization not found"}), 404
    return "", 204
