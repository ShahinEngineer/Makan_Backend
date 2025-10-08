from app.models.categorie import Category
from app.schema.category import CategoryCreate
from sqlalchemy.orm import Session

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(name=category.name, image_url=category.image_url)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()

def get_category(db: Session, category_id: int) -> Category:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Category:
    return db.query(Category).filter(Category.name == name).first()

def edit_category(db: Session, category_id: int, updated_data: dict) -> Category | None:
    category = get_category(db, category_id)
    if not category:
        return None
    for key, value in updated_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int) -> Category | None:
    category = get_category(db, category_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category