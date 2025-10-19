from app.models.news import News
from app.schema.news import NewsCreate
from sqlalchemy.orm import Session

def create_news(db: Session, news: NewsCreate) -> News:
    db_news = News(
        title=news.title,
        description=news.description,
        hash_tags=news.hash_tags,
        content=news.content,
        img_url=news.img_url,
        feature_news=news.feature_news
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def get_all_news(db: Session) -> list[News]:
    return db.query(News).all()

def get_featured_news(db: Session) -> list[News]:
    return db.query(News).filter(News.feature_news == True).all()

def get_news(db: Session, news_id: int) -> News:
    return db.query(News).filter(News.id == news_id).first()

def edit_news(db: Session, news_id: int, updated_data: dict) -> News | None:
    news = get_news(db, news_id)
    if not news:
        return None
    for key, value in updated_data.items():
        setattr(news, key, value)
    db.commit()
    db.refresh(news)
    return news

def delete_news(db: Session, news_id: int) -> News | None:
    news = get_news(db, news_id)
    if not news:
        return None
    db.delete(news)
    db.commit()
    return news