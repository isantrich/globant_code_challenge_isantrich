from pydantic import BaseModel, ValidationError
from flask import request
from flask_restful import Resource, reqparse
from resources.transactions_logger import configure_logger
from functions.database import DatabaseConnection 
from .models import DepartmentModel, JobModel, HiredEmployeeModel
import pandas as pd
from io import StringIO
import numpy as np

# Configure logger
logger = configure_logger()

# Model schema
MODEL_SCHEMA = { 
        "departments": DepartmentModel,
        "jobs": JobModel,
        "hired_employees": HiredEmployeeModel
    }

# Fillna parameters
FILLNA_PARAMETERS = 0


class GlobantResource(Resource):

    def __init__(self):
        self.db = DatabaseConnection()

    # Validate the data structure
    def validar_lote(self, datos, model):
        expected_dtypes = [type_ for field, type_ in model.__annotations__.items()]
        logger.info("Expected dtypes: %s", expected_dtypes)
        print("Expected dtypes:")
        print(expected_dtypes)
        for dtype, expected_dtype in zip(datos.dtypes, expected_dtypes):
            if dtype != expected_dtype:
                return False, f"La columna {datos.columns.tolist().index(dtype)} tiene un tipo de dato incorrecto. Esperado: {expected_dtype}, Obtenido: {dtype}"

        return True, "Todos los datos son válidos"
    
    # Handle NaN values
    def nan_handler(self, datos):
        for column in datos.columns:
            if datos[column].isnull().values.any() and datos[column].dtype == 'float64':
                datos[column] = datos[column].fillna(FILLNA_PARAMETERS)
                datos[column] = datos[column].astype(np.int64)
        datos= datos.fillna('Sin información')
        return datos

    # POST method
    def post(self):
        
        # Parameters required in the post request
        parser = reqparse.RequestParser()
        parser.add_argument('fileName', required=True, type=str)
        parser.add_argument('fileData', required=True, type=str)

        args = parser.parse_args()

        fileName = args['fileName']
        fileData = args['fileData']

        logger.info("Received file: %s", fileName)
        logger.info("File data type: %s", type(fileData))

        print(f"fileName: {fileName}")
        print(f"fileData: {type(fileData)}")

        try:
            # Receive data and convert it into a DataFrame
            data = StringIO(fileData)
            transaction_data = pd.read_csv(data, header=None, names=MODEL_SCHEMA[fileName].model_fields.keys())
            if len(transaction_data) > 1000:
                logger.error("Bad request: File exceed rows: %s", len(transaction_data))
                return {'error': "Bad request: File exceed rows"}, 400
            
            # Handle NaN values
            transaction_data = self.nan_handler(transaction_data)

        except Exception as e:
            logger.error("Error processing request: %s", e)
            return {'error': f"Bad Request: {e}"}, 400
        
        
        try:
            # Validate the data structure
            is_valid, message = self.validar_lote(transaction_data, MODEL_SCHEMA[fileName])

            if not is_valid:
                logger.error("error: %s", message)
                return {'error': message}, 400

            result, message = self.db.set_transactions(schema=fileName, data_list=transaction_data)

            if result:
                logger.info("message: %s", message)
                return {'message': message}, 200
            else:
                logger.error("error: %s", message)
                return {'error': message}, 500
        
        except Exception as e:
            logger.error("Server error: %s", e)
            return {'error': f"Server error: {e}"}, 500
            
