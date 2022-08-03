"""
tuxbot.cogs.Polls.commands.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Throwable Polls module exceptions.
"""

from discord.ext import commands


class PollsException(commands.BadArgument):
    """Base Polls module exceptions"""
