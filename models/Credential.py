from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .BaseModel import BaseModel
from datetime import datetime

class Credential(BaseModel):
    __tablename__ = "credential"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account_id = Column(BigInteger, ForeignKey('account.id'), nullable=False)
    password_hash = Column(String, nullable=True)
    previous_hash = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, default=datetime.now())

    account = relationship('Account', back_populates='credential')