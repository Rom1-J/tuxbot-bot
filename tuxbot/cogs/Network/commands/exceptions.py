"""
tuxbot.cogs.Network.commands.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from discord.ext import commands


class NetworkException(commands.BadArgument):
    """Base Network module exceptions"""


class RFC1918(NetworkException):
    """Ip reserved as local use"""
