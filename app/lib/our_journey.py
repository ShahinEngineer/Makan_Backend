

from http.client import HTTPException

from sqlalchemy.orm import Session
from app.schema.our_journey import OurJourneyCreate
from app.models.ourJourney import OurJourney


def create_our_journey(db: Session, our_journey: OurJourneyCreate) -> OurJourney:
    db_our_journey = OurJourney(
        story_subtitle=our_journey.story_subtitle,
        story_description=our_journey.story_description,
        story_img_url=our_journey.story_img_url,
        vision_description=our_journey.vision_description,
        mission_description=our_journey.mission_description,
        mission_vision_img_url=our_journey.mission_vision_img_url,
        value_description=our_journey.value_description,
        our_values=our_journey.our_values
    )
    db.add(db_our_journey)
    db.commit()
    db.refresh(db_our_journey)
    return db_our_journey

def get_our_journey(db: Session, journey_id: int) -> OurJourney:
    return db.query(OurJourney).filter(OurJourney.id == journey_id).first()

def get_all_our_journeys(db: Session) -> list[OurJourney]:
    return db.query(OurJourney).all()

def edit_our_journey(db: Session, journey_id: int, updated_data: dict) -> OurJourney | None:
    journey = get_our_journey(db, journey_id)
    if not journey:
        return None
    for key, value in updated_data.items():
        setattr(journey, key, value)
    db.commit()
    db.refresh(journey)
    return journey

def delete_our_journey(db: Session, journey_id: int) -> OurJourney | None:
    journey = get_our_journey(db, journey_id)
    if not journey:
        return None
    db.delete(journey)
    db.commit()
    return journey