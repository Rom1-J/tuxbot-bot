from .buttons import DeleteButton, GIFButton, JPGButton, PNGButton, WEBPButton


class Panel:
    buttons: list


class ViewPanel(Panel):
    buttons = [
        [GIFButton, JPGButton, PNGButton, WEBPButton],
        [DeleteButton],
    ]
