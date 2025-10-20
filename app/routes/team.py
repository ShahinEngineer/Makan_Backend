from app.lib.funs import delete_file, save_image
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.lib.funs import save_image
from app.schema.team import TeamCreate, TeamOut
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from app.db.session import get_db
from app.lib.funs import save_image, delete_file
from app.lib.team import  create_team, update_team ,delete_team, getAll_team, getById_team
import json
router = APIRouter(prefix="/api/teams", tags=["teams"])

UPLOAD_DIR = "app/static/images/teams/"

@router.post("/", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team_item(
    name: str,
    role: str,
    description: Optional[str],
    email: Optional[str],
    social_media_links: Optional [str],
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """
    Create a team. Optionally accepts an image file.
    """
    image_path = None
    try:
        if image:
            image_path = save_image(image, UPLOAD_DIR)
            social_media_links_json = json.loads(social_media_links)

            team = TeamCreate(
                name=name,
                role=role,
                image_url=image_path,
                description=description,
                email=email,
                social_media_links=social_media_links_json
            )
            created = create_team(db, team)
        return created
    except Exception as e:
        # cleanup saved file on error
        if image_path:
            try:
                delete_file(image_path)
            except Exception:
                pass
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[TeamOut])
def list_teams(db: Session = Depends(get_db)):
    """
    Get all teams.
    """
    try:
        return getAll_team(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{team_id}", response_model=TeamOut)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """
    Get a single team by ID.
    """
    team = getById_team(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=TeamOut)
async def update_team_item(
    team_id: int,
    team: TeamCreate,
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """
    Update a team. If a new image is provided, replaces the old one.
    """
    existing = getById_team(db, team_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    new_image_path = None
    try:
        if image:
            new_image_path = save_image(image)
        updated = (
            update_team(db, team_id, team, new_image_path)
            if new_image_path is not None
            else update_team(db, team_id, team)
        )
        # if update succeeded and a new image was provided, remove the old file
        if new_image_path and getattr(existing, "image", None):
            try:
                delete_file(existing.image)
            except Exception:
                pass
        return updated
    except Exception as e:
        if new_image_path:
            try:
                delete_file(new_image_path)
            except Exception:
                pass
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_item(team_id: int, db: Session = Depends(get_db)):
    """
    Delete a team and its image file if present.
    """
    existing = getById_team(db, team_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    try:
        # attempt to delete record
        delete_team(db, team_id)
        # remove file if present on the model
        if getattr(existing, "image", None):
            try:
                delete_file(existing.image)
            except Exception:
                pass
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



