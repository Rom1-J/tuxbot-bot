# Created by romain at 04/01/2020

import logging

import discord
from discord.ext import commands

from bot import TuxBot
from utils import Texts

log = logging.getLogger(__name__)


class HelpCommand(commands.HelpCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_cogs = ["Monitoring", "Help", "Logs"]
        self.owner_cogs = []

    async def send_bot_help(self, mapping):
        owners = self.context.bot.owners
        owners_name = [
            f"{owner.name}#{owner.discriminator}"
            for owner in owners
        ]

        e = discord.Embed(
            color=discord.colour.Color.blue(),
            description=Texts(
                'help', self.context
            ).get(
                'main_page.description'
            ).format(
                ', '.join(owners_name[:-1]) + ' & ' + owners_name[-1]
            )
        )

        e.set_author(
            icon_url=self.context.author.avatar_url_as(format='png'),
            name=self.context.author
        )

        cogs = ""
        for extension in self.context.bot.cogs.values():
            if self.context.author not in owners \
                    and extension.qualified_name in self.owner_cogs:
                continue
            if self.context.author in owners \
                    and extension.qualified_name in self.ignore_cogs:
                continue
            if extension.qualified_name == "Jishaku":
                continue
            cogs += f"• {extension.icon} **{extension.qualified_name}**\n"

        e.add_field(
            name=Texts(
                'help', self.context
            ).get(
                'main_page.categories'
            ),
            value=cogs
        )

        await self.context.send(embed=e)


class Help(commands.Cog):
    def __init__(self, bot: TuxBot):
        bot.help_command = HelpCommand()


def setup(bot: TuxBot):
    bot.add_cog(Help(bot))
