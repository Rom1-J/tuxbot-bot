"""
tuxbot.cogs.Auto.commands.AutoPin.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toggle auto pins
"""

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from .models.AutoPin import AutoPinModel
from .ui.ViewController import ViewController


class AutoPinCommand(commands.Cog):
    """Toggle auto pins"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    @staticmethod
    async def __get_model(guild_id: int) -> AutoPinModel:
        model: AutoPinModel | None = await AutoPinModel.get_or_none(
            guild_id=guild_id
        )

        if not isinstance(model, AutoPinModel):
            _m: AutoPinModel = await AutoPinModel.create(guild_id=guild_id)
            return _m

        return model

    # =========================================================================
    # =========================================================================

    @commands.group(name="auto_pin")
    @commands.guild_only()
    async def _auto_pin(self, ctx: commands.Context[TuxbotABC]) -> None:
        if not ctx.guild:
            return

        controller = ViewController(
            ctx=ctx,
            model=await self.__get_model(guild_id=ctx.guild.id),
        )

        await controller.send()
