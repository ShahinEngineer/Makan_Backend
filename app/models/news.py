import sqlalchemy as sa
from sqlalchemy import Boolean, Column, String, Integer, DateTime, func, Text
from sqlalchemy.dialects.postgresql import JSONB


from app.db.base import Base
from app.db.base import Base
class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    description = Column(String)
    content = Column(Text)  # New content field
    hash_tags = Column(String)
    img_url  = Column(String)
    feature_news = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Add other fields as necessary
