from typing import List
from pydantic import BaseModel

class DepartmentModel(BaseModel):
    id: int
    department: str 

class JobModel(BaseModel):
    id: int
    job: str

class HiredEmployeeModel(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class DepartmentListModel(BaseModel):
    departments: List[DepartmentModel]

class JobListModel(BaseModel):
    jobs: List[JobModel]

class HiredEmployeeListModel(BaseModel):
    hired_employees: List[HiredEmployeeModel]