from .buttons import ButtonType, DeleteButton, ToggleButton


class ViewPanel:
    buttons: tuple[tuple[ButtonType, ...], ...] = (
        (ToggleButton, DeleteButton),
    )
