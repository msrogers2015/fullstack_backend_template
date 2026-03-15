# models/BaseModel.py

from sqlalchemy.orm import DeclarativeBase
from typing import Any


class BaseModel(DeclarativeBase):
    id: Any

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
