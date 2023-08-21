"""
tuxbot.cogs.Dev.commands.HTTP.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Throwable Dev module exceptions.
"""

from tuxbot.cogs.Dev.commands.exceptions import DevException


class UnknownHttpCode(DevException):
    """Unknown HTTP code exception."""
