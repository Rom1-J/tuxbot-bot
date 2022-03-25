"""
tuxbot.cogs.Random.commands.Dog.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Random module exceptions.
"""

from ...commands.exceptions import RandomException


class DOGCEOException(RandomException):
    """Failed to fetch from dog.ceo"""
