from app.models.team import Team
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schema.team import TeamCreate, TeamOut

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

def update_team(db: Session, team_id: int, team_in: TeamCreate) -> Optional[Team]:
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return None
    update_data = team_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(team, key, value)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

def getAll_team(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    return db.query(Team).offset(skip).limit(limit).all()

def getById_team(db: Session, team_id: int) -> Optional[Team]:
    return db.query(Team).filter(Team.id == team_id).first()