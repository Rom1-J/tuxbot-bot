from .buttons import ButtonType, DeleteButton, ThresholdButton, ToggleButton


class ViewPanel:
    buttons: list[list[ButtonType]] = [
        [ToggleButton, ThresholdButton, DeleteButton],
    ]
