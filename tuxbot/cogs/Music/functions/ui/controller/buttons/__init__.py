from typing import TypeVar

from .backward import BackwardButton
from .blank import BlankButton
from .end import EndButton
from .forward import ForwardButton
from .next import NextButton
from .previous import PreviousButton
from .queue import QueueButton
from .remove import RemoveButton
from .shuffle import ShuffleButton
from .toggle import ToggleButton
from .volume import VolumeUpButton, VolumeDownButton

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
)
