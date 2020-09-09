from flask_restx import Namespace, Resource, fields
from .predictions import detector
from .data_source import source

api = Namespace("detection", description="Object detector prediction")

detection_box = api.model("BoundingBox",
                          {
                              "x": fields.Float,
                              "y": fields.Float,
                              "w": fields.Float,
                              "h": fields.Float,
                          }
                        )

detection = api.model(
    "Prediction",
    {
        "label": fields.String(required=True, description="Detected label"),
        "classId": fields.Integer(required=True, description="Detected class ID"),
        "score": fields.Float(required=True, description="Detected class ID"),
        "bbox": fields.Nested(
            detection_box
        ),
        'datetime_predicted': fields.DateTime(dt_format='rfc822'),
    },
)

@api.route("/detections")
class DetectionList(Resource):
    @api.doc("list_detections")
    @api.marshal_list_with(detection)
    def get(self):
        frame = source.get_source()
        predictions = detector.forward(frame)
        return predictions

