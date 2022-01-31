"""
tuxbot.cogs.Logs.listeners.CommandCompletion.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever command is completed
"""

from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class CommandCompletion(commands.Cog):
    """Listener whenever command is completed"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.Cog.listener(name="on_command_completion")
    async def _on_command_completion(self, ctx: commands.Context):
        command = ctx.command.name

        if parent_name := ctx.command.full_parent_name:
            command = f"{parent_name} {ctx.command.name}"

        self.bot.statsd.increment(
            "command_success", value=1, tags=[f"command:{command}"]
        )
