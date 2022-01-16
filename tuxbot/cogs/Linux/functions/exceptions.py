"""
tuxbot.cogs.Linux.functions.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Linux module exceptions.
"""

from discord.ext import commands


class LinuxException(commands.BadArgument):
    """Base Linux module exceptions"""


class CNFException(LinuxException):
    """Failed to fetch from command-not-found.com"""
