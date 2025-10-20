import datetime
from pydantic import BaseModel
from typing import Any, Dict, Optional

class TeamOut(BaseModel):
    id: int
    name: str
    image_url: str
    role: str
    description: str
    email: str
    social_media_links: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


class TeamCreate(BaseModel):
    name: str
    role: str
    image_url: str
    description: Optional[str]
    email: Optional[str]
    social_media_links: Optional[Dict[str, Any]] = None

