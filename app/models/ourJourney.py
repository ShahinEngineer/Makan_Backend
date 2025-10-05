import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, func

from app.db.base import Base

class OurJourney(Base):
    __tablename__ = "our_journey"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Add other fields as necessary
