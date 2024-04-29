from pydantic import BaseModel, ValidationError
from flask import request
from flask_restful import Resource, reqparse
from functions.database import DatabaseConnection 
from .models import DepartmentModel, JobModel, HiredEmployeeModel
import pandas as pd
from io import StringIO
import traceback
import numpy as np

MODEL_SCHEMA = { 
        "departments": DepartmentModel,
        "jobs": JobModel,
        "hired_employees": HiredEmployeeModel
    }

FILLNA_PARAMETERS = 0

class GlobantResource(Resource):

    def __init__(self):
        self.db = DatabaseConnection()


    def validar_lote(self, datos, model):
        expected_dtypes = [type_ for field, type_ in model.__annotations__.items()]
        print("Expected dtypes:")
        print(expected_dtypes)
    
        for dtype, expected_dtype in zip(datos.dtypes, expected_dtypes):
            if dtype != expected_dtype:
                return False, f"La columna {datos.columns.tolist().index(dtype)} tiene un tipo de dato incorrecto. Esperado: {expected_dtype}, Obtenido: {dtype}"
    
        return True, "Todos los datos son válidos"
    

    def nan_handler(self, datos):
        for column in datos.columns:
            if datos[column].isnull().values.any() and datos[column].dtype == 'float64':
                datos[column] = datos[column].fillna(FILLNA_PARAMETERS)
                datos[column] = datos[column].astype(np.int64)
        return datos

    def post(self):
        
        # Parametros requerido en la peticion post
        parser = reqparse.RequestParser()
        parser.add_argument('fileName', required=True, type=str)
        parser.add_argument('fileData', required=True, type=str)

        args = parser.parse_args()

        fileName = args['fileName']
        fileData = args['fileData']
        print(f"fileName: {fileName}")
        print(f"fileData: {type(fileData)}")

        try:
            # Recibo datos y convierto en un df
            data = StringIO(fileData)
            
            transaction_data = pd.read_csv(data, header=None, names=MODEL_SCHEMA[fileName].model_fields.keys())
            transaction_data = self.nan_handler(transaction_data)

            print(transaction_data.head())
            print("type:", transaction_data.dtypes)
            is_valid, message = self.validar_lote(transaction_data, MODEL_SCHEMA[fileName])
            print(is_valid, message)
            if not is_valid:
                return {'error': message}, 400
    
            result = self.db.set_transactions(schema=fileName, data_list=transaction_data)
            if result:
                return {'message': "Datos CSV procesados correctamente."}, 200
            else:
                return {'message': "Falló al procesar los datos."}, 500
            
        except Exception as e:
            print(f"Error: {e}")
            print(f"Traceback: {traceback.format_exc()}")
