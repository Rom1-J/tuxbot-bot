# Created by romain at 04/01/2020

import logging

import discord
from discord.ext import commands

from bot import TuxBot
from utils import FieldPages
from utils import commandsPlus

log = logging.getLogger(__name__)


class HelpCommand(commands.HelpCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_cogs = ["Monitoring", "Help", "Logs"]
        self.owner_cogs = []

    def get_command_signature(self, command):
        return f"[{command.cog.qualified_name.upper()}] > {command.qualified_name}"

    def common_command_formatting(self, emb, command):
        emb.title = self.get_command_signature(command)
        if command.cog_name != "Jishaku":
            emb.set_thumbnail(url=command.cog.big_icon)
        try:
            emb.description = f"{command.cog.qualified_name.lower()}_help " \
                              f"{command.parent}_{command.name}_description"
        except:
            emb.description = f"{command.cog.qualified_name.lower()}_help " \
                              f"{command.name}_description"
        usage = "help.command_help.usage"
        try:
            if command.parent:
                try:
                    usg = f"{command.cog.qualified_name.lower()}_help " \
                          f"{command.parent}_{command.name}_usage"
                except:
                    usg = f"{command.cog.qualified_name.lower()}_help " \
                          f"{command.name}_usage"
            else:
                usg = f"{command.cog.qualified_name.lower()}_help " \
                      f"{command.name}_usage"

            emb.add_field(name=usage,
                          value=f"{self.context.prefix}{command.qualified_name} " + usg)
        except KeyError:
            emb.add_field(name=usage,
                          value=f"{self.context.prefix}{command.qualified_name}")
        aliases = "`" + '`, `'.join(command.aliases) + "`"
        if aliases == "``":
            aliases = "help " \
                      "help.command_help.no_aliases"

        emb.add_field(name="help "
                           "help.command_help.aliases",
                      value=aliases)
        return emb

    async def command_callback(self, ctx, *, command=None):
        await self.prepare_help_command(ctx, command)

        if command is None:
            mapping = self.get_bot_mapping()
            return await self.send_bot_help(mapping)

        cog = ctx.bot.get_cog(command.title())
        if cog is not None:
            return await self.send_cog_help(cog)

        maybe_coro = discord.utils.maybe_coroutine

        keys = command.split(' ')
        cmd = ctx.bot.all_commands.get(keys[0])
        if cmd is None:
            string = await maybe_coro(self.command_not_found,
                                      self.remove_mentions(keys[0]))
            return await self.send_error_message(string)

        for key in keys[1:]:
            try:
                found = cmd.all_commands.get(key)
            except AttributeError:
                string = await maybe_coro(self.subcommand_not_found, cmd,
                                          self.remove_mentions(key))
                return await self.send_error_message(string)
            else:
                if found is None:
                    string = await maybe_coro(self.subcommand_not_found,
                                              cmd,
                                              self.remove_mentions(key))
                    return await self.send_error_message(string)
                cmd = found

        if isinstance(cmd, commands.Group):
            return await self.send_group_help(cmd)
        else:
            return await self.send_command_help(cmd)

    async def send_bot_help(self, mapping):
        owner = self.context.bot.owner
        emb = discord.Embed(color=discord.colour.Color.blue())
        emb.description = "help " \
                          "help.main_page.description".format(owner)
        emb.set_author(icon_url=self.context.author.avatar_url,
                       name=self.context.author)

        cogs = ""
        for extension in self.context.bot.cogs.values():
            if self.context.author != owner and extension.qualified_name.upper() in self.owner_cogs:
                continue
            if self.context.author == owner and extension.qualified_name in self.ignore_cogs:
                continue
            if extension.qualified_name == "Jishaku":
                continue
            cogs += f"• {extension.icon} **{extension.qualified_name}**\n"

        emb.add_field(name="help "
                           "help.main_page.field_title.categories",
                      value=cogs)

        await self.context.send(embed=emb)

    async def send_command_help(self, command):
        if command.cog_name in self.ignore_cogs:
            return await self.send_error_message(
                self.command_not_found(command.name))

        if isinstance(command, commandsPlus):
            if command.name == "jishaku":
                pass

        formatted = self.common_command_formatting(
            discord.Embed(color=discord.colour.Color.blue()), command)
        await self.context.send(embed=formatted)

    async def send_group_help(self, group):
        if group.cog_name in self.ignore_cogs:
            return await self.send_error_message(
                self.command_not_found(group.name))

        formatted = self.common_command_formatting(
            discord.Embed(color=discord.colour.Color.blue()), group)
        sub_cmd_list = ""
        for group_command in group.commands:
            try:
                sub_cmd_list += f"`╚╡` **{group_command.name}** - " \
                                f"{group.cog.qualified_name.lower()}_help " \
                                f"{group_command.parent}_{group_command.name}_brief\n"
            except Exception:
                sub_cmd_list += f"`╚╡` **{group_command.name}** - " \
                                f"{group.cog.qualified_name.lower()}_help" \
                                f"{group_command.name}_brief\n"
        subcommands = "help.command_help.subcommands"
        formatted.add_field(name=subcommands, value=sub_cmd_list,
                            inline=False)
        await self.context.send(embed=formatted)

    async def send_cog_help(self, cog):
        if (
                cog.qualified_name.upper() in self.owner_cogs
                and not await self.context.bot.is_owner(self.context.author)
        ) or cog.qualified_name.upper() in self.ignore_cogs:
            return
        if cog.qualified_name == "Jishaku":
            return
        if cog.qualified_name in self.ignore_cogs:
            return

        pages = {}
        for cmd in cog.get_commands():
            if not await self.context.bot.is_owner(
                    self.context.author) and (
                    cmd.hidden or cmd.category == "Hidden"):
                continue
            if cmd.category not in pages:
                pages[cmd.category] = "```asciidoc\n"
            cmd_brief = f"{cog.qualified_name.lower()}_help " \
                        f"{cmd.name}_brief"
            pages[
                cmd.category] += f"{cmd.name}{' ' * int(17 - len(cmd.name))}:: {cmd_brief}\n"
            if isinstance(cmd, commands.Group):
                for group_command in cmd.commands:
                    try:
                        cmd_brief = f"{cog.qualified_name.lower()}_help " \
                                    f"{group_command.parent}_{group_command.name}_brief"
                    except Exception:
                        cmd_brief = f"{cog.qualified_name.lower()}_help " \
                                    f"{group_command.name}_brief"
                    pages[
                        cmd.category] += f"━ {group_command.name}{' ' * int(15 - len(group_command.name))}:: {cmd_brief}\n"
        for e in pages:
            pages[e] += "```"
        formatted = []
        for name, cont in pages.items():
            formatted.append((name, cont))
        footer_text = "help " \
                      "help.category_page.footer_info".format(self.context.prefix)
        pages = FieldPages(self.context,
                           embed_color=discord.colour.Color.blue(),
                           entries=formatted,
                           title=cog.qualified_name.upper(),
                           thumbnail=cog.big_icon,
                           footertext=footer_text,
                           per_page=1)
        await pages.paginate()

    def command_not_found(self, string):
        return 'No command called "{}" found.'.format(string)


class Help(commands.Cog):
    def __init__(self, bot: TuxBot):
        bot.help_command = HelpCommand()


def setup(bot: TuxBot):
    bot.add_cog(Help(bot))
