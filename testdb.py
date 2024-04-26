from sqlalchemy import create_engine

# Establece credenciales de conexión a la base de datos MySQL en aws

SERVER = 'globant-challenge.c5mkk6cka6qn.us-east-2.rds.amazonaws.com'
USER = 'admin'
DB = 'globant_challenge'
PASSWORD = 'Guaraqueno.0211'
connection_string = f'mysql://{USER}:{PASSWORD}@{SERVER}/{DB}'

try:
    # Crea un motor de SQLAlchemy para la base de datos
    engine = create_engine(connection_string)

    # Intenta conectar a la base de datos
    with engine.connect() as connection:
        print("Conexión exitosa")

except Exception as e:
    print("Error al conectar:", e)


