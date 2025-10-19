from webbrowser import get
from app.lib.our_journey import create_our_journey, get_our_journey, get_all_our_journeys, edit_our_journey, delete_our_journey
from app.schema.our_journey import OurJourneyCreate, OurJourneySchemaOut
from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.lib.funs import save_image
from sqlalchemy.orm import Session
from typing import List
import json

router = APIRouter()
UPLOAD_DIR = "app/static/images/our_journey/"
@router.post("/our_journey/", response_model=OurJourneySchemaOut)
def create_our_journey_endpoint(
    story_subtitle: str = Form(...),
    story_description: str = Form(...),
    story_img: UploadFile = File(...),
    vision_description: str = Form(...),
    mission_description: str = Form(...),
    mission_vision_img: UploadFile = File(...),
    value_description: str = Form(...),
    our_values_images: List[UploadFile] = File(...),
    our_values: str = Form(...),  # Expecting a JSON string for our_values
    db: Session = Depends(get_db)):
    try:
        our_values_dict = json.loads(our_values)
        story_img_url = save_image(story_img, UPLOAD_DIR)
        mission_vision_img_url = save_image(mission_vision_img, UPLOAD_DIR)
        our_values_img_urls = [save_image(img, UPLOAD_DIR) for img in our_values_images]
        our_values_dict['images'] = our_values_img_urls

        our_journey_data = OurJourneyCreate(
            story_subtitle=story_subtitle,
            story_description=story_description,
            story_img_url=story_img_url,
            vision_description=vision_description,
            mission_description=mission_description,
            mission_vision_img_url=mission_vision_img_url,
            value_description=value_description,
            our_values=our_values_dict
        )
        db_our_journey = create_our_journey(db, our_journey_data)
        return db_our_journey
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/our_journey/{journey_id}", response_model=OurJourneySchemaOut)
def read_our_journey_endpoint(journey_id: int, db: Session = Depends(get_db)):
    journey = get_our_journey(db, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Our Journey not found")
    return journey

@router.get("/our_journeys/", response_model=list[OurJourneySchemaOut])
def read_all_our_journeys_endpoint(db: Session = Depends(get_db)):
    journeys = get_all_our_journeys(db)
    return journeys

@router.put("/our_journey/{journey_id}", response_model=OurJourneySchemaOut)
def update_our_journey_endpoint(
    journey_id: int,
    story_subtitle: str = Form(...),
    story_description: str = Form(...),
    story_img: UploadFile = File(None),
    vision_description: str = Form(...),
    mission_description: str = Form(...),
    mission_vision_img: UploadFile = File(None),
    value_description: str = Form(...),
    our_values_images: List[UploadFile] = File(None),
    our_values: str = Form(...),  # Expecting a JSON string for our_values
    db: Session = Depends(get_db)):
    journey = get_our_journey(db, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Our Journey not found")
    try:
        our_values_dict = json.loads(our_values)

        # Save new images if provided, else keep existing ones
        story_img_url = save_image(story_img, UPLOAD_DIR) if story_img else journey.story_img_url
        mission_vision_img_url = save_image(mission_vision_img, UPLOAD_DIR) if mission_vision_img else journey.mission_vision_img_url

        if our_values_images:
            our_values_img_urls = [save_image(img, UPLOAD_DIR) for img in our_values_images]
            our_values_dict['images'] = our_values_img_urls
        else:
            our_values_dict['images'] = journey.our_values.get('images', [])

        updated_data = OurJourneyCreate(
            story_subtitle=story_subtitle,
            story_description=story_description,
            story_img_url=story_img_url,
            vision_description=vision_description,
            mission_description=mission_description,
            mission_vision_img_url=mission_vision_img_url,
            value_description=value_description,
            our_values=our_values_dict
        )
        updated_journey = edit_our_journey(db, journey_id, updated_data)
        return updated_journey
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/our_journey/{journey_id}", response_model=dict)
def delete_our_journey_endpoint(journey_id: int, db: Session = Depends(get_db)):
    journey = get_our_journey(db, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Our Journey not found")
    try:
        delete_our_journey(db, journey_id)
        return {"detail": "Our Journey deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))