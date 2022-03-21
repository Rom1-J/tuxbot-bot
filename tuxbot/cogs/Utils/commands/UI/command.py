"""
tuxbot.cogs.Utils.commands.UI.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives information about a user
"""

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from ...converters.MemberOrUserConverter import MemberOrUserConverter
from ..exceptions import UserNotFound


class UICommand(commands.Cog):
    """Shows user information"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="ui", aliases=["user_info"])
    async def _ui(
        self,
        ctx: commands.Context,
        *,
        user_id: MemberOrUserConverter = "me",  # type: ignore
    ):
        if user_id is None:
            raise UserNotFound("Unable to find this user")

        if user_id == "me":
            user_id = ctx.author

        e = discord.Embed(color=self.bot.utils.colors.EMBED_BORDER.value)

        if isinstance(user_id, (discord.User, discord.Member)):
            e.set_author(name=user_id, icon_url=user_id.display_avatar.url)
            e.set_thumbnail(url=user_id.display_avatar.url)
            e.set_footer(text=f"ID: {user_id.id}")

            e.add_field(
                name="Created at",
                value=f"> <t:{int(user_id.created_at.timestamp())}:F>",
                inline=True,
            )

        if isinstance(user_id, discord.Member):
            e.add_field(
                name="Joined at",
                value=f"> <t:{int(user_id.joined_at.timestamp())}:F>",
                inline=True,
            )

            if roles := user_id.roles[1:]:
                e.add_field(
                    name=f"Roles ({len(roles)})",
                    value=" ".join(role.mention for role in roles),
                    inline=False,
                )

            if premium_since := user_id.premium_since:
                e.add_field(
                    name="Premium since",
                    value=f"> <t:{int(premium_since.timestamp())}:F>",
                )

            # noinspection PyUnresolvedReferences
            if (
                status := user_id.status.value.upper()
            ) in self.bot.utils.colors.__members__:
                e.colour = getattr(self.bot.utils.colors, status).value

            if activity := user_id.activity:
                e.description = activity.name

        await ctx.send(embed=e)
