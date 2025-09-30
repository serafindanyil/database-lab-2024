from flask_restx import Namespace, Resource, fields

from app.services.review_service import ReviewService

review_ns = Namespace(
    "review",
    path="/review",
    description="Operations related to reviews and user-song connections",
)


review_create_model = review_ns.model(
    "ReviewCreate",
    {
        "song_id": fields.Integer(required=True, description="Identifier of the song"),
        "user_id": fields.Integer(required=True, description="Identifier of the user"),
        "content": fields.String(required=True, description="Review text"),
        "rating": fields.Integer(required=True, description="Rating between 1 and 5"),
    },
)

user_song_connection_model = review_ns.model(
    "UserSongConnection",
    {
        "user_name": fields.String(required=True, description="Name of the user"),
        "song_name": fields.String(required=True, description="Name of the song"),
    },
)

message_model = review_ns.model(
    "Message",
    {"message": fields.String(description="Operation result")},
)


@review_ns.route("/")
class ReviewCollection(Resource):
    @review_ns.expect(review_create_model, validate=True)
    @review_ns.marshal_with(message_model, code=201)
    @review_ns.response(400, "Validation error")
    @review_ns.response(500, "Failed to insert review")
    def post(self):
        """Create a review for a song"""
        payload = review_ns.payload or {}
        try:
            ReviewService.insert_review(
                payload["song_id"],
                payload["user_id"],
                payload["content"],
                payload["rating"],
            )
        except ValueError as error:
            review_ns.abort(400, str(error))
        except RuntimeError as error:
            review_ns.abort(500, str(error))
        except Exception as error:  # pragma: no cover - unexpected failure
            review_ns.abort(500, str(error))
        return {"message": "Review inserted successfully!"}, 201


@review_ns.route("/song")
class ReviewUserSong(Resource):
    @review_ns.expect(user_song_connection_model, validate=True)
    @review_ns.marshal_with(message_model, code=201)
    @review_ns.response(400, "Validation error")
    @review_ns.response(500, "Failed to create user-song connection")
    def post(self):
        """Create a download entry linking a user and a song"""
        payload = review_ns.payload or {}
        try:
            ReviewService.insert_user_song_connection(
                payload["user_name"],
                payload["song_name"],
            )
        except ValueError as error:
            review_ns.abort(400, str(error))
        except RuntimeError as error:
            review_ns.abort(500, str(error))
        except Exception as error:  # pragma: no cover - unexpected failure
            review_ns.abort(500, str(error))
        return {"message": "User-song connection created!"}, 201