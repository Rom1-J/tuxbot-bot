"""
tuxbot.cogs.Network.commands.Iplocalise.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from ..exceptions import NetworkException


class VersionNotFound(NetworkException):
    """Domain not reachable with given inet"""
