from app.lib.funs import delete_file, save_image
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.lib.funs import save_image
from app.schema.category import CategoryCreate, CategoryOut
from app.lib.category import create_category, get_category, get_category_by_name, get_all_categories, edit_category, delete_category
from app.db.session import get_db

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

        image_path = save_image(image, UPLOAD_DIR)
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

    # Save new image and delete old one if a new image is provided
    if image:
        image_path = save_image(image, UPLOAD_DIR)
        if category.image_url:
            try:
                delete_file(category.image_url)
            except Exception as e:
                print(f"Error deleting old image file: {e}")
    else:
        image_path = category.image_url # Keep existing image if no new image is provided

    updated_category = CategoryCreate(name=name, image_url=image_path)
    updated_category = edit_category(db, category_id, updated_category.model_dump())
    if not updated_category:
        raise HTTPException(status_code=400, detail="Failed to update category")
    return updated_category

@router.delete("/categories/{category_id}", response_model=CategoryOut)
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    CategoryOut = None
    try:
        CategoryOut = delete_category(db, category_id)
    except Exception as e:
         raise HTTPException(status_code=404, detail="can't delete category with products")
    # delete image from folder if needed
    if CategoryOut and CategoryOut.image_url:
        try:
            delete_file(CategoryOut.image_url)
            return CategoryOut
        except Exception as e:
            print(f"Error deleting image file: {e}")
    if not CategoryOut:
        raise HTTPException(status_code=404, detail="Category not found or could not be deleted")
    return {"detail": "Category deleted successfully"}