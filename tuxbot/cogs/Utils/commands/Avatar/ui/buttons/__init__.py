from typing import TypeVar

from .DeleteButton import DeleteButton
from .GIFButton import GIFButton
from .JPGButton import JPGButton
from .PNGButton import PNGButton
from .WEBPButton import WEBPButton

__all__ = [
    "ButtonType",
    "GIFButton",
    "JPGButton",
    "PNGButton",
    "WEBPButton",
    "DeleteButton",
]


ButtonType = TypeVar(
    "ButtonType",
    GIFButton,
    JPGButton,
    PNGButton,
    WEBPButton,
    DeleteButton,
)
