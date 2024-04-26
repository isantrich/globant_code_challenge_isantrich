from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.engine.reflection import Inspector

metadata = MetaData()

DEPARTMENTS_SCHEMA = Table('departments', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('department', String(255)))

JOBS_SCHEMA = Table('jobs', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('job', String(255)))


HIRED_EMPLOYEES_SCHEMA = Table('hired_employees', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('name', String(100)),
                             Column('datetime', String(100)),
                             Column('department_id', Integer),
                             Column('job_id', Integer))
