"""
tuxbot.cogs.Help.commands.Help.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to restart Tuxbot
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC


class HelpCommand(commands.HelpCommand):
    """Tuxbot help command"""

    def __init__(self) -> None:
        super().__init__()

        self.site_url = "https://tuxbot.gnous.eu"
        self.wiki_url = self.site_url + "/wiki"
        self.discord_url = "https://discord.gg/QXmESeghBP"

    # =========================================================================

    async def on_help_command_error(  # type: ignore
        self, ctx: commands.Context[TuxbotABC], error: commands.CommandError
    ) -> None:
        """Shows error if happens"""

        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    # =========================================================================
    # =========================================================================

    async def send_bot_help(
        self, mapping: typing.Any
    ) -> None:  # skipcq: PYL-W0613
        """Send global bot help"""

        e = discord.Embed(title="Tuxbot Wiki!", color=0x2F3136)
        e.add_field(
            name="Site",
            value=f"> • [wiki]({self.wiki_url})\n"
            f"> • [site]({self.site_url})",
            inline=True,
        )
        e.add_field(
            name="Discord",
            value=f"> [support]({self.discord_url})",
            inline=True,
        )

        await self.context.send(embed=e)

    # =========================================================================

    # pylint: disable=arguments-differ
    async def send_cog_help(self, cog: commands.Cog) -> None:
        """Send specific cog help"""

        url = self.wiki_url + f"/{cog.qualified_name}"

        e = discord.Embed(title=f"{cog.qualified_name} Wiki: ", color=0x2F3136)
        e.description = f"[{url}]({url})"

        await self.context.send(embed=e)

    # =========================================================================

    # pylint: disable=arguments-differ
    async def send_command_help(
        self, command: commands.Command  # type: ignore
    ) -> None:
        """Send specific command help"""

        url = self.wiki_url + f"/{command.cog_name}#{command.name}"

        e = discord.Embed(title=f"{command.name} Wiki: ", color=0x2F3136)
        e.description = f"[{url}]({url})"

        await self.context.send(embed=e)

    # =========================================================================

    # pylint: disable=arguments-differ
    async def send_group_help(
        self, group: commands.Group  # type: ignore
    ) -> None:
        """Send specific command group help"""

        url = self.wiki_url + f"/{group.cog_name}#{group.name}"

        e = discord.Embed(title=f"{group.name} Wiki: ", color=0x2F3136)
        e.description = f"[{url}]({url})"

        await self.context.send(embed=e)
