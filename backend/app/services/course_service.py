from fastapi import HTTPException
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.course import Course
from app.schemas.course import CourseCreate

class CourseService:
    @staticmethod
    async def get_course(db: AsyncSession, course_id: int):
        query = select(Course).where(Course.id == course_id)
        result = await db.execute(query)
        course = result.scalar_one_or_none()
    
        if course and course.parent_id:
            parent_query = select(Course).where(Course.id == course.parent_id)
            parent_result = await db.execute(parent_query)
            parent = parent_result.scalar_one_or_none()
            if parent:
                course.parent_name = parent.name
    
        return course
 
    @staticmethod
    async def get_courses(db: AsyncSession, skip: int = 0, limit: int = 100):
        query = select(Course).offset(skip).limit(limit)
        result = await db.execute(query)
        courses = result.scalars().all()
    
        for course in courses:
            if course.parent_id:
                parent_query = select(Course).where(Course.id == course.parent_id)
                parent_result = await db.execute(parent_query)
                parent = parent_result.scalar_one_or_none()
                if parent:
                    course.parent_name = parent.name
        return courses
    
    @staticmethod
    async def create_course(db: AsyncSession, course: CourseCreate):
        try:
            existing_course = await db.execute(
                select(Course).where(Course.name == course.name)
            )
            if existing_course.scalar_one_or_none():
                raise HTTPException(
                    status_code=400,
                    detail=f"Course with name '{course.name}' already exists"
                )

            course_data = {"name": course.name}

            if course.parent_name:
                parent_course = await db.execute(
                    select(Course).where(Course.name == course.parent_name)
                )
                parent = parent_course.scalar_one_or_none()
                if not parent:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Parent course '{course.parent_name}' not found"
                    )
                course_data["parent_id"] = parent.id

            db_course = Course(**course_data)
            db.add(db_course)
            await db.commit()
            await db.refresh(db_course)
            return db_course
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def update_course(db: AsyncSession, course_id: int, course: CourseCreate):
        db_course = await CourseService.get_course(db, course_id)
        if db_course:
            if course.name != db_course.name:
                existing_course = await db.execute(
                    select(Course).where(Course.name == course.name)
                )
                if existing_course.scalar_one_or_none():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Course with name '{course.name}' already exists"
                    )

            db_course.name = course.name

            if course.parent_name:
                parent_course = await db.execute(
                    select(Course).where(Course.name == course.parent_name)
                )
                parent = parent_course.scalar_one_or_none()
                if not parent:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Parent course '{course.parent_name}' not found"
                    )
                db_course.parent_id = parent.id
            else:
                db_course.parent_id = None

            await db.commit()
            await db.refresh(db_course)
        return db_course

    
    @staticmethod
    async def delete_course(db: AsyncSession, course_id: int):
        db_course = await CourseService.get_course(db, course_id)
        if db_course:
            await db.delete(db_course)
            await db.commit()
        return db_course

    @staticmethod
    async def get_course_dependencies(db: AsyncSession, course_id: int):
        query = text("""
            WITH RECURSIVE course_dependencies AS (
                SELECT id, name, parent_id
                FROM course
                WHERE id = :course_id
                UNION ALL
                SELECT c.id, c.name, c.parent_id
                FROM course c
                INNER JOIN course_dependencies cd ON c.id = cd.parent_id
            )
            SELECT * FROM course_dependencies
            WHERE id != :course_id;
        """)
        result = await db.execute(query, {"course_id": course_id})
        return result.fetchall()

    @staticmethod
    async def get_courses_by_parent_id(db: AsyncSession, parent_id: int):
        query = select(Course).where(Course.parent_id == parent_id)
        result = await db.execute(query)
        return result.scalars().all()