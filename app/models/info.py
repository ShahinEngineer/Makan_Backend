import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB


from app.db.base import Base

class Info(Base):
    __tablename__ = "info"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    phone = Column(Integer)
    email = Column(String)
    social_media = Column(String)
    location = Column(String)
    business_hours = Column(DateTime)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
