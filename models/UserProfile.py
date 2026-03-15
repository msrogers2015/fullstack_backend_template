# models/UserProfile.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    ForeignKey,
    UniqueConstraint,
    DateTime,
)
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class UserProfile(BaseModel):
    __tablename__ = "user_profile"
    __table_args__ = (
        UniqueConstraint("account_id", name="user_profile_account_id_ukey"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=True)
    phone_number = Column(String(15), nullable=True)
    account_id = Column(
        BigInteger, ForeignKey("account.id", ondelete="RESTRICT"), nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    account = relationship("Account", back_populates="user_profile")
