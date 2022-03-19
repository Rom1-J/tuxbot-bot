"""
tuxbot.cogs.Utils.commands.Avatar.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows avatar of user
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from ...converters.MemberOrUserConverter import MemberOrUserConverter
from ..exceptions import UserNotFound
from .ui.view import ViewController


class AvatarCommand(commands.Cog):
    """Shows user's avatar"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="avatar")
    async def _avatar(
        self,
        ctx: commands.Context,
        *,
        user_id: MemberOrUserConverter = "me",  # type: ignore
    ):
        if user_id is None:
            raise UserNotFound("Unable to find this user")

        if user_id == "me":
            user_id = ctx.author

        e = discord.Embed(
            title=f"Avatar of {user_id}",
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )
        e.set_image(url=user_id.display_avatar.url)

        controller = ViewController(ctx=ctx, data=user_id)

        await controller.send()
