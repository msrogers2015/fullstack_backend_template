# models/Account.py

from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from .BaseModel import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class Account(BaseModel):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    role_id = Column(
        BigInteger, ForeignKey("role.id", ondelete="RESTRICT"), nullable=True
    )
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    full_name = Column(String, nullable=True)

    credential = relationship("Credential", back_populates="account", uselist=False)
    user_profile = relationship("UserProfile", back_populates="account", uselist=False)
    role = relationship("Role", back_populates="accounts")
