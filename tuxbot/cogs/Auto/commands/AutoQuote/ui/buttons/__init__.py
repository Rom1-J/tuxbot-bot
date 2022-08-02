from typing import TypeVar

from .DeleteButton import DeleteButton
from .ToggleButton import ToggleButton


__all__ = [
    "ButtonType",
    "DeleteButton",
    "ToggleButton",
]


ButtonType = TypeVar(
    "ButtonType",
    DeleteButton,
    ToggleButton,
)
