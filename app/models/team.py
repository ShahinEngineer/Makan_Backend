import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB


from app.db.base import Base
from app.db.base import Base
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    role = Column(String)
    description = Column(String)
    image_url = Column(String)
    email = Column(String, unique=True, index=True)
    social_media_links = Column(JSONB)  # Store as JSON for flexibility

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Add other fields as necessary
