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
    buttons: tuple[tuple[ButtonType, ...], ...] = (
        (GlobalButton, GeoButton, RawButton, IPInfoButton, BGPButton),
        (WhoisButton, ASNButton, DeleteButton),
    )
