from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.lesson import Lesson

router = APIRouter()

# get all lessons
@router.get("/")
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()

# get a lesson by its slug
@router.get("/{slug}")
def get_lesson(slug: str, db: Session = Depends(get_db)):
    return db.query(Lesson).filter(Lesson.slug == slug).first()