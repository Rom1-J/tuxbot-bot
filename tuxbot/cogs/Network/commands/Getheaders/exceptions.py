"""
tuxbot.cogs.Network.commands.Getheaders.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from ..exceptions import NetworkException


class UnreachableAddress(NetworkException):
    """Given address is unreachable"""
