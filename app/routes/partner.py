from app.lib.funs import delete_file, save_image
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.lib.funs import save_image
from app.schema.partner import CreatePartner, PartnerOut
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from app.db.session import get_db
from app.lib.funs import save_image, delete_file
from app.lib.partner import  create_partner, get_all_partners ,get_partner_by_id, update_partner, delete_partner

router = APIRouter(prefix="/api/partners", tags=["partners"])


UPLOAD_DIR = "app/static/images/partner/"

@router.post("/", response_model=PartnerOut, status_code=status.HTTP_201_CREATED)
def create_partner_endpoint(
    name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    image_path = None
    if file:
        try:
            image_path = save_image(file, UPLOAD_DIR)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save image")
    try:
        # create_partner(db, partner, image_path) is expected to accept (db, partner, image_path)

        created = create_partner(db, image_url=image_path, name=name)
        return created
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))




@router.get("/", response_model=List[PartnerOut])
def get_partners(db: Session = Depends(get_db)):
    return get_all_partners(db)


@router.put("/{partner_id}", response_model=PartnerOut)
def update_partner_endpoint(
    partner_id: int,
    partner: CreatePartner,
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    existing = get_partner_by_id(db, partner_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found")

    image_path = getattr(existing, "image", None)
    if file:
        # remove old file if present, then save new one
        try:
            if image_path:
                delete_file(image_path)
        except Exception:
            # non-fatal: log in real app, continue to attempt save
            pass
        try:
            image_path = save_image(file)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save new image")

    try:
        updated = update_partner(db, partner_id, partner, image_path)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    return updated


@router.delete("/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partner_endpoint(partner_id: int, db: Session = Depends(get_db)):
    existing = get_partner_by_id(db, partner_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found")

    img = getattr(existing, "image", None)
    if img:
        try:
            delete_file(img)
        except Exception:
            # non-fatal: continue with deletion of DB record
            pass

    try:
        delete_partner(db, partner_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    return None
