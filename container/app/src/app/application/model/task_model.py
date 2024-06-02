from pydantic import BaseModel
from datetime import datetime, date


class TaskCreateModel(BaseModel):
    title: str
    detail: str
    priority_id: int
    category_id: int
    start_date: date


class TaskReadModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    detail: str
    priority_id: int
    category_id: int
    start_date: date
    is_done: bool


class TaskUpdateModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    detail: str
    priority_id: int
    category_id: int
    start_date: date
