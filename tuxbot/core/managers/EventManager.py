"""
Tuxbot manager module: EventManager

Contains all events management
"""
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class EventManager:
    """Tuxbot event manager"""
    _events: List = []

    def __init__(self, tuxbot: "Tuxbot"):
        self.tuxbot = tuxbot

    @property
    def events(self) -> List:
        """Events list"""
        return self._events
