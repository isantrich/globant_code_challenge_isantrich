import os
from flask import Flask, render_template
from flask_restful import Api
from resources.transactions import GlobantResource, GlobantResourceJSON
from logger import LogResource
from functions.database import DatabaseConnection
import pandas as pd
from resources.requirements_querys import hired_employees_by_quarter, department_most_hired_employees

app = Flask(__name__)
api = Api(app)

# Configure logger
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'flask_app.log')

#Endpoint resource for logs on html
@app.route('/logshtml')
def LogResourceHTML():
    with open(LOG_PATH, 'r') as f:
        log = f.read()
    log_lines = log.split('\n')
    html_log = '<br>'.join(log_lines)
    
    return render_template('log_template.html', html_log=html_log)

#Endpoint resource for query hired employees by quarter on html
@app.route('/hiredemployeesbyquarter')
def requirement_hired_by_quarter():   
    db_connection = DatabaseConnection()
    df = pd.read_sql_query(hired_employees_by_quarter, db_connection.engine)
    custom_titles = ["Number of employees hired for each job and department in 2021 divided by quarter."]
    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=custom_titles)

#Endpoint resource for query department most hired employees on html
@app.route('/departmentmosthiredemployees')
def requirements_most_hired():   
    db_connection = DatabaseConnection()
    df = pd.read_sql_query(department_most_hired_employees, db_connection.engine)
    custom_titles = ["List of departments that hired more employees than the mean of employees hired in 2021."]
    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=custom_titles)

#Endpoint for transactions
api.add_resource(GlobantResource, '/loadtransactions')

#Endpoint for logs file
api.add_resource(LogResource, '/logs')

#Endponit for get transactions in JSON format
api.add_resource(GlobantResourceJSON, '/gettransactions/<string:table_name>')

if __name__ == '__main__':
    app.run(debug=True)