from pydantic import BaseModel

from app.domain import QR_CODE_RENDER_STYLES


class QrStyle(BaseModel):
    style: QR_CODE_RENDER_STYLES
