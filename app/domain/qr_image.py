from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    CircleModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
)

if TYPE_CHECKING:
    from typing import Optional, Union

    from qrcode.image.pil import PilImage
    from qrcode.image.styles.moduledrawers.pil import StyledPilQRModuleDrawer

QR_CODE_RENDER_STYLES = Literal[
    "circle",
    "horizontal",
    "round",
    "vertical",
]


class QrImage(BaseModel):
    content: str
    style: Optional[QR_CODE_RENDER_STYLES] = None

    def _qr(self) -> QRCode:
        return QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            box_size=15,
        )

    def _get_drawer(self, style_name: str) -> StyledPilQRModuleDrawer:
        STYLE_MAP = {
            "round": RoundedModuleDrawer,
            "vertical": VerticalBarsDrawer,
            "horizontal": HorizontalBarsDrawer,
            "circle": CircleModuleDrawer,
        }

        return STYLE_MAP[style_name]()

    def generate(self) -> Union[PilImage, StyledPilImage]:
        qr = self._qr()
        qr.add_data(self.content)
        if self.style:
            return qr.make_image(
                image_factory=StyledPilImage, module_drawer=self._get_drawer(self.style)
            )
        else:
            return qr.make_image()

    def to_bytes(self, image: Union[PilImage, StyledPilImage]) -> BytesIO:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer
