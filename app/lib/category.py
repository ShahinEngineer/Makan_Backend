from app.models.categorie import Category
from app.schema.category import CategoryCreate, CategoryCreateLang, CategoryOutLang
from sqlalchemy.orm import Session
from app.models.product import Product
from sqlalchemy import text

def create_category(db: Session, category: CategoryCreateLang) -> Category:
    db_category = Category(name=category.name, name_ar=category.name_ar, name_de=category.name_de, image_url=category.image_url)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def get_category_by_lang(db: Session, lang: str) -> list[Category]:
    query = text(f"""
        SELECT
            id,
            name_{lang} AS name,
            image_url,
            created_at,
            updated_at
        FROM categories
    """)
    rows = db.execute(query).fetchall()

    return rows

def get_category_by_lang_v1(db: Session, lang: str) -> list[Category]:
    query = text(f"""
        SELECT
            id,
            name_{lang} AS name,
            image_url,
            created_at,
            updated_at
        FROM categories
    """)
    rows = db.execute(query).mappings().all()  # ✅ returns dicts, not tuples
    return [dict(row) for row in rows]

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

def get_categories_with_product_images_by_lang(db: Session, lang: str) -> list[dict]:
    # ✅ Validate supported languages
    valid_langs = {"en", "ar", "de", "default"}
    if lang not in valid_langs:
        raise ValueError(f"Unsupported language: {lang}")

    # ✅ Determine which name column to select
    name_column = f"name_{lang}" if lang in {"ar", "de"} else "name"

    # ✅ Raw SQL with JOIN
    query = text(f"""
        SELECT
            c.id AS category_id,
            c.{name_column} AS category_name,
            c.image_url AS category_image,
            p.image_url AS product_image
        FROM categories c
        LEFT JOIN products p ON p.category_id = c.id
        ORDER BY c.id, p.created_at
    """)

    rows = db.execute(query).mappings().all()  # returns dict-like mappings

    # ✅ Group images by category
    categories = {}
    for r in rows:
        cid = r["category_id"]
        if cid not in categories:
            categories[cid] = {
                "id": cid,
                "name": r["category_name"],
                "category_image": r["category_image"],
                "product_images": [],
            }

        if r["product_image"] and len(categories[cid]["product_images"]) < 3:
            categories[cid]["product_images"].append(r["product_image"])

    return list(categories.values())
def get_category(db: Session, category_id: int) -> Category:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Category:
    return db.query(Category).filter(Category.name == name).first()

def edit_category(db: Session, category_id: int, updated_data: dict) -> CategoryOutLang :
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