import os
from dotenv import load_dotenv

APP_ENV = os.getenv("APP_ENV","DEVELOPMENT")
if APP_ENV == "DEVELOPMENT":
    load_dotenv()

APP_HOST = os.getenv("APP_HOST")
APP_PORT = os.getenv("APP_PORT")
FLASK_DEBUG = True if os.getenv("FLASK_DEBUG","FALSE").lower() == "true" else False
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER","tmp/uploads")
REDIS_URI = os.getenv("REDIS_URI")


