import logging

import discord
from discord.ext import commands

from tuxbot.cogs.Linux.functions.utils import get_from_cnf
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)

log = logging.getLogger("tuxbot.cogs.Linux")
_ = Translator("Linux", __file__)


class Linux(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def cog_before_invoke(self, ctx: ContextPlus):
        await ctx.trigger_typing()

    # =========================================================================
    # =========================================================================

    @command_extra(name="cnf")
    async def _cnf(self, ctx: ContextPlus, command: str):
        cnf = await get_from_cnf(command)

        if cnf["distro"]:
            e = discord.Embed(title=f"{cnf['description']} ({cnf['command']})")

            description = (
                "__Maintainer:__ {maintainer}\n"
                "__Homepage:__ [{homepage}]({homepage})\n"
                "__Section:__ {section}".format(
                    maintainer=cnf["meta"].get("maintainer", "N/A"),
                    homepage=cnf["meta"].get("homepage", "N/A"),
                    section=cnf["meta"].get("section", "N/A"),
                )
            )

            e.description = description

            e.set_footer(
                text="Powered by https://command-not-found.com/ "
                "and with his authorization"
            )

            for k, v in cnf["distro"].items():
                e.add_field(name=f"**__{k}__**", value=f"```{v}```")

            return await ctx.send(embed=e)

        await ctx.send(_("No result found", ctx, self.bot.config))
