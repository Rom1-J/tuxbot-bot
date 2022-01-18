"""
tuxbot.cogs.Network.commands.Peeringdb.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Network module exceptions.
"""

from ..exceptions import NetworkException


class InvalidAsn(NetworkException):
    """Given ASN doesn't respect any format"""
