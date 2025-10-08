from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schema.news import NewsCreate
from app.lib.new import create_news, get_all_news, get_news, edit_news, delete_news
from app.db.session import get_db

router = APIRouter()

@router.post("/news/", response_model=NewsCreate)
def create_news_endpoint(news: NewsCreate, db: Session = Depends(get_db)):
    try:
        db_news = create_news(db, news)
        return db_news
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))