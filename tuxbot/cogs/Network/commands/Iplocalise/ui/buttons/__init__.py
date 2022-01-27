from typing import TypeVar

from .GlobalButton import GlobalButton
from .GeoButton import GeoButton
from .RawButton import RawButton

from .WhoisButton import WhoisButton
from .ASNButton import ASNButton

from .IPInfoButton import IPInfoButton
from .BGPButton import BGPButton

from .DeleteButton import DeleteButton


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
