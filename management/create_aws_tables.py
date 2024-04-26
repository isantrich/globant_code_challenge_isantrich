from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.engine.reflection import Inspector

# Establecer parámetros de conexión a la base de datos MySQL en AWS
SERVER = 'globant-challenge.c5mkk6cka6qn.us-east-2.rds.amazonaws.com'
USER = 'admin'
DB = 'globant_challenge'
PASSWORD = 'Guaraqueno.0211'
connection_string = f'mysql://{USER}:{PASSWORD}@{SERVER}/{DB}'

# Crea un motor de SQLAlchemy para la base de datos
engine = create_engine(connection_string)

# Define el metadata para la base de datos
metadata = MetaData()

# Define la estructura de las tablas
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

# Inspecciona la base de datos para verificar si las tablas ya existen
inspector = Inspector.from_engine(engine)
for table_name, table in tables.items():
    if not inspector.has_table(table_name):
        table.create(engine)
        print(f"La tabla '{table_name}' ha sido creada.")
    else:
        print(f"La tabla '{table_name}' ya existe en la base de datos.")
