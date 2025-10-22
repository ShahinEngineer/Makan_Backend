from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app.lib.funs import save_image
from app.routes.category import UPLOAD_DIR
from app.schema.news import NewsCreate, NewsOut
from app.lib.new import create_news, get_all_news, get_news, edit_news, delete_news, get_new_by_lang
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.news import News

router = APIRouter()

UPLOAD_DIR = "app/static/images/news/"

@router.post("/news/", response_model=NewsOut)
def create_news_endpoint(
    title: str= File(...),
    title_ar: str = File(...),
    title_de: str = File(...),
    image: UploadFile = File(...),
    description: str = File(...),
    description_ar: str = File(...),
    description_de: str = File(...),
    content: str = File(...),
    content_ar: str = File(...),
    content_de: str = File(...),
    hash_tags: str = File(...),
    feature_news: bool = File(False),
    db: Session = Depends(get_db)):
    try:
        image_url = save_image(image, UPLOAD_DIR)

        news = NewsCreate(
            title=title,
            title_ar=title_ar,
            title_de=title_de,
            description=description,
            description_ar= description_ar,
            description_de= description_de,
            hash_tags=hash_tags,
            img_url=image_url,
            content=content,
            content_ar=content_ar,
            content_de=content_de,
            feature_news=feature_news
        )
        db_news = create_news(db, news)
        return db_news
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/news/lang/{lang}", response_model=list[NewsOut])
def read_news_by_language(lang: str, db: Session = Depends(get_db)):
    valid = {"en", "de", "ar", "default"}
    try:
        if lang not in valid:
            raise HTTPException(status_code=400, detail=f"Unsupported language '{lang}'")
        result = []
        if lang == "en" or lang == "default":
            result = get_all_news(db)
        else:
            result = get_new_by_lang(db, lang)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/news/{news_id}", response_model=NewsOut)
def read_news_endpoint(news_id: int, db: Session = Depends(get_db)):
    news = get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.get("/news/", response_model=list[NewsOut])
def read_all_news_endpoint(db: Session = Depends(get_db)):
    news_list = get_all_news(db)
    return news_list
@router.put("/news/{news_id}", response_model=NewsOut)
def update_news_endpoint(
    news_id: int,
    name: str = File(...),
    image: UploadFile = File(None),
    description: str = File(...),
    content: str = File(...),
    hash_tags: str = File(...),
    feature_news: bool = File(False),
    db: Session = Depends(get_db)):

    news = get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    updated_data = {
        "title": name,
        "description": description,
        "content": content,
        "hash_tags": hash_tags,
        "feature_news": feature_news
    }

    # Save new image and delete old one if a new image is provided
    if image:
        image_path = save_image(image, UPLOAD_DIR)
        if news.img_url:
            # Optionally, add code to delete the old image file if needed
            pass
        updated_data["img_url"] = image_path

    updated_news = edit_news(db, news_id, updated_data)
    if not updated_news:
        raise HTTPException(status_code=400, detail="Failed to update news")
    return updated_news

@router.delete("/news/{news_id}", response_model=NewsOut)
def delete_news_endpoint(news_id: int, db: Session = Depends(get_db)):
    news = get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    deleted_news = delete_news(db, news_id)
    if not deleted_news:
        raise HTTPException(status_code=400, detail="Failed to delete news")
    return deleted_news