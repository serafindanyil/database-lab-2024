from flask_restx import Namespace, Resource, fields

from app.services.label_service import LabelService

label_ns = Namespace(
    "label",
    path="/label",
    description="Aggregated label insights",
)


label_creators_model = label_ns.model(
    "LabelCreators",
    {
        "label_name": fields.String(description="Label name"),
        "creators": fields.String(description="Comma-separated list of creators"),
    },
)


@label_ns.route("/label_to_creators")
class LabelCreators(Resource):
    @label_ns.marshal_list_with(label_creators_model)
    @label_ns.response(200, "Creators grouped by label retrieved")
    def get(self):
        """Get creators grouped by label"""
        return LabelService.get_creator_for_every_label()


