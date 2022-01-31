from typing import TypeVar

from .ASNButton import ASNButton
from .BGPButton import BGPButton
from .DeleteButton import DeleteButton
from .GeoButton import GeoButton
from .GlobalButton import GlobalButton
from .IPInfoButton import IPInfoButton
from .RawButton import RawButton
from .WhoisButton import WhoisButton

__all__ = [
    "ButtonType",
    "GlobalButton",
    "GeoButton",
    "RawButton",
    "WhoisButton",
    "ASNButton",
    "IPInfoButton",
    "BGPButton",
    "DeleteButton",
]


ButtonType = TypeVar(
    "ButtonType",
    GlobalButton,
    GeoButton,
    RawButton,
    WhoisButton,
    ASNButton,
    IPInfoButton,
    BGPButton,
    DeleteButton,
)
