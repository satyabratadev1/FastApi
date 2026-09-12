from pydantic import BaseModel
from typing import Optional

class ApiResponse(BaseModel):
    status :str
    message:str
    data : Optional[dict] = None
