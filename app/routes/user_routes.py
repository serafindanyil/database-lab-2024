from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
def get_users():
    users = UserService.get_all_users()
    return jsonify([user.to_dict() for user in users])


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict())


@bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = UserService.create_user(data or {})
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "An internal error occurred", "error": str(e)}), 500


@bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    try:
        user = UserService.update_user(user_id, data)
    except ValueError as error:
        return jsonify({"message": str(error)}), 400
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict())


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if not success:
        return jsonify({"message": "User not found"}), 404
    return "", 204


@bp.route("/download", methods=["GET"])
def get_download():
    downloads = UserService.get_downloads()
    return jsonify(downloads)
