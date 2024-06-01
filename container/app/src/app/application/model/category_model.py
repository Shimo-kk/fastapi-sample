from pydantic import BaseModel
from datetime import datetime


class CategoryCreateModel(BaseModel):
    name: str


class CategoryReadModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str


class CategoryUpdateModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
