from .buttons import (
    ASNButton,
    BGPButton,
    ButtonType,
    DeleteButton,
    GeoButton,
    GlobalButton,
    IPInfoButton,
    RawButton,
    WhoisButton,
)


class ViewPanel:
    buttons: list[list[ButtonType]] = [
        [GlobalButton, GeoButton, RawButton, IPInfoButton, BGPButton],
        [WhoisButton, ASNButton, DeleteButton],
    ]
