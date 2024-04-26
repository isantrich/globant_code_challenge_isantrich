from pydantic import BaseModel, ValidationError, constr, Field

# Definir el modelo Pydantic para la validación de datos
class DepartmentModel(BaseModel):
    id: int
    department: str 