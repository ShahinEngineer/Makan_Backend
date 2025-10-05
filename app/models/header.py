import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base

class Headers(Base):
    __tablename__ = "headers"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    products = Column(JSONB)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Add other fields as necessary
