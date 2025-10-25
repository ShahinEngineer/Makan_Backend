from app.lib.funs import delete_file, save_image
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.lib.funs import save_image
from app.schema.gallary import GallaryCreate, GallaryOut
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from app.db.session import get_db
from app.lib.funs import save_image, delete_file
from app.lib.gallary import  create_gallary, getAllGallary,getGallaryById,edit_gallary,delete_gallary

router = APIRouter(prefix="/api/gallary", tags=["gallary"])

UPLOAD_DIR = "app/static/images/gallary/"

@router.post("/", response_model=GallaryCreate, status_code=status.HTTP_201_CREATED)
def create_new_gallary(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = save_image(image, UPLOAD_DIR)

    db_item = create_gallary(db,filename)
    return db_item


@router.get("/", response_model=List[GallaryOut])
def get_all_gallaries(db: Session = Depends(get_db)):
    items = getAllGallary(db)
    return items


@router.get("/{item_id}", response_model=GallaryOut)
def get_gallary(item_id: int, db: Session = Depends(get_db)):
    item = getGallaryById(db,item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery item not found")
    return item


@router.put("/{item_id}", response_model=GallaryOut)
def edit_gallary_item(
    item_id: int,
    image: Optional[UploadFile] = File(None),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    item = getGallaryById(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery item not found")

    new_filename = None
    if image is not None:
        new_filename = save_image(image, UPLOAD_DIR)

    # Call library edit function. It should handle None values if no update for that field.
    updated = edit_gallary(db, item_id, new_filename, title)

    # If a new file was saved successfully, delete the old file from disk
    if new_filename:
        try:
            delete_file(item.image, UPLOAD_DIR)
        except Exception:
            # ignore file deletion errors
            pass

    return updated


@router.delete("/{item_id}", response_model=GallaryOut)
def remove_gallary(item_id: int, db: Session = Depends(get_db)):
    try:
        item = getGallaryById(db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery item not found")
        delete_gallary(db, item_id)
        if item.img_url:
            delete_file(item.img_url)
        return item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete image gallery item: " + str(e))