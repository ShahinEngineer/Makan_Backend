import datetime
from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    description: str
    content: str
    hash_tags: str
    img_url: str
    feature_news: bool = False

class NewsOut(BaseModel):
    id: int
    title: str
    description: str
    content: str
    hash_tags: str
    img_url: str
    feature_news: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}
