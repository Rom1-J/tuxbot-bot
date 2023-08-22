from .buttons import (
    ButtonType,
    DeleteButton,
    GIFButton,
    JPGButton,
    PNGButton,
    WEBPButton,
)


class ViewPanel:
    buttons: tuple[tuple[ButtonType, ...], ...] = (
        (GIFButton, JPGButton, PNGButton, WEBPButton),
        (DeleteButton,),
    )
