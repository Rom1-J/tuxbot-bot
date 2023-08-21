from .delete_button import DeleteButton
from .gif_button import GIFButton
from .jpg_button import JPGButton
from .png_button import PNGButton
from .webp_button import WEBPButton


__all__ = [
    "ButtonType",
    "GIFButton",
    "JPGButton",
    "PNGButton",
    "WEBPButton",
    "DeleteButton",
]

ButtonType = (
    type[GIFButton]
    | type[JPGButton]
    | type[PNGButton]
    | type[WEBPButton]
    | type[DeleteButton]
)
