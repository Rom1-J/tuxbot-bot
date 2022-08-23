"""
tuxbot.cogs.Utils.commands.UI.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives information about a user
"""

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ...converters.MemberOrUserConverter import MemberOrUserConverter
from ..exceptions import UserNotFound


class UICommand(commands.Cog):
    """Shows user information"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="ui", aliases=["user_info"])
    async def _ui(
        self,
        ctx: commands.Context[TuxbotABC],
        *,
        argument: str | None = None,
    ) -> None:
        if not argument:
            user = ctx.author
        elif not (_u := await MemberOrUserConverter().convert(ctx, argument)):
            raise UserNotFound("Unable to find this user")
        else:
            user = _u

        e = discord.Embed(color=self.bot.utils.colors.EMBED_BORDER)

        if isinstance(user, (discord.User, discord.Member)):
            e.set_author(name=user, icon_url=user.display_avatar.url)
            e.set_thumbnail(url=user.display_avatar.url)
            e.set_footer(text=f"ID: {user.id}")

            e.add_field(
                name="Created at",
                value=f"> <t:{int(user.created_at.timestamp())}:F>",
                inline=True,
            )

        if isinstance(user, discord.Member):
            if user.joined_at:
                e.add_field(
                    name="Joined at",
                    value=f"> <t:{int(user.joined_at.timestamp())}:F>",
                    inline=True,
                )

            if roles := user.roles[1:]:
                e.add_field(
                    name=f"Roles ({len(roles)})",
                    value=" ".join(role.mention for role in roles),
                    inline=False,
                )

            if premium_since := user.premium_since:
                e.add_field(
                    name="Premium since",
                    value=f"> <t:{int(premium_since.timestamp())}:F>",
                )

            if hasattr(
                self.bot.utils.colors, (status := user.status.value.upper())
            ):
                e.colour = getattr(self.bot.utils.colors, status).value

            if activity := user.activity:
                e.description = activity.name

        await ctx.send(embed=e)
