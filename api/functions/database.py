from sqlalchemy import create_engine, select
from sqlalchemy.sql import select
from .models_db import DEPARTMENTS_SCHEMA
import pandas as pd
from fastavro import writer, reader
import os

# Function to convert a Python type to an Avro type
def python_type_to_avro_type(python_type):
    if python_type == "int":
        return 'int'
    elif python_type == "float":
        return 'double'
    elif python_type == "str":
        return 'string'
    else:
        return python_type

class DatabaseConnection():
    def __init__(self) -> None:

        # Database connection
        SERVER = 'globant-challenge.c5mkk6cka6qn.us-east-2.rds.amazonaws.com'
        USER = 'admin'
        DB = 'globant_challenge'
        PASSWORD = 'Guaraqueno.0211'
        connection_string = f'mysql://{USER}:{PASSWORD}@{SERVER}/{DB}'

        try:
            # Create a SQLAlchemy engine
            self.engine = create_engine(connection_string)

            # Try to connect to the database
            with self.engine.connect() as connection:
                print("Conexión exitosa")

        except Exception as e:
            print("Error al conectar:", e)

    # TODO: Refactor this method to use the get_transactions method
    def get_transactions(self):      
        query = select(DEPARTMENTS_SCHEMA)
        with self.engine.connect() as connection:
            result = connection.execute(query)
        columns = [col for col in result.keys()]
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return rows

    
    # Set transactions in the database
    def set_transactions(self, schema, data_list): 
        try:
            # Insert the rows into the table
            with self.engine.connect() as connection:
                data_list.to_sql(schema, connection, if_exists='append', index=False)
            return True, f"Datos cargados exitosamente en {schema}"  
        except Exception as e:
            return False ,  f"Server error: {e}" 
    
    # Create a backup of a table in AVRO format
    def backup_table_to_avro(self, table_name, table_schema, output_dir):
        # Obtaining the table schema
        query = select(table_schema)
        with self.engine.connect() as connection:
            result = connection.execute(query)
            rows = [{column.name: value for column, value in zip(table_schema.columns, row)} for row in result.fetchall()]

        # Create AVRO schema
        avro_schema = {
            "type": "record",
            "name": table_name,
            "fields": [{"name": column.name, "type": python_type_to_avro_type(column.type.python_type.__name__)} for column in table_schema.columns]
        }

        # Create AVRO file
        avro_file_path = os.path.join(output_dir, f"{table_name}.avro")
        print("AVRO filepath:", avro_file_path)
        with open(avro_file_path, 'wb') as avro_file:
            writer(avro_file, avro_schema, rows)

        print(f"Backup table '{table_name}' saved in'{avro_file_path}'")


    # Restore a table from an AVRO file
    def restore_table_from_avro(self, table_name, avro_file_path):

        # Read the AVRO file
        with open(avro_file_path, 'rb') as avro_file:
            avro_reader = reader(avro_file)
            rows = [record for record in avro_reader]

        # Create a DataFrame from the rows
        data_list= pd.DataFrame(rows)

        # Insert the rows into the 
        with self.engine.connect() as connection:
                data_list.to_sql(table_name, connection, if_exists='replace', index=False)

        print(f"Restauración de la tabla '{table_name}' completada correctamente")

