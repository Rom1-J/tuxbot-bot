import typing

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


ButtonType = typing.Union[
    type[GlobalButton],
    type[GeoButton],
    type[RawButton],
    type[WhoisButton],
    type[ASNButton],
    type[IPInfoButton],
    type[BGPButton],
    type[DeleteButton],
]
