import datetime
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    image_url: str | None = None


class CategoryOut(BaseModel):
    id: int
    name: str
    image_url: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}
