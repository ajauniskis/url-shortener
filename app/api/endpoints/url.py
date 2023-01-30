from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.api.schemas import AdminUrlResponse, CreateUrlRequest, CreateUrlResponse
from app.domain import SecretKey
from app.domain import Url as UrlDomainModel
from app.domain.exception import UrlIsActiveException, UrlIsNotActiveException
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
    url_repository = UrlRepository()

    url_domain = UrlDomainModel(
        secret_key=await SecretKey.generate_unique(url_repository),
        target_url=url.target_url,
    )

    create_response = await url_repository.create(model=url_domain)
    admin_response = await get_admin_info(create_response.secret_key)
    return CreateUrlResponse(**admin_response.dict())


@router.get(
    "/{url_key}",
    summary="Redirect to target URL",
    response_class=RedirectResponse,
    status_code=307,
)
async def forward_to_url(url_key: str):
    url_repository = UrlRepository()

    if url := await url_repository.get(url_key):
        if url.is_active:
            await url.click()
            await url_repository.update(url)

            return url.target_url
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Requested key: '{url_key}' is not active.",
            )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested key: '{url_key}' does not exist.",
        )


@router.get(
    "/admin/{secret_key}",
    summary="Administration info",
    response_model=AdminUrlResponse,
)
async def get_admin_info(secret_key: str) -> AdminUrlResponse:
    url_repository = UrlRepository()

    if url := await url_repository.get_by_secret_key(secret_key):
        response = AdminUrlResponse(
            **url.dict(),
            url=url.short_url,
        )
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested secret key: '{secret_key}' does not exist.",
        )


@router.post(
    "/admin/activate/{secret_key}",
    summary="Activate short URL",
    response_model=AdminUrlResponse,
)
async def activate_url(secret_key: str):
    url_repository = UrlRepository()

    if url := await url_repository.get_by_secret_key(secret_key):
        try:
            await url.activate()
            await url_repository.update(url)

            response = AdminUrlResponse(
                **url.dict(),
                url=url.short_url,
            )
            return response
        except UrlIsActiveException:
            raise HTTPException(
                status_code=400,
                detail=f"Requested secret key: '{secret_key}' is already active.",
            )

    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested secret key: '{secret_key}' does not exist.",
        )


@router.post(
    "/admin/deactivate/{secret_key}",
    summary="Deactivate short URL",
    response_model=AdminUrlResponse,
)
async def deactivate_url(secret_key: str) -> AdminUrlResponse:
    url_repository = UrlRepository()

    if url := await url_repository.get_by_secret_key(secret_key):
        try:
            await url.deactivate()
            await url_repository.update(url)

            response = AdminUrlResponse(
                **url.dict(),
                url=url.short_url,
            )
            return response
        except UrlIsNotActiveException:
            raise HTTPException(
                status_code=400,
                detail=f"Requested secret key: '{secret_key}' is not active.",
            )

    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested secret key: '{secret_key}' does not exist.",
        )


@router.delete(
    "/admin/{secret_key}",
    summary="Delete short URL",
    status_code=204,
)
async def delete_url(secret_key: str) -> None:
    url_repository = UrlRepository()
    if url := await url_repository.get_by_secret_key(secret_key):
        await url_repository.delete(model=url)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested secret key: '{secret_key}' does not exist.",
        )
