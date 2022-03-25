"""
tuxbot.cogs.Random.commands.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Random module exceptions.
"""

from discord.ext import commands


class RandomException(commands.BadArgument):
    """Base Random module exceptions"""


class APIException(RandomException):
    """Failed to fetch from API"""
