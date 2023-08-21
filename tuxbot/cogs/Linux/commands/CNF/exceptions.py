"""
tuxbot.cogs.Linux.commands.CNF.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Throwable Linux module exceptions.
"""

from tuxbot.cogs.Linux.commands.exceptions import LinuxException


class CNFException(LinuxException):
    """Failed to fetch from command-not-found.com."""
