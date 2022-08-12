"""
tuxbot.cogs.Utils.commands.Avatar.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows avatar of user
"""

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ...converters.MemberOrUserConverter import MemberOrUserConverter
from ..exceptions import UserNotFound
from .ui.ViewController import ViewController


class AvatarCommand(commands.Cog):
    """Shows user's avatar"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="avatar")
    async def _avatar(
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

        e = discord.Embed(
            title=f"Avatar of {user}",
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )
        e.set_image(url=user.display_avatar.url)

        controller = ViewController(ctx=ctx, data=user)

        await controller.send()
