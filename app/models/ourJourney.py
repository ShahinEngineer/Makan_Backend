import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class OurJourney(Base):
    __tablename__ = "our_journey"

    id = Column(Integer, primary_key=True, index=True)
    story_subtitle = Column(String)
    story_description = Column(String)
    story_img_url = Column(String)
    # vision and mission
    vision_description = Column(String)
    mission_description = Column(String)
    mission_vision_img_url = Column(String)
    # values
    value_description = Column(String)
    our_values = Column(JSONB)



    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Add other fields as necessary
