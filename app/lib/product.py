from os import name
from app.models.product import Product
from sqlalchemy.orm import Session
from app.schema.product import ProductCreate
from sqlalchemy import text

def create_product(db: Session, create_product: ProductCreate) -> Product:
    db_product = Product(name=create_product.name,
                         name_ar = create_product.name_ar,
                         name_de = create_product.name_de,
                         image_url=create_product.image_url,
                         description=create_product.description,
                         description_ar=create_product.description_ar,
                         description_de=create_product.description_de,
                         category_id=create_product.category_id,
                         feature_product=create_product.feature_product,
                         visible=create_product.visible,
                         variants=create_product.variants)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def get_products_by_lang(db: Session, lang: str) -> list[Product]:
    query = text(f"""
        SELECT
            id,
            name_{lang} AS name,
            category_id,
            feature_product,
            variants,
            visible,
            created_at,
            updated_at,
            description_{lang} AS description,
            image_url,
            created_at,
            updated_at
        FROM products
    """)
    rows = db.execute(query).fetchall()

    return rows

def get_products_by_lang_v1(db: Session, lang: str) -> list[Product]:
    query = text(f"""
        SELECT
            id,
            name_{lang} AS name,
            category_id,
            feature_product,
            variants,
            visible,
            created_at,
            updated_at,
            description_{lang} AS description,
            image_url,
            created_at,
            updated_at
        FROM products
    """)
    rows = db.execute(query).mappings().all()  # ✅ returns dicts, not tuples
    return [dict(row) for row in rows]

def get_featured_products(db: Session) -> list[Product]:
    return db.query(Product).filter(Product.feature_product == True).all()

def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

def edit_product(db: Session, product_id: int, updated_data: dict) -> Product | None:
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in updated_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> Product | None:
    product = get_product(db, product_id)
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product
