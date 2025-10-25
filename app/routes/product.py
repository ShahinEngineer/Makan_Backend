import json
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Form, HTTPException, UploadFile
from app.lib.funs import delete_file, save_image
from app.schema.product import ProductCreate, ProductOut
from app.lib.product import create_product, delete_product, edit_product, get_product, get_all_products
from app.db.session import get_db
from typing import Dict

router = APIRouter()
UPLOAD_DIR = "app/static/images/products/"

@router.post("/product/", response_model=ProductOut)
def create_product_endpoint(
    name: str = Form(...),
    image: UploadFile = File(...),
    description: str = Form(...),
    category_id: int = Form(...),
    feature_product: bool = Form(False),
    visible: bool = Form(True),
    variants: str = Form(...),  # Expecting a comma-separated string for variants
    db: Session = Depends(get_db)):
    try:
        variants_dict = json.loads(variants)
        image_path = save_image(image, UPLOAD_DIR)  # Ensure you have a function to save the image and return its path
        product_create =  ProductCreate(name=name, image_url=image_path, description=description, category_id=category_id, feature_product=feature_product, visible=visible, variants=variants_dict)
        db_product = create_product(db, product_create)
        return db_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Additional endpoints for products can be added here (e.g., get, update, delete)
@router.get("/product/{product_id}", response_model=ProductCreate)
def read_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/", response_model=list[ProductOut])
def read_all_products_endpoint(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products

# You can add update and delete endpoints similarly
@router.put("/product/{product_id}", response_model=ProductOut)
def update_product_endpoint(
    product_id: int,
    name: str = Form(...),
    image: UploadFile = File(None),
    description: str = Form(...),
    category_id: int = Form(...),
    feature_product: bool = Form(False),
    visible: bool = Form(True),
    variants: str = Form(...),  # Expecting a comma-separated string for variants
    db: Session = Depends(get_db)):

    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        variants_dict = json.loads(variants)
        updated_data = {
            "name": name,
            "description": description,
            "category_id": category_id,
            "feature_product": feature_product,
            "visible": visible,
            "variants": variants_dict
        }

        if image:
            image_path = save_image(image, UPLOAD_DIR)
            updated_data["image_url"] = image_path

        updated_product = edit_product(db, product_id, updated_data)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found after update")
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/product/{product_id}", response_model=ProductOut)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    print("Deleting product endpoint called for ID:", product_id)
    try:
        print("Attempting to delete product with ID:", product_id)
        product = get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        deleted_product = None
        if product.image_url:
            delete_file(product.image_url)
            deleted_product = delete_product(db, product_id)
            return deleted_product
        if not deleted_product:
            raise HTTPException(status_code=400, detail="Failed to delete product")
        return {"detail": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to delete product error: " + str(e))
