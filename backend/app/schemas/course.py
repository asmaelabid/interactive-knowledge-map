from pydantic import BaseModel
from typing import Optional, List

class CourseBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
    class Config:
        from_attributes = True 