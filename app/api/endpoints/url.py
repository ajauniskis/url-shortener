from fastapi import APIRouter
from app.api.schemas import URLBase

router = APIRouter(
    prefix="/url",
    tags=["url"],
)


@router.post(
    "/",
    summary="Create short URL",
)
def create_url(url: URLBase):

    return "Not implemented yet"
