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
            description=(
                f"Auto pin toggled to `{self.model.activated}` "
                f"and threshold `{self.model.threshold}`"
            ),
            colour=self.controller.ctx.bot.utils.colors.ONLINE
            if self.model.activated
            else self.controller.ctx.bot.utils.colors.DND,
        )

        return e
