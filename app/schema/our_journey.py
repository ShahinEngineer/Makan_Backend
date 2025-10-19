import datetime
from pydantic import BaseModel

class OurJourneyCreate(BaseModel):
    story_subtitle: str
    story_description: str
    story_img_url: str
    vision_description: str
    mission_description: str
    mission_vision_img_url: str
    value_description: str
    our_values: dict

class OurJourneySchemaOut(BaseModel):
    id: int
    story_subtitle: str
    story_description: str
    story_img_url: str
    vision_description: str
    mission_description: str
    mission_vision_img_url: str
    value_description: str
    our_values: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {"from_attributes": True}
