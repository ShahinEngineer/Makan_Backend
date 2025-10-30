from app.models.partner import Partner
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schema.partner import CreatePartner, PartnerOut, PartnerOutLang

def create_partner(db: Session, image_url:str, name:str, name_ar:str, name_de:str) -> PartnerOut:
    partner = Partner(name=name, image_url=image_url, name_ar=name_ar, name_de=name_de)
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

def get_all_partners(db: Session) -> List[PartnerOut]:
    partners = db.query(Partner).all()
    return partners


def get_partner_by_id(db: Session, partner_id: int) -> Optional[PartnerOut]:
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    return partner


def update_partner(db: Session, partner_id: int, name, name_ar, name_de, image_url) -> PartnerOutLang:
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        return None
    update_data = {
        "image_url": image_url,
        "name": name,
        "name_ar": name_ar,
        "name_de": name_de,
    }
    for field, value in update_data.items():
        setattr(partner, field, value)
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

def delete_partner(db: Session, partner_id: int) -> bool:
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        return False
    db.delete(partner)
    db.commit()
    return True