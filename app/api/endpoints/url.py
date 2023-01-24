import secrets

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.api.schemas import CreateUrlRequest, CreateUrlResponse
from app.domain import Url as UrlDomainModel
from app.repositories import UrlRepository

router = APIRouter(
    prefix="/url",
    tags=["url"],
)


@router.post(
    "/",
    summary="Create short URL",
    response_model=CreateUrlResponse,
)
async def create_url(url: CreateUrlRequest) -> CreateUrlResponse:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    secret_key = "".join(secrets.choice(chars) for _ in range(8))

    url_domain = UrlDomainModel(
        secret_key=secret_key,
        target_url=url.target_url,
    )

    url_repository = UrlRepository()
    repository_response = await url_repository.create(url_model=url_domain)
    response = CreateUrlResponse(**repository_response.dict())

    return response


@router.get(
    "/{url_key}",
    summary="Redirect to target URL",
    response_class=RedirectResponse,
    status_code=307,
)
async def forward_to_url(url_key: str):
    url_repository = UrlRepository()

    repository_response = await url_repository.get(url_key)

    if repository_response:
        return repository_response.target_url
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested key: '{url_key}' does not exist.",
        )
