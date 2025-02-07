from fastapi import FastAPI
from app.api.router.router import router, setup_cors

app = FastAPI(
    title="Knowledge Map API",
    description="API for managing courses and their relationships",
    version="1.0.0"
)

setup_cors(app)

app.include_router(router)