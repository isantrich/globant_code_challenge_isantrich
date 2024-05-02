from flask import Flask
from flask_restful import Api
from resources.transactions_logger import configure_logger
from resources.transactions import GlobantResource

app = Flask(__name__)
api = Api(app)


# Resource endpoint
api.add_resource(GlobantResource, '/loadtransactions')

if __name__ == '__main__':
    app.run(debug=True)