"""
tuxbot.cogs.Dev.commands.HTTP.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Dev module exceptions.
"""

from discord.ext import commands


class DevException(commands.BadArgument):
    """Base Dev module exceptions"""


class UnknownHttpCode(DevException):
    """Unknown HTTP code exception"""
