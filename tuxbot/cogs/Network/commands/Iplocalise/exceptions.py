"""
tuxbot.cogs.Network.commands.Iplocalise.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Throwable Network module exceptions.
"""

from tuxbot.cogs.Network.commands.exceptions import NetworkException


class VersionNotFound(NetworkException):
    """Domain not reachable with given inet."""
