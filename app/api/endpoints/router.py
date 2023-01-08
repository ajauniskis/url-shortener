from fastapi import APIRouter

from app.api.endpoints import url

api_router = APIRouter(prefix="/api")
api_router.include_router(url.router)
