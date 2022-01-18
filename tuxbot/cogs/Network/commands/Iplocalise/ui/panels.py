from .buttons import (
    GlobalButton,
    GeoButton,
    WhoisButton,
    ASNButton,
    IPInfoButton,
    BGPButton,
    DeleteButton,
)


class Panel:
    buttons: list


class ViewPanel(Panel):
    buttons = [
        [GlobalButton, GeoButton, IPInfoButton, BGPButton],
        [WhoisButton, ASNButton, DeleteButton],
    ]
