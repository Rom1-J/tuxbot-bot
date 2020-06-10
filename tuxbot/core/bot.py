import asyncio
import datetime
import logging
import sys
from typing import List, Union

import discord
from colorama import Fore, Style, init
from discord.ext import commands
from . import Config
from .data_manager import logs_data_path

from .utils.functions.cli import bordered

from . import __version__
from .utils.functions.extra import ContextPlus

log = logging.getLogger("tuxbot")
init()

NAME = r"""
  _____           _           _        _           _   
 |_   _|   ___  _| |__   ___ | |_     | |__   ___ | |_ 
   | || | | \ \/ / '_ \ / _ \| __|____| '_ \ / _ \| __|
   | || |_| |>  <| |_) | (_) | ||_____| |_) | (_) | |_ 
   |_| \__,_/_/\_\_.__/ \___/ \__|    |_.__/ \___/ \__|                                    
"""

packages: List[str] = ["jishaku", "tuxbot.cogs.warnings", "tuxbot.cogs.admin"]


class Tux(commands.AutoShardedBot):
    _loading: asyncio.Task

    def __init__(self, *args, cli_flags=None, **kwargs):
        # by default, if the bot shutdown without any intervention,
        # it's a crash
        self.shutdown_code = ExitCodes.CRITICAL
        self.cli_flags = cli_flags
        self.instance_name = self.cli_flags.instance_name
        self.last_exception = None
        self.logs = logs_data_path(self.instance_name)

        self.config = Config(self.instance_name)

        async def _prefixes(bot, message) -> List[str]:
            prefixes = self.config("core").get("prefixes")

            prefixes.extend(self.config.get_prefixes(message.guild))

            if self.config("core").get("mentionable"):
                return commands.when_mentioned_or(*prefixes)(bot, message)
            return prefixes

        if "command_prefix" not in kwargs:
            kwargs["command_prefix"] = _prefixes

        if "owner_ids" in kwargs:
            kwargs["owner_ids"] = set(kwargs["owner_ids"])
        else:
            kwargs["owner_ids"] = self.config.owners_id()

        message_cache_size = 100_000
        kwargs["max_messages"] = message_cache_size
        self.max_messages = message_cache_size

        self.uptime = None
        self._app_owners_fetched = False  # to prevent abusive API calls

        super().__init__(*args, help_command=None, **kwargs)

    async def load_packages(self):
        if packages:
            print("Loading packages...")
            for package in packages:
                try:
                    self.load_extension(package)
                except Exception as e:
                    print(
                        Fore.RED
                        + f"Failed to load package {package}"
                        + Style.RESET_ALL
                        + f" check "
                        f"{str((self.logs / 'tuxbot.log').resolve())} "
                        f"for more details"
                    )

                    log.exception(f"Failed to load package {package}", exc_info=e)

    async def on_ready(self):
        self.uptime = datetime.datetime.now()
        INFO = {
            "title": "INFO",
            "rows": [
                str(self.user),
                f"Prefixes: {', '.join(self.config('core').get('prefixes'))}",
                f"Language: {self.config('core').get('locale')}",
                f"Tuxbot Version: {__version__}",
                f"Discord.py Version: {discord.__version__}",
                "Python Version: " + sys.version.replace("\n", ""),
                f"Shards: {self.shard_count}",
                f"Servers: {len(self.guilds)}",
                f"Users: {len(self.users)}",
            ],
        }

        COGS = {"title": "COGS", "rows": []}
        for extension in packages:
            COGS["rows"].append(
                f"[{'X' if extension in self.extensions else ' '}] {extension}"
            )

        print(Fore.LIGHTBLUE_EX + NAME)
        print(Style.RESET_ALL)
        print(bordered(INFO, COGS))

        print(f"\n{'=' * 118}\n\n")

    async def is_owner(self, user: Union[discord.User, discord.Member]) -> bool:
        """Determines if the user is a bot owner.

        Parameters
        ----------
        user: Union[discord.User, discord.Member]

        Returns
        -------
        bool
        """
        if user.id in self.config.owners_id():
            return True

        owner = False
        if not self._app_owners_fetched:
            app = await self.application_info()
            if app.team:
                ids = [m.id for m in app.team.members]
                await self.config.update("core", "owners_id", ids)
                owner = user.id in ids
            self._app_owners_fetched = True

        return owner

    async def get_context(self, message: discord.Message, *, cls=None):
        return await super().get_context(message, cls=ContextPlus)

    async def process_commands(self, message: discord.Message):
        """Check for blacklists.

        """
        if message.author.bot:
            return

        if (
            message.guild.id in self.config.get_blacklist("guild")
            or message.channel.id in self.config.get_blacklist("channel")
            or message.author.id in self.config.get_blacklist("user")
        ):
            return

        ctx = await self.get_context(message)

        if ctx is None or ctx.valid is False:
            self.dispatch("message_without_command", message)
        else:
            await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

    async def logout(self):
        """Disconnect from Discord and closes all actives connections.

        Todo: add postgresql logout here
        """
        await super().logout()

    async def shutdown(self, *, restart: bool = False):
        """Gracefully quit.

        Parameters
        ----------
        restart:bool
            If `True`, systemd or the launcher gonna see custom exit code
            and reboot.

        """
        if not restart:
            self.shutdown_code = ExitCodes.SHUTDOWN
        else:
            self.shutdown_code = ExitCodes.RESTART

        await self.logout()
        sys.exit(self.shutdown_code)


class ExitCodes:
    CRITICAL = 1
    SHUTDOWN = 0
    RESTART = 42
