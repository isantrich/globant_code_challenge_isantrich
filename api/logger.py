import os
from flask import send_file
from flask_restful import Resource


# Configure logger
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'flask_app.log')

class LogResource(Resource):
    def get(self):
        try:
            return send_file(LOG_PATH)
        except Exception as e:
            return str(e)
