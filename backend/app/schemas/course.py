from pydantic import BaseModel
from typing import Optional, List

class CourseBase(BaseModel):
    name: str
    parent_name: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    parent_id: Optional[int] = None
    parent_name: Optional[str] = None

    class Config:
        from_attributes = True 