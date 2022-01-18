"""
tuxbot.cogs.Network.commands.Iplocalise.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from ..exceptions import NetworkException


class RFC1819(NetworkException):
    """Ip reserved as local use"""


class VersionNotFound(NetworkException):
    """Domain not reachable with given inet"""
