import typing

from .DeleteButton import DeleteButton
from .ToggleButton import ToggleButton


__all__ = [
    "ButtonType",
    "DeleteButton",
    "ToggleButton",
]


ButtonType = typing.Union[type[DeleteButton], type[ToggleButton]]
