from pydantic import BaseModel
from typing import Optional

class ApiObservation(BaseModel):
    task_id: str
    message: str
    last_action: Optional[str] = None

class ApiAction(BaseModel):
    action: str
