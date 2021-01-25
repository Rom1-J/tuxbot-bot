from discord.ext import commands


class RFC18(commands.UserNotFound):
    pass


class InvalidIp(commands.BadArgument):
    pass
