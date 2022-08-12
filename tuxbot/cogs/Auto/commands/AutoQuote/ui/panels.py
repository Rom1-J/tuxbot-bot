from .buttons import ButtonType, DeleteButton, ToggleButton


class Panel:
    buttons: list[list[ButtonType]]


class ViewPanel(Panel):
    buttons = [
        [ToggleButton, DeleteButton],
    ]
