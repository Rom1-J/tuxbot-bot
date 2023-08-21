"""
tuxbot.cogs.Network.commands.Getheaders.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Throwable Network module exceptions.
"""

from tuxbot.cogs.Network.commands.exceptions import NetworkException


class UnreachableAddress(NetworkException):
    """Given address is unreachable."""
