from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.course import router as course_router

router = APIRouter()

router.include_router(
    course_router,
    prefix="/api/v1",
    tags=["courses"]
)

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "https://interactive-knowledge-map.vercel.app"
]

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )