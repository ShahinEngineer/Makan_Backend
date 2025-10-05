from sqlalchemy import Column, String, Integer
from app.db.base import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    image_url = Column(String)
    name = Column(String)
    # Add other fields as necessary
