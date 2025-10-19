from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.lib.new import get_featured_news
from app.lib.product import get_featured_products, get_all_products
from app.lib.category import get_all_categories, get_categories_with_product_images

router = APIRouter()

@router.get("/home")
def get_all_info(db=Depends(get_db)):
    try:
        all_product = get_all_products(db)
        featured_products = get_featured_products(db)
        categories_with_product_image = get_categories_with_product_images(db)
        featured_news = get_featured_news(db)

        return {
            "all_product": all_product,
            "featured_products": featured_products,
            "categories": categories_with_product_image,
            "featured_news": featured_news
        }

    except Exception as e:
        return {"error": str(e)}


