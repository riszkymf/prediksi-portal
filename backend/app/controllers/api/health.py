from flask_restful import Resource
from flask import current_app
from app.helpers.rest import *

class HealthCheck(Resource):
    def get(self):
        data = {
            "check": "100"
        }
        return response(200, data=data, message="OK")