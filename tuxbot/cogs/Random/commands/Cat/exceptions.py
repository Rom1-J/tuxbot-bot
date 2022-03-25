"""
tuxbot.cogs.Random.commands.Cat.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Random module exceptions.
"""

from ...commands.exceptions import RandomException


class CATAASException(RandomException):
    """Failed to fetch from cataas.com"""
