from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse

from app.api.schemas.qr import QrStyle
from app.domain.qr_image import QrImage
from app.repositories import UrlRepository

router = APIRouter(
    prefix="/qr",
    tags=["qr"],
)


@router.get(
    "/{secret_key}",
    summary="Create a QR code for target URL",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def generate_qr(
    secret_key: str,
    url_repository: UrlRepository = Depends(UrlRepository.get_repository),
):
    if url := await url_repository.get_by_secret_key(secret_key):
        qr = QrImage(content=url.short_url)
        image = qr.generate()
        _bytes = qr.to_bytes(image)
        return StreamingResponse(content=_bytes, media_type="image/png")
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested secret key: '{secret_key}' does not exist.",
        )


@router.get(
    "/{secret_key}/{style}",
    summary="Create a styled QR code for target URL",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def generate_styled_qr(
    secret_key: str,
    style: QrStyle = Depends(),
    url_repository: UrlRepository = Depends(UrlRepository.get_repository),
):
    if url := await url_repository.get_by_secret_key(secret_key):
        qr = QrImage(content=url.short_url, style=style.style)
        image = qr.generate()
        _bytes = qr.to_bytes(image)
        return StreamingResponse(content=_bytes, media_type="image/png")
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Requested secret key: '{secret_key}' does not exist.",
        )
