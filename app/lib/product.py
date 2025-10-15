from os import name
from app.models.product import Product
from sqlalchemy.orm import Session

from app.schema.product import ProductCreate


def create_product(db: Session, create_product: ProductCreate) -> Product:
    db_product = Product(name=create_product.name,
                         image_url=create_product.image_url,
                         description=create_product.description,
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
