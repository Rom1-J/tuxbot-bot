"""
tuxbot.cogs.Random.commands.Duck.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Random module exceptions.
"""

from ...commands.exceptions import RandomException


class RDUCKException(RandomException):
    """Failed to fetch from random-d.uk"""
