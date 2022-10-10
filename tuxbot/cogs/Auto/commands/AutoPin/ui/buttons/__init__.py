import typing

from .DeleteButton import DeleteButton
from .ThresholdButton import ThresholdButton
from .ToggleButton import ToggleButton


__all__ = [
    "ButtonType",
    "DeleteButton",
    "ThresholdButton",
    "ToggleButton",
]


ButtonType = typing.Union[
    type[DeleteButton], type[ThresholdButton], type[ToggleButton]
]
