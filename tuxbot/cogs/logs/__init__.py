import logging

from discord.ext import commands

from .logs import Logs, GatewayHandler, on_error
from ...core.bot import Tux


def setup(bot: Tux):
    cog = Logs(bot)
    bot.add_cog(cog)

    handler = GatewayHandler(cog)
    logging.getLogger().addHandler(handler)
    commands.AutoShardedBot.on_error = on_error
