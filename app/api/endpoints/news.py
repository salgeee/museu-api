from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_active_user, get_admin_user, get_db
from app.models.news import News
from app.models.user import User
from app.schemas.news import NewsCreate, NewsInDB, NewsUpdate

router = APIRouter()


@router.get("/", response_model=List[NewsInDB])
async def read_news(
        skip: int = 0,
        limit: int = 100,
        published_only: bool = True,
        category: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """
    Retrieve news articles
    """
    query = db.query(News)

    if published_only:
        query = query.filter(News.is_published == True)

    if category:
        query = query.filter(News.category == category)

    news = query.offset(skip).limit(limit).all()
    return news


@router.get("/{news_id}", response_model=NewsInDB)
async def read_news_item(news_id: int, db: Session = Depends(get_db)):
    """
    Get news by ID
    """
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )
    return news


@router.post("/", response_model=NewsInDB)
async def create_news(
        news_in: NewsCreate,
        current_user: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """
    Create new news article (admin only)
    """
    news = News(
        **news_in.dict(),
        author_id=current_user.id
    )

    db.add(news)
    db.commit()
    db.refresh(news)

    return news


@router.put("/{news_id}", response_model=NewsInDB)
async def update_news(
        news_id: int,
        news_in: NewsUpdate,
        current_user: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """
    Update news article (admin only)
    """
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )

    # Update fields
    update_data = news_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(news, field, value)

    # If publishing, set published_at
    if news_in.is_published and not news.is_published:
        news.published_at = datetime.utcnow()

    db.commit()
    db.refresh(news)

    return news


@router.delete("/{news_id}")
async def delete_news(
        news_id: int,
        current_user: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """
    Delete news article (admin only)
    """
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )

    db.delete(news)
    db.commit()

    return {"message": "News deleted successfully"}