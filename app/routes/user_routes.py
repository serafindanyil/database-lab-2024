from flask_restx import Namespace, Resource, fields

from app.services.user_service import UserService

user_ns = Namespace(
    "user",
    path="/user",
    description="Operations for managing users and their downloads",
)


profile_model = user_ns.model(
    "ProfileUser",
    {
        "id": fields.Integer(description="Profile identifier"),
        "picture_link": fields.String(description="Profile avatar URL"),
        "bio": fields.String(description="Short biography"),
    },
)

subscription_model = user_ns.model(
    "Subscription",
    {
        "id": fields.Integer(description="Subscription identifier"),
        "plan": fields.String(description="Subscription plan name"),
        "price": fields.Integer(description="Subscription price"),
    },
)

user_model = user_ns.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="User identifier"),
        "name": fields.String(required=True, description="Display name"),
        "authorization_id": fields.Integer(required=True, description="Authorization reference"),
        "profile_user_id": fields.Integer(description="Profile reference"),
        "subscription_id": fields.Integer(description="Subscription reference"),
        "profile": fields.Nested(profile_model, allow_null=True),
        "subscription": fields.Nested(subscription_model, allow_null=True),
    },
)

user_create_model = user_ns.model(
    "UserCreate",
    {
        "name": fields.String(required=True, description="Display name"),
        "authorization_id": fields.Integer(required=True, description="Authorization identifier"),
        "subscription_id": fields.Integer(required=True, description="Subscription identifier"),
    },
)

user_update_model = user_ns.model(
    "UserUpdate",
    {
        "name": fields.String(description="Display name"),
        "subscription_id": fields.Integer(description="Subscription identifier"),
    },
)

download_model = user_ns.model(
    "Download",
    {
        "id": fields.Integer(description="Download identifier"),
        "song_id": fields.Integer(description="Related song"),
        "user_id": fields.Integer(description="User who downloaded"),
    },
)


@user_ns.route("/")
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    @user_ns.response(200, "List of users retrieved")
    def get(self):
        """List all users"""
        users = UserService.get_all_users()
        return [user.to_dict() for user in users]

    @user_ns.expect(user_create_model, validate=True)
    @user_ns.marshal_with(user_model, code=201)
    @user_ns.response(400, "Missing or invalid data")
    @user_ns.response(500, "Internal server error")
    def post(self):
        """Create a new user"""
        payload = user_ns.payload or {}
        try:
            user = UserService.create_user(payload)
        except ValueError as error:
            user_ns.abort(400, str(error))
        except Exception as error:  # pragma: no cover - unexpected failure
            user_ns.abort(500, "An internal error occurred", error=str(error))
        return user.to_dict(), 201


@user_ns.route("/<int:user_id>")
@user_ns.param("user_id", "User identifier")
class UserDetail(Resource):
    @user_ns.marshal_with(user_model)
    @user_ns.response(404, "User not found")
    def get(self, user_id: int):
        """Retrieve a user by ID"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            user_ns.abort(404, "User not found")
        return user.to_dict()

    @user_ns.expect(user_update_model, validate=True)
    @user_ns.marshal_with(user_model)
    @user_ns.response(400, "Missing or invalid data")
    @user_ns.response(404, "User not found")
    def put(self, user_id: int):
        """Update an existing user"""
        payload = user_ns.payload or {}
        if not payload:
            user_ns.abort(400, "No data provided for update")
        try:
            user = UserService.update_user(user_id, payload)
        except ValueError as error:
            user_ns.abort(400, str(error))
        if not user:
            user_ns.abort(404, "User not found")
        return user.to_dict()

    @user_ns.response(204, "User deleted")
    @user_ns.response(404, "User not found")
    def delete(self, user_id: int):
        """Delete a user"""
        success = UserService.delete_user(user_id)
        if not success:
            user_ns.abort(404, "User not found")
        return "", 204


@user_ns.route("/download")
class UserDownloadList(Resource):
    @user_ns.marshal_list_with(download_model)
    @user_ns.response(200, "Download list retrieved")
    def get(self):
        """List all downloads"""
        return UserService.get_downloads()
