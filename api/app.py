from flask_restful import Api
from resources.transactions import GlobantResource
from flask import Flask

app = Flask(__name__)
api = Api(app)

# Rutas de los recursos
api.add_resource(GlobantResource, '/loadtransactions')

if __name__ == '__main__':
    app.run(debug=True)