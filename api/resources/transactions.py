from pydantic import ValidationError
from flask import request
from flask_restful import Resource, reqparse
from functions.database import DatabaseConnection 
from .models import DepartmentModel
import pandas as pd
from io import StringIO


class GlobantResource(Resource):
    def __init__(self):
        self.db = DatabaseConnection() 

    def get(self):
        departments = self.db.get_departments()
        return {'departments': [DepartmentModel(**dept).dict() for dept in departments]}, 200

    def post(self):
        # Parametros requerido en la peticion post
        parser = reqparse.RequestParser()
        parser.add_argument('fileName', required=True, type=str)
        parser.add_argument('fileData', required=True, type=str)

        args = parser.parse_args()

        fileName = args['fileName']
        fileData = args['fileData']

        try:
            # Recibo datos y convierto en un df
            data = StringIO(fileData)
            transaction_data=pd.read_csv(data)

        except:
            return {'message': "Archivo no valido."}, 500
        
        result = self.db.set_transactions(schema=fileName, data_list=transaction_data)
        if result:
            return {'message': "Datos CSV procesados correctamete."}, 200
        else:
            return {'message': "Falló al procesar los datos."}, 500



    #    try:
    #        departamento = DepartmentModel(**data)
    #        rows_affected = self.db.set_departments(departamento)
    #        if rows_affected > 0:
    #            return {'message': 'Departamento creado correctamente', 'data': departamento.dict()}, 201
    #        else:
    #            return {'message': 'Ocurrió un error al agregar el departamento'}, 500
    #    except ValidationError as e:
    #        return {'error': 'Error de validación', 'details': e.errors()}, 400
        