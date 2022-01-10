"""
Tuxbot abstract class module: ModuleABC

Contains all Module properties
"""
from abc import abstractmethod
from typing import Optional, Any, TYPE_CHECKING

from discord.ext import commands

from tuxbot.core.collections.CommandCollection import CommandCollection

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class ModuleABC(commands.Cog):
    """Module Abstract Class"""

    _name: str = ""
    _description: str = ""

    _enabled: bool = False

    _commands: Optional[CommandCollection] = None
    _models: Optional[CommandCollection] = None

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

    @property
    def commands(self) -> CommandCollection:
        """Module commands"""
        return self._commands

    @commands.setter
    def commands(self, value: CommandCollection):
        self._commands = value

    # =========================================================================

    @property
    def models(self):
        """Module models"""
        return self._models

    @models.setter
    def models(self, value):
        self._models = value

    # =========================================================================
    # =========================================================================

    def __init__(self, tuxbot: "Tuxbot"): ...

    # =========================================================================
    # =========================================================================

    @abstractmethod
    def register_listener(self, event: str, *args: Any, **kwargs: Any):
        """Register listener"""

    # =========================================================================

    @abstractmethod
    def crash_report(self):
        """Crash report handler"""
