"""
tuxbot.cogs.Utils.commands.Avatar.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Shows avatar of user
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.cogs.Utils.commands.exceptions import UserNotFound
from tuxbot.cogs.Utils.converters.member_or_user_converter import (
    MemberOrUserConverter,
)
from tuxbot.core.tuxbot import Tuxbot

from .ui.view_controller import ViewController


class AvatarCommand(commands.Cog):
    """Shows user's avatar."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="avatar")
    async def _avatar(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],
        *,
        argument: str | None = None,
    ) -> None:
        if not argument:
            user = ctx.author
        elif not (_u := await MemberOrUserConverter().convert(ctx, argument)):
            msg = "Unable to find this user"
            raise UserNotFound(msg)
        else:
            user = _u

        e = discord.Embed(
            title=f"Avatar of {user}",
            color=self.bot.utils.colors.EMBED_BORDER,
        )
        e.set_image(url=user.display_avatar.url)

        controller = ViewController(ctx=ctx, data=user)

        await controller.send()
