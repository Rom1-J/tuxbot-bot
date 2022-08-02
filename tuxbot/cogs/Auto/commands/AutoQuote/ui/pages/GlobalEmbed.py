"""
Global embed page
"""

import discord

from .Embed import Embed


class GlobalEmbed(Embed):
    """Global embed page"""

    def rebuild(self) -> discord.Embed:
        """(Re)build embed"""

        e = discord.Embed(
            description=f"Auto quote toggled to `{self.model.activated}`",
            colour=self.controller.ctx.bot.utils.colors.ONLINE.value
            if self.model.activated
            else self.controller.ctx.bot.utils.colors.DND.value,
        )

        return e
