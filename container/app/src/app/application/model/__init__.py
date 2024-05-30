from pydantic import BaseModel


class DefaultModel(BaseModel):
    message: str
