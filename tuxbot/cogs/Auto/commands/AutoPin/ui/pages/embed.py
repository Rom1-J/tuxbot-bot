"""Base embed page."""
import abc
import typing

import discord


if typing.TYPE_CHECKING:
    from tuxbot.cogs.Auto.commands.AutoPin.ui.view_controller import (
        ViewController,
    )


class Embed(abc.ABC):
    """Base embed page."""

    def __init__(self: typing.Self, controller: "ViewController") -> None:
        self.controller = controller
        self.model = self.controller.model

        self.ctx = self.controller.ctx

    # =========================================================================
    # =========================================================================

    @abc.abstractmethod
    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
