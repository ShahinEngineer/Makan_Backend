import os
from isort import file
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.schema.category import CategoryCreate, CategoryOut
from app.lib.category import create_category, get_category, get_category_by_name, get_all_categories, edit_category, delete_category
from app.db.session import get_db
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "app/static/images/categories/"

@router.post("/categories/", response_model=CategoryOut)
def create_category_endpoint(
    name: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)):
    try:
        existing_category = get_category_by_name(db, name)
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")

        image_path = None
        if image:
            filename = f"{uuid4().hex}_{image.filename}"
            file_location = f"{UPLOAD_DIR}{filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(image.file.read())
            image_path = file_location
        # Create new category
        category_data = CategoryCreate(name=name, image_url=image_path)
        db_category = create_category(db, category_data)
        return db_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/categories/{category_id}", response_model=CategoryOut)
def read_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/", response_model=list[CategoryOut])
def read_all_categories_endpoint(db: Session = Depends(get_db)):
    categories = get_all_categories(db)
    return categories

@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category_endpoint(category_id: int,
                             name: str = Form(...),
                             image: UploadFile = File(...),
                             db: Session = Depends(get_db)):

    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check for name uniqueness if the name is being updated
    if name != category.name:
        existing_category = get_category_by_name(db, name)
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")

    image_path = category.image_url
    if image:
        filename = f"{uuid4().hex}_{image.filename}"
        file_location = f"{UPLOAD_DIR}{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(image.file.read())
        image_path = file_location
    updated_category = CategoryCreate(name=name, image_url=image_path)
    updated_category = edit_category(db, category_id, updated_category.model_dump())
    if not updated_category:
        raise HTTPException(status_code=400, detail="Failed to update category")
    return updated_category

@router.delete("/categories/{category_id}", response_model=dict)
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    CategoryOut = delete_category(db, category_id)
    # delete image from folder if needed
    if CategoryOut and CategoryOut.image_url:
        try:
            os.remove(CategoryOut.image_url)
        except Exception as e:
            print(f"Error deleting image file: {e}")
    if not CategoryOut:
        raise HTTPException(status_code=404, detail="Category not found or could not be deleted")
    return {"detail": "Category deleted successfully"}