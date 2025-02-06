from fastapi import FastAPI
from app.api.endpoints import course


app = FastAPI()
app.include_router(course.router, tags=["courses"])