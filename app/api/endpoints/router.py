from fastapi import APIRouter

from app.api.endpoints import url
from app.api.endpoints import qr

api_router = APIRouter(prefix="/api")
api_router.include_router(url.router)
api_router.include_router(qr.router)
