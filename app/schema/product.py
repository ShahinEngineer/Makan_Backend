import datetime
from typing import Any, Dict, Optional, List
from pydantic import BaseModel

from app.schema.category import CategoryOut
from app.schema.news import NewsOut
from app.schema.partner import PartnerOut
from app.schema.gallary import GallaryOut
from app.schema.team import TeamOut

class ProductCreate(BaseModel):
    category_id: int
    name: str
    name_ar: str
    name_de: str
    description: str
    description_ar: str
    description_de: str
    variants: Optional[Dict[str, Any]] = None
    image_url: str
    feature_product: bool = False
    visible: bool = True

class ProductOut(BaseModel):
    id: int
    name: str
    name_ar: str
    name_de: str
    description: str
    description_ar: str
    description_de: str
    image_url: str
    feature_product: bool
    visible: bool
    category_id: int
    variants: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}



class ProductOutWihOutLang(BaseModel):
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


class HomeResponse(BaseModel):
    all_product: List[ProductOut]
    featured_products: List[ProductOut]
    categories: List[CategoryOut]
    featured_news: List[NewsOut]
    partners: List[PartnerOut]
    gallary: List[GallaryOut]
    teams: List[TeamOut]