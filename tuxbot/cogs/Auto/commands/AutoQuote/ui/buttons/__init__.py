from .delete_button import DeleteButton
from .toggle_button import ToggleButton


__all__ = (
    "ButtonType",
    "DeleteButton",
    "ToggleButton",
)


ButtonType = type[DeleteButton] | type[ToggleButton]
