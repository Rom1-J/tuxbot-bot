from .buttons import (
    ASNButton,
    BGPButton,
    DeleteButton,
    GeoButton,
    GlobalButton,
    IPInfoButton,
    RawButton,
    WhoisButton,
)


class Panel:
    buttons: list


class ViewPanel(Panel):
    buttons = [
        [GlobalButton, GeoButton, RawButton, IPInfoButton, BGPButton],
        [WhoisButton, ASNButton, DeleteButton],
    ]
