from app.models.categorie import Category
from app.schema.category import CategoryCreate
from sqlalchemy.orm import Session
from app.models.product import Product

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(name=category.name, image_url=category.image_url)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()

def get_categories_with_product_images(db: Session) -> list[dict]:
    # Join categories with products
    results = (
        db.query(
            Category.id,
            Category.name,
            Category.image_url.label("category_image"),
            Product.image_url.label("product_image")
        )
        .outerjoin(Product, Product.category_id == Category.id)
        .order_by(Category.id, Product.created_at)  # order products by created_at
        .all()
    )

    # Group images by category, pick at most 3
    categories = {}
    for r in results:
        if r.id not in categories:
            categories[r.id] = {
                "id": r.id,
                "name": r.name,
                "category_image": r.category_image,
                "product_images": []
            }

        if r.product_image and len(categories[r.id]["product_images"]) < 3:
            categories[r.id]["product_images"].append(r.product_image)

    return list(categories.values())

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