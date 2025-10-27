from app.models.team import Team
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schema.team import TeamCreate, TeamOut, TeamOutLang

def create_team(db: Session, team_in: TeamCreate) -> Team:
    db_team = Team(**team_in.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int) -> bool:
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return False
    db.delete(team)
    db.commit()
    return True

def update_team(db: Session, team_id: int, team_in: TeamCreate) -> Optional[TeamOutLang]:
    existing = db.query(Team).filter(Team.id == team_id).first()
    if not existing:
        return None
    update_data = team_in.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(existing, key, value)
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing

def getAll_team(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    return db.query(Team).offset(skip).limit(limit).all()

def getById_team(db: Session, team_id: int) -> Optional[TeamOutLang]:
    return db.query(Team).filter(Team.id == team_id).first()