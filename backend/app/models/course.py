from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from app.core.db import Base

course_prerequisite = Table(
    "course_prerequisite",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("course.id"), primary_key=True),
    Column("prerequisite_id", Integer, ForeignKey("course.id"), primary_key=True),
)

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("course.id"), nullable=True)
    children = relationship("Course", backref=backref("parent", remote_side=[id]))

    prerequisites = relationship(
        "Course",
        secondary=course_prerequisite,
        primaryjoin=id == course_prerequisite.c.course_id,
        secondaryjoin=id == course_prerequisite.c.prerequisite_id,
        backref="dependents",
    )
