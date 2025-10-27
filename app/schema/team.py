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

class TeamOutLang(BaseModel):
    id: int
    name: str
    name_ar: str
    name_de: str
    image_url: str
    role: str
    role_ar: str
    role_de: str
    description: str
    description_ar: str
    description_de: str
    email: str
    social_media_links: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}

class TeamCreate(BaseModel):
    name: str
    name_ar: str
    name_de: str
    role: str
    role_ar: str
    role_de: str
    image_url: str
    description: Optional[str]
    description_ar: Optional[str]
    description_de: Optional[str]
    email: Optional[str]
    social_media_links: Optional[Dict[str, Any]] = None

