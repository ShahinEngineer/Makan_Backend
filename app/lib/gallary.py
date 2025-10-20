from app.models.gallary import Gallary
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schema.gallary import GallaryCreate, GallaryOut

def create_gallary(db: Session, img_url:str) -> Gallary:
    db_gallary = Gallary(img_url = img_url)
    db.add(db_gallary)
    db.commit()
    db.refresh(db_gallary)
    return db_gallary

def getAllGallary(db: Session, skip: int = 0, limit: int = 100) -> List[Gallary]:
    return db.query(Gallary).offset(skip).limit(limit).all()

def getGallaryById(db:Session, gallary_id:int) -> Gallary:
    return db.query(Gallary).filter(Gallary.id == gallary_id).first()

def edit_gallary(db: Session, gallary_id: int, gallary: GallaryOut) -> Optional[Gallary]:
    db_gallary = db.query(Gallary).filter(Gallary.id == gallary_id).first()
    if not db_gallary:
        return None
    update_data = gallary.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_gallary, field, value)
    db.add(db_gallary)
    db.commit()
    db.refresh(db_gallary)
    return db_gallary

def delete_gallary(db: Session, gallary_id: int) -> bool:
    db_gallary = db.query(Gallary).filter(Gallary.id == gallary_id).first()
    if not db_gallary:
        return False
    db.delete(db_gallary)
    db.commit()
    return True

