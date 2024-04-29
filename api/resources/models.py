from typing import List
from pydantic import BaseModel
from pydantic import BaseModel
import numpy as np

class DepartmentModel(BaseModel):
    id: np.int64
    department: np.object_ 

    class Config:
        arbitrary_types_allowed = True

class JobModel(BaseModel):
    id: np.int64
    job: np.object_
    
    class Config:
        arbitrary_types_allowed = True

class HiredEmployeeModel(BaseModel):
    id: np.int64
    name: np.object_
    datetime: np.object_
    department_id: np.int64
    job_id: np.int64

    class Config:
        arbitrary_types_allowed = True