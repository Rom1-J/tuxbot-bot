"""
tuxbot.cogs.Utils.commands.UI.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Utils module exceptions.
"""

from ...commands.exceptions import UtilsException


class UserNotFound(UtilsException):
    """Failed find user"""
