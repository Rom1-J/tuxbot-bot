# Created by romain at 04/01/2020

import logging

import discord
from discord.ext import commands
from discord import utils

from bot import TuxBot
from utils import Texts
from utils.paginator import FieldPages

log = logging.getLogger(__name__)


class HelpCommand(commands.HelpCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_cogs = ["Monitoring", "Help"]
        self.owner_cogs = ["Jishaku"]
        self.admin_cogs = ["Admin"]

    def common_command_formatting(self, e, command):
        prefix = self.context.prefix if str(self.context.bot.user.id) not in self.context.prefix else f"@{self.context.bot.user.name}"

        e.title = self.get_command_signature(command)
        e.description = command.description

        e.add_field(
            name="TODO: Text.params :",
            value=command.usage
        )
        e.add_field(
            name="TODO: Text.usage :",
            value=f"{prefix}{command.qualified_name} " + command.usage
        )

        aliases = "`" + '`, `'.join(command.aliases) + "`"
        if aliases == "``":
            aliases = Texts(
                'help', self.context
            ).get(
                'command_help.no_aliases'
            )
        e.add_field(
            name=Texts(
                'help', self.context
            ).get(
                'command_help.aliases'
            ),
            value=aliases
        )

        return e

    async def send_bot_help(self, mapping):
        owners = self.context.bot.owners
        owners_name = [
            f"{owner.name}#{owner.discriminator}"
            for owner in owners
        ]
        prefix = self.context.prefix if str(self.context.bot.user.id) not in self.context.prefix else f"@{self.context.bot.user.name} "

        e = discord.Embed(
            color=discord.Color.blue(),
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
        e.set_footer(
            text=Texts(
                'help', self.context
            ).get(
                'main_page.footer'
            ).format(
                prefix
            )
        )

        cogs = ""
        for extension in self.context.bot.cogs.values():
            if self.context.author not in owners \
                    and extension.__class__.__name__ in self.owner_cogs:
                continue
            if extension.__class__.__name__ in self.ignore_cogs:
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

    async def send_cog_help(self, cog):
        pages = {}
        prefix = self.context.prefix if str(self.context.bot.user.id) not in self.context.prefix else f"@{self.context.bot.user.name}"

        if cog.__class__.__name__ in self.owner_cogs \
                and self.context.author not in self.context.bot.owners:
            return self.command_not_found(cog.qualified_name)

        for cmd in cog.get_commands():
            if self.context.author not in self.context.bot.owners \
                    and (cmd.hidden or cmd.category == "Hidden"):
                continue

            if cmd.category not in pages:
                pages[cmd.category] = "```asciidoc\n"

            pages[cmd.category] \
                += f"{cmd.name}" \
                   + ' ' * int(17 - len(cmd.name)) \
                   + f":: {cmd.help}\n"

            if isinstance(cmd, commands.Group):
                for group_command in cmd.commands:
                    pages[cmd.category] \
                        += f"━ {group_command.name}" \
                           + ' ' * int(15 - len(group_command.name)) \
                           + f":: {cmd.help}\n"
        for e in pages:
            pages[e] += "```"
        formatted = []
        for name, cont in pages.items():
            formatted.append((name, cont))
        footer_text = Texts('help', self.context) \
            .get('main_page.footer') \
            .format(prefix)

        pages = FieldPages(
            self.context,
            embed_color=discord.Color.blue(),
            entries=formatted,
            title=cog.qualified_name.upper(),
            thumbnail=cog.big_icon,
            footericon=self.context.bot.user.avatar_url,
            footertext=footer_text,
            per_page=1
        )
        await pages.paginate()

    async def send_group_help(self, group):
        if group.cog_name in self.ignore_cogs:
            return await self.send_error_message(
                self.command_not_found(group.name)
            )

        formatted = self.common_command_formatting(
            discord.Embed(color=discord.Color.blue()),
            group
        )
        sub_cmd_list = ""
        for group_command in group.commands:
            sub_cmd_list += f"└> **{group_command.name}** - {group_command.description}\n"
        subcommands = Texts(
            'help', self.context
        ).get(
            'command_help.subcommands'
        )

        formatted.add_field(name=subcommands, value=sub_cmd_list, inline=False)
        await self.context.send(embed=formatted)

    async def send_command_help(self, command):
        if isinstance(command, commands.Group):
            return await self.send_group_help(command)

        if command.cog_name in self.ignore_cogs:
            return await self.send_error_message(
                self.command_not_found(command.name))

        formatted = self.common_command_formatting(
            discord.Embed(color=discord.Color.blue()),
            command
        )

        await self.context.send(embed=formatted)

    def command_not_found(self, command):
        return Texts(
            'help', self.context
        ).get(
            'main_page.not_found'
        ).format(
            command
        )


class Help(commands.Cog):
    def __init__(self, bot: TuxBot):
        bot.help_command = HelpCommand()


def setup(bot: TuxBot):
    bot.add_cog(Help(bot))
