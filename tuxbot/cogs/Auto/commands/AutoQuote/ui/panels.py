from .buttons import ButtonType, DeleteButton, ToggleButton


class ViewPanel:
    buttons: list[list[ButtonType]] = [
        [ToggleButton, DeleteButton],
    ]
