"""
tuxbot.cogs.Linux.commands.CNF.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Linux module exceptions.
"""

from discord.ext import commands


class LinuxException(commands.BadArgument):
    """Base Linux module exceptions"""


class CNFException(LinuxException):
    """Failed to fetch from command-not-found.com"""
