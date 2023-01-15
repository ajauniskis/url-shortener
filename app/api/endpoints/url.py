import secrets

from fastapi import APIRouter

from app.api.schemas import CreateUrlRequest, CreateUrlResponse
from app.domain import Url as UrlDomainModel
from app.repositories import UrlRepository

router = APIRouter(
    prefix="/url",
    tags=["url"],
)

url_repository = UrlRepository()


@router.post(
    "/",
    summary="Create short URL",
    response_model=CreateUrlResponse,
)
async def create_url(url: CreateUrlRequest):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    secret_key = "".join(secrets.choice(chars) for _ in range(8))

    url_domain = UrlDomainModel(
        secret_key=secret_key,
        target_url=url.target_url,
    )

    response = await url_repository.create_url(url_model=url_domain)

    return response
