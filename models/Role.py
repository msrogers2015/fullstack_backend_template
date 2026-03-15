# models/Role.py

from sqlalchemy import Column, BigInteger, String, Integer
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel


class Role(BaseModel):
    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    access_level = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    accounts = relationship("Account", back_populates="role")
