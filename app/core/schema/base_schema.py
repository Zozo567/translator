__all__ = ("BaseSchema",)

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config(BaseModel.Config):
        orm_mode = True
        arbitrary_types_allowed = True
