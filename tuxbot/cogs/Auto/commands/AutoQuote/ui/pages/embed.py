"""Base embed page."""
import typing

import discord


if typing.TYPE_CHECKING:
    from tuxbot.cogs.Auto.commands.AutoQuote.ui.view_controller import (
        ViewController,
    )


class Embed:
    """Base embed page."""

    def __init__(self: typing.Self, controller: "ViewController") -> None:
        self.controller = controller
        self.model = self.controller.model

        self.ctx = self.controller.ctx

    # =========================================================================
    # =========================================================================

    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
