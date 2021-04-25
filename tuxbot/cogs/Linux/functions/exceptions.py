from discord.ext import commands


class LinuxException(commands.BadArgument):
    pass


class CNFException(LinuxException):
    pass
