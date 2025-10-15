import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: str
    variants: Optional[Dict[str, Any]] = None
    image_url: str
    feature_product: bool = False
    visible: bool = True

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    feature_product: bool
    visible: bool
    category_id: int
    variants: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}