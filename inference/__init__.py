from flask_restx import Api

from .api import api as detection_api

api = Api(title="YOLOv4 Detection API", version="1.0", description="YOLOv4 Detection API",)

api.add_namespace(detection_api)
