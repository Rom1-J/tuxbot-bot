import logging

import discord
from discord.ext import commands
from jishaku.models import copy_context_with
from tuxbot.core.config import set_for_key

from tuxbot.core import Config

from tuxbot.core.utils import checks
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils import emotes as utils_emotes
from tuxbot.core.utils.functions.extra import (
    command_extra,
    ContextPlus,
    group_extra,
)

from .functions.converters import ChannelConverter

log = logging.getLogger("tuxbot.cogs.Admin")
_ = Translator("Admin", __file__)


class Admin(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    # =========================================================================
    # =========================================================================

    @command_extra(name="quit", aliases=["shutdown"], deletable=False)
    @checks.is_owner()
    async def _quit(self, ctx: ContextPlus):
        await ctx.send("*quit...*")
        await self.bot.shutdown()

    # =========================================================================

    @command_extra(name="restart", deletable=False)
    @checks.is_owner()
    async def _restart(self, ctx: ContextPlus):
        await ctx.send("*restart...*")
        await self.bot.shutdown(restart=True)

    # =========================================================================

    @command_extra(name="update", deletable=False)
    @checks.is_owner()
    async def _update(self, ctx: ContextPlus):
        sh = "jsk sh"

        git = f"{sh} git pull"
        update = f"{sh} make update"

        git_command_ctx = await copy_context_with(
            ctx, content=ctx.prefix + git
        )
        update_command_ctx = await copy_context_with(
            ctx, content=ctx.prefix + update
        )

        await git_command_ctx.command.invoke(git_command_ctx)
        await update_command_ctx.command.invoke(update_command_ctx)

        await self._restart(ctx)

    # =========================================================================

    @group_extra(name="blacklist", deletable=False)
    @checks.is_owner()
    async def _blacklist(self, ctx: ContextPlus):
        if not ctx.invoked_subcommand:
            await ctx.send("blacklister: ...")

    @_blacklist.command(name="guild", aliases=["server", "guilds", "servers"])
    @checks.is_owner()
    async def _blacklist_guild(
        self, ctx: ContextPlus, guilds: commands.Greedy[discord.Guild]
    ):
        output = "blacklisted: \n"

        for guild in set(guilds):
            set_for_key(
                self.bot.config.Servers,
                guild.id,
                Config.Server,
                blacklisted=True,
            )
            output += (
                f"`+ {guild.name}` (`{guild.id}`): {utils_emotes.check[0]}\n"
            )

        await ctx.send(output)

    @_blacklist.command(name="channel", aliases=["chan", "channels", "chans"])
    @checks.is_owner()
    async def _blacklist_channel(
        self,
        ctx: ContextPlus,
        channels: commands.Greedy[ChannelConverter],
    ):
        output = "blacklisted: \n"

        for channel in set(channels):
            set_for_key(
                self.bot.config.Channels,
                channel.id,
                Config.Channel,
                blacklisted=True,
            )
            output += f"`+ {channel.name}` (`{channel.id}`): {utils_emotes.check[0]}\n"

        await ctx.send(output)

    @_blacklist.command(name="user", aliases=["member", "users", "members"])
    @checks.is_owner()
    async def _blacklist_user(
        self, ctx: ContextPlus, users: commands.Greedy[discord.User]
    ):
        output = "blacklisted: \n"

        for user in set(users):
            set_for_key(
                self.bot.config.Users, user.id, Config.User, blacklisted=True
            )
            output += (
                f"`+ {user.name}` (`{user.id}`): {utils_emotes.check[0]}\n"
            )

        await ctx.send(output)
