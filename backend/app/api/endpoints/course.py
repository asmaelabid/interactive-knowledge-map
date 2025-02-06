from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.db import get_db
from app.schemas.course import Course, CourseCreate
from app.services.course_service import CourseService

router = APIRouter()

@router.post("/courses/", response_model=Course)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await CourseService.create_course(db=db, course=course)

@router.get("/courses/", response_model=List[Course])
async def read_courses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    courses = await CourseService.get_courses(db, skip=skip, limit=limit)
    return courses

@router.get("/courses/{course_id}", response_model=Course)
async def read_course(course_id: int, db: AsyncSession = Depends(get_db)):
    db_course = await CourseService.get_course(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.put("/courses/{course_id}", response_model=Course)
async def update_course(course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = await CourseService.update_course(db, course_id, course)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/courses/{course_id}", response_model=Course)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    db_course = await CourseService.delete_course(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course