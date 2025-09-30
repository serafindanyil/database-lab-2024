from flask_restx import Namespace, Resource, fields

from app.services.authorization_service import AuthorizationService

authorization_ns = Namespace(
    "authorization",
    path="/authorization",
    description="Operations for managing authorizations",
)


authorization_model = authorization_ns.model(
    "Authorization",
    {
        "id": fields.Integer(readonly=True, description="Unique identifier"),
        "email": fields.String(required=True, description="Email address"),
        "password": fields.String(required=True, description="User password"),
    },
)

authorization_create_model = authorization_ns.model(
    "AuthorizationCreate",
    {
        "email": fields.String(required=True, description="Email address"),
        "password": fields.String(required=True, description="User password"),
    },
)

authorization_update_model = authorization_ns.clone(
    "AuthorizationUpdate",
    authorization_create_model,
)


@authorization_ns.route("/")
class AuthorizationList(Resource):
    @authorization_ns.marshal_list_with(authorization_model)
    @authorization_ns.response(200, "List of authorizations retrieved")
    def get(self):
        """List all authorizations"""
        authorizations = AuthorizationService.get_all_authorizations()
        return [auth.to_dict() for auth in authorizations]

    @authorization_ns.expect(authorization_create_model, validate=True)
    @authorization_ns.marshal_with(authorization_model, code=201)
    @authorization_ns.response(400, "Missing or invalid data")
    def post(self):
        """Create a new authorization"""
        payload = authorization_ns.payload or {}
        try:
            authorization = AuthorizationService.create_authorization(payload)
        except ValueError as error:
            authorization_ns.abort(400, str(error))
        return authorization.to_dict(), 201


@authorization_ns.route("/<int:auth_id>")
@authorization_ns.param("auth_id", "Authorization identifier")
class AuthorizationDetail(Resource):
    @authorization_ns.marshal_with(authorization_model)
    @authorization_ns.response(404, "Authorization not found")
    def get(self, auth_id: int):
        """Get authorization by ID"""
        authorization = AuthorizationService.get_authorization_by_id(auth_id)
        if not authorization:
            authorization_ns.abort(404, "Authorization not found")
        return authorization.to_dict()

    @authorization_ns.expect(authorization_update_model, validate=True)
    @authorization_ns.marshal_with(authorization_model)
    @authorization_ns.response(400, "No data provided")
    @authorization_ns.response(404, "Authorization not found")
    def put(self, auth_id: int):
        """Update authorization information"""
        payload = authorization_ns.payload or {}
        if not payload:
            authorization_ns.abort(400, "No data provided")
        authorization = AuthorizationService.update_authorization(auth_id, payload)
        if not authorization:
            authorization_ns.abort(404, "Authorization not found")
        return authorization.to_dict()

    @authorization_ns.response(204, "Authorization deleted")
    @authorization_ns.response(404, "Authorization not found")
    def delete(self, auth_id: int):
        """Delete authorization"""
        success = AuthorizationService.delete_authorization(auth_id)
        if not success:
            authorization_ns.abort(404, "Authorization not found")
        return "", 204
