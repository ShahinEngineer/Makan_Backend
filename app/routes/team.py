from app.lib.funs import delete_file, save_image
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.lib.funs import save_image
from app.schema.team import TeamCreate, TeamOut, TeamOutLang
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from app.db.session import get_db
from app.lib.funs import save_image, delete_file
from app.lib.team import  create_team, update_team ,delete_team, getAll_team, getById_team
import json
router = APIRouter(prefix="/api/teams", tags=["teams"])

UPLOAD_DIR = "app/static/images/teams/"

@router.post("/", response_model=TeamOutLang, status_code=status.HTTP_201_CREATED)
async def create_team_item(
    name: str = Form(...),
    name_ar: str = Form(...),
    name_de: str = Form(...),
    role: str = Form(...),
    role_ar: str = Form(...),
    role_de: str = Form(...),
    description: Optional[str] = Form(None),
    description_ar: Optional[str] = Form(None),
    description_de: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    social_media_links: Optional[str] = Form(None),
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
                name_ar=name_ar,
                name_de=name_de,
                role=role,
                role_ar=role_ar,
                role_de=role_de,
                image_url=image_path,
                description=description,
                description_ar=description_ar,
                description_de=description_de,
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


@router.put("/{team_id}", response_model=TeamOutLang)
async def update_team_item(
    team_id: int,
    name: str = Form(...),
    name_ar: str = Form(...),
    name_de: str = Form(...),
    role: str = Form(...),
    role_ar: str = Form(...),
    role_de: str = Form(...),
    description: Optional[str] = Form(None),
    description_ar: Optional[str] = Form(None),
    description_de: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    social_media_links: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):

    print(social_media_links)
    existing = getById_team(db, team_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    new_image_path = None
    try:
        if image:
            image_path = save_image(image, UPLOAD_DIR)
            social_media_links_json = json.loads(social_media_links)
            print(social_media_links_json, "wew")
            new_image_path = image_path
        else:
            social_media_links_json = json.loads(social_media_links) if social_media_links else existing.social_media_links
        team = TeamCreate(
                name=name,
                name_ar=name_ar,
                name_de=name_de,
                role=role,
                role_ar=role_ar,
                role_de=role_de,
                image_url=new_image_path if new_image_path else existing.image_url,
                description=description,
                description_ar=description_ar,
                description_de=description_de,
                email=email,
                social_media_links=social_media_links_json
            )

        if new_image_path:
            try:
                delete_file(existing.image_url)
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete old image file")
        updated = update_team(db, team_id, team )
        return updated
    except Exception as e:
        if new_image_path:
            try:
                delete_file(new_image_path)
            except Exception:
                pass
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{team_id}",  status_code=status.HTTP_200_OK, response_model=TeamOut)
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
        return existing
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




        # updated = update_team(db, team_id, team )

        # if update succeeded and a new image was provided, remove the old file
        if new_image_path:
            try:
                delete_file(existing.image_url)
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete old image file")
        return existing
    except Exception as e:
        if new_image_path:
            try:
                delete_file(new_image_path)
            except Exception:
                pass
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{team_id}",  status_code=status.HTTP_200_OK, response_model=TeamOut)
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
        return existing
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



