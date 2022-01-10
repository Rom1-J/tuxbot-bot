"""
Tuxbot abstract class module: CommandABC

Contains all Command properties
"""
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class CommandABC(ABC):
    """Command Abstract Class"""

    _name: str = super.__class__.__name__
    _description: str = ""

    _enabled: bool = False

    # =========================================================================
    # =========================================================================

    @property
    def name(self) -> str:
        """Module name"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    # =========================================================================

    @property
    def description(self) -> str:
        """Module description"""
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    # =========================================================================

    @property
    def enabled(self) -> bool:
        """Module state"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    # =========================================================================
    # =========================================================================

    def __init__(self, tuxbot: "Tuxbot"): ...

    # =========================================================================
    # =========================================================================
