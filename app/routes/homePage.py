from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.lib.new import get_all_news, get_featured_news
from app.lib.product import get_featured_products, get_all_products
from app.lib.category import get_all_categories, get_categories_with_product_images
from app.lib.partner import get_all_partners
from app.lib.gallary import getAllGallary
from app.lib.team import getAll_team

router = APIRouter()

@router.get("/home")
def get_all_info(db=Depends(get_db)):
    try:
        all_product = get_all_products(db)
        featured_products = get_featured_products(db)
        categories_with_product_image = get_categories_with_product_images(db)
        featured_news = get_featured_news(db)
        partners = get_all_partners(db)
        gallary = getAllGallary(db)
        team = getAll_team(db)

        return {
            "all_product": all_product,
            "featured_products": featured_products,
            "categories": categories_with_product_image,
            "featured_news": featured_news,
            "partners": partners,
            "gallary": gallary,
            "teams": team,
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("/admin/all-home-data")
def get_all_home_data(db=Depends(get_db)):
    try:
        products = get_all_products(db)
        categories = get_all_categories(db)
        news = get_all_news(db)
        partners = get_all_partners(db)
        gallery = getAllGallary(db)
        team = getAll_team(db)

        return {
            "products": products,
            "categories": categories,
            "news": news,
            "partners": partners,
            "gallery": gallery,
            "teams": team,
        }

    except Exception as e:
        return {"error": str(e)}


