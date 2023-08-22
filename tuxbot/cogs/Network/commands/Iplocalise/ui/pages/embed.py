"""Base embed page."""
import abc
import typing

import discord


if typing.TYPE_CHECKING:
    from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
        ViewController,
    )


class Embed(abc.ABC):
    """Base embed page."""

    def __init__(self: typing.Self, controller: "ViewController") -> None:
        self.controller = controller
        self.data = self.controller.data

        self.ctx = self.controller.ctx

    # =========================================================================
    # =========================================================================

    def update(self: typing.Self, controller: "ViewController") -> None:
        """Update loaded data."""
        self.controller = controller
        self.data = self.controller.data

    # =========================================================================

    @abc.abstractmethod
    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
