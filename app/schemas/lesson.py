from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict

class LessonBase(BaseModel):
    title: str
    content: Dict[str, Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None