import json
import os
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.database import engine, Base
from app.models.lesson import Lesson

LESSONS_DIR = "./app/data/lessons"

Base.metadata.create_all(bind=engine)

def load_lessons():
    db: Session = SessionLocal()

    try:
        for filename in os.listdir(LESSONS_DIR):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(LESSONS_DIR, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # --- Basic validation ---
            if "title" not in data or "content" not in data:
                print(f"Skipping {filename}: missing required fields")
                continue

            # --- Prevent duplicates (by slug ideally) ---
            existing = db.query(Lesson).filter(
                Lesson.slug == data.get("slug")
            ).first()

            if existing:
                print(f"Lesson already exists: {data.get('slug')}")
                continue

            # --- Create lesson ---
            lesson = Lesson(
                title=data["title"],
                slug=data.get("slug"),
                level=data.get("level"),
                description=data.get("description"),
                tags=data.get("tags"),
                image=data.get("image"),
                content=data["content"]
            )

            db.add(lesson)
            print(f"Added: {data['title']}")

        db.commit()
        print("Seeding complete")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    load_lessons()