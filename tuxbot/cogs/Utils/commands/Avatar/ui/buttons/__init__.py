import typing

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

ButtonType = typing.Union[
    type[GIFButton],
    type[JPGButton],
    type[PNGButton],
    type[WEBPButton],
    type[DeleteButton],
]
