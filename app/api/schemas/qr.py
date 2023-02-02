from pydantic import BaseModel
from typing import Literal
from app.domain import QR_CODE_RENDER_STYLES


class QrStyle(BaseModel):
    style: QR_CODE_RENDER_STYLES
