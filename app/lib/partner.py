from app.models.partner import Partner
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schema.partner import CreatePartner, PartnerOut

def create_partner(db: Session, image_url:str, name:str) -> PartnerOut:
    partner = Partner(name=name, image_url=image_url)
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


def update_partner(db: Session, partner_id: int, partner_in: CreatePartner) -> Optional[PartnerOut]:
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        return None
    update_data = partner_in.dict(exclude_unset=True)
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