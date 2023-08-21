"""
tuxbot.cogs.Utils.commands.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Throwable Utils module exceptions.
"""

from discord.ext import commands


class UtilsException(commands.BadArgument):
    """Base Utils module exceptions."""


class UserNotFound(UtilsException):
    """Failed find user."""
