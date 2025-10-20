import datetime
from pydantic import BaseModel

class GallaryCreate(BaseModel):
    img_url: str


class GallaryOut(BaseModel):
    img_url: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}