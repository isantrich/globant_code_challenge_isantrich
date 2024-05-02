from api.functions.database import DatabaseConnection
from api.functions.models_db import DEPARTMENTS_SCHEMA, HIRED_EMPLOYEES_SCHEMA, JOBS_SCHEMA

db = DatabaseConnection()
output_dir = 'api\database_backups'

# Ejemplo de uso para cada tabla
try:
    db.backup_table_to_avro(table_name='departments', table_schema=DEPARTMENTS_SCHEMA, output_dir=output_dir)
    db.backup_table_to_avro(table_name='jobs', table_schema=JOBS_SCHEMA, output_dir=output_dir)
    db.backup_table_to_avro(table_name='hired_employees', table_schema=HIRED_EMPLOYEES_SCHEMA, output_dir=output_dir)
    print("Backup exitoso")
except Exception as e:
    print("Error al hacer backup:", e)