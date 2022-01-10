"""
Tuxbot collections module: CommandCollection

Contains all command collections
"""
from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Iterator, Dict, Type

from tuxbot.abc.CommandABC import CommandABC
from tuxbot.core.logger import logger

if TYPE_CHECKING:
    from tuxbot.core.Tuxbot import Tuxbot


class CommandCollection(MutableMapping):
    """Tuxbot commands collection"""

    _commands: Dict[str, CommandABC] = {}

    def __setitem__(self, key: str, value: CommandABC) -> None:
        self._commands[key] = value

    def __delitem__(self, key: str) -> None:
        del self._commands[key]

    def __getitem__(self, key: str) -> CommandABC:
        return self._commands[key]

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self) -> Iterator[str]:
        return self._commands.__iter__()

    def __init__(self, config, tuxbot: "Tuxbot"):
        self.config = config
        self.tuxbot = tuxbot

    # =========================================================================

    def register(self, _command: Type[CommandABC]):
        """Register command

        Parameters
        ----------
        _command:ModuleABC
            Command class to register
        """
        if not isinstance(_command, CommandABC):
            return logger.debug("[CommandCollection Skipping unknown command]")
