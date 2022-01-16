"""
tuxbot.cogs.Dev.functions.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Dev module exceptions.
"""

from discord.ext import commands


class DevException(commands.BadArgument):
    """Base Dev module exceptions"""
    pass


class UnknownHttpCode(DevException):
    """Unknown HTTP code exception"""
    pass
