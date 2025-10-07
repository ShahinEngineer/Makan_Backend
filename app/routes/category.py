from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schema.category import CategoryCreate, CategoryOut
from app.lib.category import create_category, get_category, get_category_by_name, get_all_categories, edit_category, delete_category
from app.db.session import get_db

router = APIRouter()

@router.post("/categories/", response_model=CategoryOut)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        existing_category = get_category_by_name(db, category.name)
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")

        # Create new category
        db_category = create_category(db, category)
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
def update_category_endpoint(category_id: int, updated_data: CategoryCreate, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check for name uniqueness if the name is being updated
    if updated_data.name != category.name:
        existing_category = get_category_by_name(db, updated_data.name)
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")

    updated_category = edit_category(db, category_id, updated_data.model_dump())
    if not updated_category:
        raise HTTPException(status_code=400, detail="Failed to update category")
    return updated_category

@router.delete("/categories/{category_id}", response_model=dict)
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    success = delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or could not be deleted")
    return {"detail": "Category deleted successfully"}