from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.engine.reflection import Inspector

# Establish the connection to the database
SERVER = 'globant-challenge.c5mkk6cka6qn.us-east-2.rds.amazonaws.com'
USER = 'admin'
DB = 'globant_challenge'
PASSWORD = 'Guaraqueno.0211'
connection_string = f'mysql://{USER}:{PASSWORD}@{SERVER}/{DB}'

# Create the engine
engine = create_engine(connection_string)

metadata = MetaData()

# Define structure of the tables
tables = {
    'departments': Table('departments', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('department', String(255))),
    'jobs': Table('jobs', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('job', String(255))),
    'hired_employees': Table('hired_employees', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('name', String(100)),
                             Column('datetime', String(100)),
                             Column('department_id', Integer),
                             Column('job_id', Integer))
}

# Inspector to check if tables exist
inspector = Inspector.from_engine(engine)
for table_name, table in tables.items():
    if not inspector.has_table(table_name):
        table.create(engine)
        print(f"La tabla '{table_name}' ha sido creada.")
    else:
        print(f"La tabla '{table_name}' ya existe en la base de datos.")
