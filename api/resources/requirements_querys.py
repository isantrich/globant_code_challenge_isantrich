
# Number of hired employees by quarter and department and job

hired_employees_by_quarter= '''
WITH HIRES AS (
	SELECT department_id, job_id, QUARTER(datetime) hire_quarter, count(id) num_hired_employees
	FROM globant_challenge.hired_employees he 
	WHERE YEAR(datetime)= 2021
	group by 1, 2, 3

)
SELECT
d.department,
j.job,
CASE WHEN hire_quarter = 1 THEN num_hired_employees else 0 end as Q1,
CASE WHEN hire_quarter = 2 THEN num_hired_employees else 0 end as Q2,
CASE WHEN hire_quarter = 3 THEN num_hired_employees else 0 end as Q3,
CASE WHEN hire_quarter = 4 THEN num_hired_employees else 0 end as Q4
FROM HIRES h
LEFT JOIN globant_challenge.jobs j 
ON h.job_id = j.id
LEFT JOIN globant_challenge.departments d 
ON h.department_id = d.id
ORDER BY d.department ASC, j.job ASC
'''

# Department with the most hired employees thant the aver1age hired in 2021
department_most_hired_employees= '''
WITH HIRES AS (
	SELECT department_id, count(id) num_hired_employees
	FROM globant_challenge.hired_employees he 
	WHERE YEAR(datetime)= 2021
	group by 1
)
SELECT
h.department_id as id,
d.department,
num_hired_employees as hired
FROM HIRES h
LEFT JOIN globant_challenge.departments d 
ON h.department_id = d.id
HAVING num_hired_employees > (SELECT AVG(num_hired_employees) FROM HIRES)
ORDER BY num_hired_employees DESC
'''