from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class ReceivedMessage(Base):
    __tablename__ = "received_messages"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(Integer)
    message = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    # Add other fields as necessary
