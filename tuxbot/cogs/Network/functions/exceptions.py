"""
tuxbot.cogs.Network.functions.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from discord.ext import commands


class NetworkException(commands.BadArgument):
    """Base Network module exceptions"""
    pass


class RFC1819(NetworkException):
    pass


class InvalidIp(NetworkException):
    pass


class InvalidDomain(NetworkException):
    pass


class InvalidQueryType(NetworkException):
    pass


class VersionNotFound(NetworkException):
    """Domain not reachable with given inet"""
    pass
