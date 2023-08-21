"""Global embed page."""
import typing

import discord

from .embed import Embed


class GlobalEmbed(Embed):
    """Global embed page."""

    def rebuild(self: typing.Self) -> discord.Embed:
        """(Re)build embed."""
        return discord.Embed(
            description=(
                f"Auto pin toggled to `{self.model.activated}` "
                f"and threshold `{self.model.threshold}`"
            ),
            colour=self.controller.ctx.bot.utils.colors.ONLINE
            if self.model.activated
            else self.controller.ctx.bot.utils.colors.DND,
        )
