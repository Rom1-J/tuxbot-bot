"""
tuxbot.cogs.Auto.commands.AutoQuote.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Toggle auto quotes
"""
import typing

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot

from .models.auto_quote import AutoQuoteModel
from .ui.view_controller import ViewController


class AutoQuoteCommand(commands.Cog):
    """Toggle auto quotes."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    @staticmethod
    async def __get_model(guild_id: int) -> AutoQuoteModel:
        model: AutoQuoteModel | None = await AutoQuoteModel.get_or_none(
            guild_id=guild_id
        )

        if not isinstance(model, AutoQuoteModel):
            _m: AutoQuoteModel = await AutoQuoteModel.create(guild_id=guild_id)
            return _m

        return model

    # =========================================================================
    # =========================================================================

    @commands.group(name="auto_quote")
    @commands.guild_only()
    async def _auto_quote(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        if not ctx.guild:
            return

        controller = ViewController(
            ctx=ctx,
            model=await self.__get_model(guild_id=ctx.guild.id),
        )

        await controller.send()
