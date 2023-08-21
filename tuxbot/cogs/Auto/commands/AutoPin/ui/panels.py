from .buttons import ButtonType, DeleteButton, ThresholdButton, ToggleButton


class ViewPanel:
    buttons: tuple[tuple[ButtonType]] = (
        (ToggleButton, ThresholdButton, DeleteButton),
    )
