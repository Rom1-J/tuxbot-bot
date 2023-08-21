"""Global embed page."""
import typing

import discord

from .embed import Embed


class GlobalEmbed(Embed):
    """Global embed page."""

    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
        return discord.Embed(
            description=f"Auto quote toggled to `{self.model.activated}`",
            colour=self.controller.ctx.bot.utils.colors.ONLINE
            if self.model.activated
            else self.controller.ctx.bot.utils.colors.DND,
        )
