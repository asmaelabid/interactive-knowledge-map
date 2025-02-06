import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlalchemy.orm import Session
from app.core.db import sync_engine, SyncSessionLocal
from app.models.course import Course

def seed():
    session = SyncSessionLocal()

    course1 = Course(name="Introduction to Programming")
    course2 = Course(name="Data Structures", parent_id=course1.id)
    course3 = Course(name="Algorithms", parent_id=course2.id)
    course4 = Course(name="Databases")
    course5 = Course(name="Advanced Databases", parent_id=course4.id)
    course6 = Course(name="Machine Learning", parent_id=course3.id)

    course2.prerequisites.append(course1)
    course3.prerequisites.append(course2)
    course5.prerequisites.append(course4)
    course6.prerequisites.append(course3)

    session.add_all([course1, course2, course3, course4, course5, course6])

    session.commit()

    courses = session.query(Course).all()
    for course in courses:
        print(f"Course: {course.name}, Parent: {course.parent_id}, Prerequisites: {[prereq.name for prereq in course.prerequisites]}")

    session.close()

if __name__ == "__main__":
    seed()