from flask import Blueprint
from flask_restful import Api
from .health import *
from .dataset import *
from .process import *

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)
api.add_resource(HealthCheck,"/health")
api.add_resource(DataInputHandler,"/dataset")
api.add_resource(DatasetHandler,"/process")