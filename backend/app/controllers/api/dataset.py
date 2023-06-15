from flask_restful import Resource,request
from flask import current_app
from app.helpers.rest import *
from app.helpers import redis

import pandas

class DataInputHandler(Resource):
    def get(self):
        redis_client = None
        with current_app.app_context():
            redis_client = current_app.config['redis_client']
        args = request.args.to_dict()
        target = args.get("target","dataset")
        if target == "dataset:filename":
            data = redis.redis_get_list(redis_client,"dataset:filename")
        else:
            data = redis.redis_get_json(redis_client,"dataset:raw")
        return response(200, data=data, message="OK")
    
    def post(self):
        redis_client = None
        with current_app.app_context():
            redis_client = current_app.config['redis_client']
        try:
            file = request.files.get("file")
            filename = file.filename
            if filename.split(".")[-1] != "csv":
                raise TypeError("File is not in csv format")
            df = pandas.read_csv(file)
            dataset_dict = df.to_dict()
            redis.redis_store_json(redis_client,"dataset:raw",dataset_dict)
            redis.redis_add_list(redis_client,"dataset:filename",[filename])
        except ValueError:
            return response(400,message="Invalid Input")
        except Exception as e:
            return response(400, message=str(e))
            
        data = {
            "status": True
        }
        return response(200, data=data, message="OK")
