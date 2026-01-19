from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .BaseModel import BaseModel
from datetime import datetime

class Account(BaseModel):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=False), nullable=False, default=datetime.now())
    last_login = Column(DateTime(timezone=False), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    credential = relationship('Credential', back_populates='account')