from .buttons import (
    BlankButton,
    RemoveButton,
    VolumeUpButton,
    EndButton,
    BackwardButton,
    PreviousButton,
    ToggleButton,
    NextButton,
    ForwardButton,
    ShuffleButton,
    VolumeDownButton,
    QueueButton,
    JumpButton,
)


class Panel:
    buttons: list


class ViewPanel(Panel):
    buttons = [
        [
            BlankButton,
            RemoveButton,
            VolumeUpButton,
            EndButton,
            BlankButton,
        ],
        [
            BackwardButton,
            PreviousButton,
            ToggleButton,
            NextButton,
            ForwardButton,
        ],
        [
            BlankButton,
            ShuffleButton,
            VolumeDownButton,
            QueueButton,
            BlankButton,
        ],
    ]


class JumpPanel(Panel):
    buttons = [[RemoveButton, JumpButton]]
