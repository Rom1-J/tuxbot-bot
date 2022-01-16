"""
tuxbot.cogs.Network.functions.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from discord.ext import commands


class NetworkException(commands.BadArgument):
    """Base Network module exceptions"""


class RFC1819(NetworkException):
    """Ip reserved as local use"""


class VersionNotFound(NetworkException):
    """Domain not reachable with given inet"""
