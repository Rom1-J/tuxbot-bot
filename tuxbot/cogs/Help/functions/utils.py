import discord
from discord.ext import commands

from tuxbot.core.utils.functions.extra import CommandPLus, GroupPlus
from ..config import HelpConfig


class HelpCommand(commands.HelpCommand):
    def __init__(self, config: HelpConfig):
        super().__init__()

        self.__config = config

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    # =========================================================================
    # =========================================================================

    async def send_bot_help(self, mapping: dict):  # skipcq: PYL-W0613
        e = discord.Embed(title="Tuxbot Wiki!", color=0x2F3136)
        e.add_field(
            name="Site",
            value=f"> • [wiki]({self.__config.wikiUrl})\n"
            f"> • [site]({self.__config.siteUrl})",
            inline=True,
        )
        e.add_field(
            name="Discord",
            value=f"> [support]({self.__config.discordUrl})",
            inline=True,
        )

        await self.context.send(embed=e)

    async def send_cog_help(self, cog: commands.Cog):
        url = self.__config.wikiUrl + f"/{cog.qualified_name}"

        e = discord.Embed(title=f"{cog.qualified_name} Wiki: ", color=0x2F3136)
        e.description = f"[{url}]({url})"

        await self.context.send(embed=e)

    async def send_command_help(self, command: CommandPLus):
        url = self.__config.wikiUrl + f"/{command.cog_name}#{command.name}"

        e = discord.Embed(title=f"{command.name} Wiki: ", color=0x2F3136)
        e.description = f"[{url}]({url})"

        await self.context.send(embed=e)

    async def send_group_help(self, group: GroupPlus):
        url = self.__config.wikiUrl + f"/{group.cog_name}#{group.name}"

        e = discord.Embed(title=f"{group.name} Wiki: ", color=0x2F3136)
        e.description = f"[{url}]({url})"

        await self.context.send(embed=e)
