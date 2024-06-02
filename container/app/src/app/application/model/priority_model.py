from pydantic import BaseModel
from datetime import datetime


class PriorityReadModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
