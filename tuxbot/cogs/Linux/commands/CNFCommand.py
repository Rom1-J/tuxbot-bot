"""
tuxbot.cogs.Linux.commands.CNFCommand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows which package to install when `command not found`
"""

import discord
import yaml
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from ..functions.CNF import get_from_cnf


class CNFCommand(commands.Cog):
    """Shows required package for command"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="cnf")
    async def _cnf(self, ctx: commands.Context, command: str):
        if cnf := await self.bot.redis.get(self.bot.utils.gen_key(command)):
            from_cache = True
            cnf = yaml.load(cnf, Loader=yaml.Loader)
        else:
            from_cache = False
            cnf = await get_from_cnf(command)
            await self.bot.redis.set(
                self.bot.utils.gen_key(command),
                str(cnf),
                ex=3600 * 12  # cache for 12h
            )

        if distro := cnf["distro"]:
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
                     "and with his authorization " + (
                         "(Retrieved from cache)" if from_cache else ""
                     )
            )

            for k, v in distro.items():
                e.add_field(name=f"**__{k}__**", value=f"```{v}```")

            return await ctx.send(embed=e)

        await ctx.send("No result found")
