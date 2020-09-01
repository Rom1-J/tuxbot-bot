from discord.ext import commands


class DisabledCommandByServerOwner(commands.CheckFailure):
    pass


class DisabledCommandByBotOwner(commands.CheckFailure):
    pass
