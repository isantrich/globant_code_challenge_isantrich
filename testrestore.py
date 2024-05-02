from api.functions.database import DatabaseConnection
from api.functions.models_db import DEPARTMENTS_SCHEMA, HIRED_EMPLOYEES_SCHEMA, JOBS_SCHEMA


db = DatabaseConnection()
backup_dir = 'api\database_backups'

#db.restore_table_from_avro('departments', f'{backup_dir}\departments.avro')
#db.restore_table_from_avro('jobs', f'{backup_dir}\jobs.avro')
db.restore_table_from_avro('hired_employees', f'{backup_dir}\hired_employees.avro')