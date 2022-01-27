from .buttons import (
    GlobalButton,
    GeoButton,
    RawButton,
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
        [GlobalButton, GeoButton, RawButton, IPInfoButton, BGPButton],
        [WhoisButton, ASNButton, DeleteButton],
    ]
