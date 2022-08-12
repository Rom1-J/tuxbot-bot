from .buttons import (
    ButtonType,
    DeleteButton,
    GIFButton,
    JPGButton,
    PNGButton,
    WEBPButton,
)


class ViewPanel:
    buttons: list[list[ButtonType]] = [
        [GIFButton, JPGButton, PNGButton, WEBPButton],
        [DeleteButton],
    ]
