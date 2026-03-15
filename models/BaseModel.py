# models/BaseModel.py

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
