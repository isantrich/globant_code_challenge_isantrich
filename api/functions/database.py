from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql import select, insert
from .models_db import DEPARTMENTS_SCHEMA, HIRED_EMPLOYEES_SCHEMA, JOBS_SCHEMA
import pandas as pd


class DatabaseConnection():
    def __init__(self) -> None:

        # Establecer parámetros de conexión a la base de datos MySQL en AWS
        SERVER = 'globant-challenge.c5mkk6cka6qn.us-east-2.rds.amazonaws.com'
        USER = 'admin'
        DB = 'globant_challenge'
        PASSWORD = 'Guaraqueno.0211'
        connection_string = f'mysql://{USER}:{PASSWORD}@{SERVER}/{DB}'

        try:
            # Crea un motor de SQLAlchemy para la base de datos
            self.engine = create_engine(connection_string)

            # Intenta conectar a la base de datos
            with self.engine.connect() as connection:
                print("Conexión exitosa")

        except Exception as e:
            print("Error al conectar:", e)


    def get_transactions(self):      
        query = select(DEPARTMENTS_SCHEMA)
        with self.engine.connect() as connection:
            result = connection.execute(query)
        columns = [col for col in result.keys()]
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return rows


    def set_transactions_old(self, schema, data):
        if schema == "departments":
            query = insert(DEPARTMENTS_SCHEMA).values(id= data.id, department= data.department)
        elif schema == "jobs":
            query = insert(JOBS_SCHEMA).values(id= data.id, jobs= data.jobs)
        elif schema == "hired_employees":
            query = insert(HIRED_EMPLOYEES_SCHEMA).values(id= data.id, name= data.name, datetime = data.datetime, department_id = data.department_id, job_id= data.job_id)
        else:
            return False

        with self.engine.connect() as connection:
            result = connection.execute(query)
        rows_affected = result.rowcount  # Obtener el número de filas afectadas
        return rows_affected
    

    def set_transactions(self, schema, data_list): 
        try:
            # Escribir el DataFrame en la base de datos
            with self.engine.connect() as connection:
                data_list.to_sql(schema, connection, if_exists='append', index=False)
            return True, f"Datos cargados exitosamente en {schema}"  # Devolver True si la operación fue exitosa
        except Exception as e:
            return False ,  f"Server error: {e}" # Devolver False si la operación falló