import logging

from discord.ext import commands

from .logs import Logs, GatewayHandler, on_error


def setup(bot):
    cog = Logs(bot)
    bot.add_cog(cog)

    handler = GatewayHandler(cog)
    logging.getLogger().addHandler(handler)
    commands.AutoShardedBot.on_error = on_error
