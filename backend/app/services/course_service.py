from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.course import Course
from app.schemas.course import CourseCreate

class CourseService:
    @staticmethod
    async def get_course(db: AsyncSession, course_id: int):
        query = select(Course).where(Course.id == course_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_courses(db: AsyncSession, skip: int = 0, limit: int = 100):
        query = select(Course).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create_course(db: AsyncSession, course: CourseCreate):
        try:
            db_course = Course(**course.model_dump())
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
            for key, value in course.model_dump().items():
                setattr(db_course, key, value)
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