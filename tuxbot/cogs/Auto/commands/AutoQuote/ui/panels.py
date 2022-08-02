from .buttons import DeleteButton, ToggleButton


class Panel:
    buttons: list


class ViewPanel(Panel):
    buttons = [
        [ToggleButton, DeleteButton],
    ]
