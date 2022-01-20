"""
tuxbot.cogs.Dev.commands.HTTP.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Dev module exceptions.
"""

from ...commands.exceptions import DevException


class UnknownHttpCode(DevException):
    """Unknown HTTP code exception"""
