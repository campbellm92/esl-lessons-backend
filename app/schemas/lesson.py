from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema for task
class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None