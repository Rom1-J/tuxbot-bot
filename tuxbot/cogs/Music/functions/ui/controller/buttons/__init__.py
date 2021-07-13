from typing import TypeVar

from .view import *
from .jump import *

ButtonType = TypeVar(
    "ButtonType",
    BackwardButton,
    BlankButton,
    EndButton,
    ForwardButton,
    NextButton,
    PreviousButton,
    QueueButton,
    RemoveButton,
    ShuffleButton,
    ToggleButton,
    VolumeUpButton,
    VolumeDownButton,
    JumpButton,
)
