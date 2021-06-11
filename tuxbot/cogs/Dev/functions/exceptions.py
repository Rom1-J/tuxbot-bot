from discord.ext import commands


class DevException(commands.BadArgument):
    pass


class UnknownHttpCode(DevException):
    pass
