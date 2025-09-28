from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String) # Store hashed passwords only
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    is_superuser = Column(Integer, default=0)  # 1 for superuser