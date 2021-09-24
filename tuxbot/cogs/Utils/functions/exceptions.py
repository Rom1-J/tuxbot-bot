from discord.ext import commands


class UtilsException(commands.BadArgument):
    pass


class UserNotFound(UtilsException):
    pass
