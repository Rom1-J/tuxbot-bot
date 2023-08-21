from .delete_button import DeleteButton
from .threshold_button import ThresholdButton
from .toggle_button import ToggleButton


__all__ = [
    "ButtonType",
    "DeleteButton",
    "ThresholdButton",
    "ToggleButton",
]


ButtonType = type[DeleteButton] | type[ThresholdButton] | type[ToggleButton]
