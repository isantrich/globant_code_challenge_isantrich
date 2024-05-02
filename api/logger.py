from flask import send_file
from flask_restful import Resource


LOG_PATH = 'flask_app.log'

class LogResource(Resource):
    def get(self):
        try:
            return send_file(LOG_PATH)
        except Exception as e:
            return str(e)
