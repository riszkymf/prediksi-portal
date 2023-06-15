import os,logging,sys
from flask import Flask,current_app,g
from dotenv import load_dotenv
from datetime import date,datetime
from app import config
from flask_cors import CORS
import redis



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*":{"origins": "*"}})

    from .controllers import api_blueprint
    app.register_blueprint(api_blueprint)
    with app.app_context():
        redis_client = redis.from_url(config.REDIS_URI)
        app.config['redis_client'] = redis_client
    return app