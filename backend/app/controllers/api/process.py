from flask_restful import Resource,request
from flask import current_app
from app.helpers.rest import *
from app.helpers import redis
from app.helpers import dataset_handler
import pandas


class DatasetHandler(Resource):
    def get(self):
        with current_app.app_context():
            redis_client = current_app.config['redis_client']
        args = request.args.to_dict()
        target = args.get("target","dataset:normalized")
        if target == "dataset:result":
            data = redis.redis_get_json(redis_client,"dataset:result")
        else:
            data = redis.redis_get_json(redis_client,"dataset:normalized")
        return response(200, data=data, message="OK")
    
    def post(self):
        json_req = request.get_json(force=True)
        action = json_req.get("action","invalid")
        if action == 'preprocess':
            response_obj = self.__preprocess_data()
        else:
            response_obj = response(400,message="Unknown command")

        return response_obj

    def __switch_to_original_column(self,dataset:pandas.DataFrame):
        '''
        Fungsi untuk merubah nama kolom dari A1,A2,A3...An ke nama asli
        '''
        with current_app.app_context():
            redis_client = current_app.config['redis_client']
        column_mapping = redis.redis_get_json(redis_client,"dataset:column_mapping")
        change_column = dict()
        for col in dataset.columns:
            change_column[col] = column_mapping[col]
        result = dataset.rename(columns=change_column)
        return result
            
    
    def __preprocess_data(self):
        # Get redis object from flask
        with current_app.app_context():
            redis_client = current_app.config['redis_client']
        if redis_client == None:
            return response(500, message="Trouble connecting to database")
        try:

            # Get raw unprocessed data from redis db
            dataset_dict = redis.redis_get_json(redis_client,"dataset:raw")
            df_raw = pandas.DataFrame(data=dataset_dict)
            # Normalize
            df_normalize = dataset_handler.normalize_datasets(df_raw)

            # Create column mapping
            original_column = list(dataset_dict.keys())
            normalized_columns = list(df_normalize.columns)
            column_mapping = dict(zip(normalized_columns,original_column))



            # Store data
            redis.redis_store_json(redis_client, "dataset:column_mapping", column_mapping)
            # Rename to original
            df_return = self.__switch_to_original_column(df_normalize)
            redis.redis_store_json(redis_client,"dataset:normalized",df_return.to_dict('records'))
        except Exception as e:
            return response(400,message=str(e))
        
        # Train data
        # Data langsung di train nanti front end tinggal ambil
        data_trainer = dataset_handler.DataTrainer(df_normalize,column_mapping)

        try:
            data_trainer.train_data(df_normalize)
        except Exception as e:
            return response(400,message=str(e))
        
        try:
            # Convert to json
            store_result = json.dumps(data_trainer.training_result,cls=dataset_handler.NpEncoder)
            redis.redis_store_json(redis_client,"dataset:result",store_result)
        except Exception as e:
            return response(500,message=str(e))

        data = df_return.to_dict('records')

        return response(200, data=data, message="OK")
