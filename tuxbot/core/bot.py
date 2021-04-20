import asyncio
import datetime
import importlib
import logging
from collections import Counter
from typing import List, Union

import aiohttp
import discord
from discord.ext import commands
from rich import box
from rich.columns import Columns
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from tortoise import Tortoise

from tuxbot import version_info
from tuxbot.core.utils.data_manager import (
    logs_data_path,
    config_file,
)
from tuxbot.core.utils.functions.extra import ContextPlus
from tuxbot.core.utils.functions.prefix import get_prefixes
from tuxbot.core.utils.console import console
from tuxbot.core.config import (
    Config,
    ConfigFile,
    search_for,
)
from . import __version__, ExitCodes
from . import exceptions

log = logging.getLogger("tuxbot")

packages: List[str] = [
    "jishaku",
    "tuxbot.cogs.Admin",
    "tuxbot.cogs.Logs",
    "tuxbot.cogs.Dev",
    "tuxbot.cogs.Utils",
    "tuxbot.cogs.Polls",
    "tuxbot.cogs.Custom",
    "tuxbot.cogs.Network",
    # "tuxbot.cogs.Crypto",
]


class Tux(commands.AutoShardedBot):
    _loading: asyncio.Task
    _progress = {"tasks": {}, "main": Progress()}

    def __init__(self, *args, cli_flags=None, **kwargs):
        # by default, if the bot shutdown without any intervention,
        # it's a crash
        self.shutdown_code = ExitCodes.CRITICAL
        self.cli_flags = cli_flags
        self.last_exception = None
        self.logs = logs_data_path()

        self.console = console

        self.stats = {"commands": Counter(), "socket": Counter()}

        self.config: Config = ConfigFile(config_file, Config).config
        self.instance_name = self.config.Core.instance_name

        async def _prefixes(bot, message) -> List[str]:
            prefixes = self.config.Core.prefixes

            prefixes.extend(get_prefixes(self, message.guild))

            if self.config.Core.mentionable:
                return commands.when_mentioned_or(*prefixes)(bot, message)
            return prefixes

        if "command_prefix" not in kwargs:
            kwargs["command_prefix"] = _prefixes

        if "owner_ids" in kwargs:
            kwargs["owner_ids"] = set(kwargs["owner_ids"])
        else:
            kwargs["owner_ids"] = self.config.Core.owners_id

        message_cache_size = 100_000
        kwargs["max_messages"] = message_cache_size
        self.max_messages = message_cache_size

        self.uptime = None
        self.last_on_ready = None
        self._app_owners_fetched = False  # to prevent abusive API calls
        self.loop = asyncio.get_event_loop()

        self.before_invoke(self._typing)

        super().__init__(
            *args,
            # help_command=None,
            intents=discord.Intents.all(),
            loop=self.loop,
            **kwargs,
        )
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def _is_blacklisted(self, message: discord.Message) -> bool:
        """Check for blacklists."""
        if message.author.bot:
            return True

        if (
            search_for(self.config.Users, message.author.id, "blacklisted")
            or search_for(
                self.config.Channels, message.channel.id, "blacklisted"
            )
            or (
                message.guild
                and search_for(
                    self.config.Servers, message.guild.id, "blacklisted"
                )
            )
        ):
            return True

        return False

    @staticmethod
    async def _typing(ctx: ContextPlus) -> None:
        await ctx.trigger_typing()

    async def load_packages(self):
        if packages:
            with Progress() as progress:
                task = progress.add_task(
                    "Loading packages...", total=len(packages)
                )

                for package in packages:
                    try:
                        self.load_extension(package)
                        progress.console.print(f"{package} loaded")
                    except Exception as e:
                        log.exception(
                            "Failed to load package %s", package, exc_info=e
                        )
                        progress.console.print(
                            f"[red]Failed to load package {package} "
                            f"[i](see "
                            f"{str((self.logs / 'tuxbot.log').resolve())} "
                            f"for more details)[/i]"
                        )

                    progress.advance(task)

    async def on_ready(self):
        if self.uptime is not None:
            self.last_on_ready = datetime.datetime.now()
            return

        self.uptime = datetime.datetime.now()
        self.last_on_ready = self.uptime

        with self._progress["main"] as progress:
            progress.stop_task(self._progress["tasks"]["discord_connecting"])
            progress.remove_task(self._progress["tasks"]["discord_connecting"])
            self._progress["tasks"].pop("discord_connecting")
            self.console.clear()

        self.console.print(
            Panel(f"[bold blue]Tuxbot V{version_info.major}", style="blue"),
            justify="center",
        )
        self.console.print()

        columns = Columns(align="center", expand=True)

        table = Table(style="dim", border_style="not dim", box=box.HEAVY_HEAD)
        table.add_column(
            "INFO",
        )
        table.add_row(str(self.user))
        table.add_row(f"Prefixes: {', '.join(self.config.Core.prefixes)}")
        table.add_row(f"Language: {self.config.Core.locale}")
        table.add_row(f"Tuxbot Version: {__version__}")
        table.add_row(f"Discord.py Version: {discord.__version__}")
        table.add_row(f"Instance name: {self.instance_name}")
        table.add_row(f"Shards: {self.shard_count}")
        table.add_row(f"Servers: {len(self.guilds)}")
        table.add_row(f"Users: {len(self.users)}")
        columns.add_renderable(table)

        table = Table(style="dim", border_style="not dim", box=box.HEAVY_HEAD)
        table.add_column(
            "COGS",
        )
        for extension in packages:
            if extension in self.extensions:
                status = f"[green]:heavy_check_mark: {extension} "
            else:
                status = f"[red]:heavy_multiplication_x: {extension} "

            table.add_row(status)
        columns.add_renderable(table)

        self.console.print(columns)
        self.console.print()

    async def is_owner(
        self, user: Union[discord.User, discord.Member, discord.Object]
    ) -> bool:
        """Determines if the user is a bot owner.

        Parameters
        ----------
        user: Union[discord.User, discord.Member]

        Returns
        -------
        bool
        """
        if user.id in self.config.Core.owners_id:
            return True

        owner = False
        if not self._app_owners_fetched:
            app = await self.application_info()
            if app.team:
                ids = [m.id for m in app.team.members]
                self.config.Core.owners_id = ids
                owner = user.id in ids
            self._app_owners_fetched = True

        return owner

    # pylint: disable=unused-argument
    async def get_context(self, message: discord.Message, *, cls=None):
        ctx: ContextPlus = await super().get_context(message, cls=ContextPlus)

        if (ctx is None or not ctx.valid) and (
            user_aliases := search_for(
                self.config.Users, message.author.id, "aliases"
            )
        ):
            # noinspection PyUnboundLocalVariable
            for alias, command in user_aliases.items():
                back_content = message.content
                message.content = message.content.replace(alias, command, 1)

                if (
                    ctx := await super().get_context(message, cls=ContextPlus)
                ) is None or not ctx.valid:
                    message.content = back_content
                else:
                    break

        return ctx

    async def process_commands(self, message: discord.Message):
        ctx: ContextPlus = await self.get_context(message)

        if ctx is not None and ctx.valid:
            if message.guild and ctx.command in search_for(
                self.config.Servers, message.guild.id, "disabled_command", []
            ):
                raise exceptions.DisabledCommandByServerOwner

            if ctx.command in self.config.Core.disabled_command:
                raise exceptions.DisabledCommandByBotOwner

            await self.invoke(ctx)
        else:
            self.dispatch("message_without_command", message)

    async def on_message(self, message: discord.Message):
        if not await self._is_blacklisted(message):
            await self.process_commands(message)

    async def start(self, token):  # pylint: disable=arguments-differ
        """Connect to Discord and start all connections."""
        with Progress() as progress:
            task = progress.add_task(
                "Connecting to PostgreSQL...", total=len(self.extensions)
            )

            models = []

            for extension, _ in self.extensions.items():
                if extension == "jishaku":
                    progress.advance(task)
                    continue

                if importlib.import_module(extension).HAS_MODELS:
                    models.append(f"{extension}.models.__init__")

                progress.advance(task)

            await Tortoise.init(
                db_url="postgres://{}:{}@{}:{}/{}".format(
                    self.config.Core.Database.username,
                    self.config.Core.Database.password,
                    self.config.Core.Database.domain,
                    self.config.Core.Database.port,
                    self.config.Core.Database.db_name,
                ),
                modules={"models": models},
            )
            await Tortoise.generate_schemas()

        with self._progress["main"] as progress:
            task_id = self._progress["tasks"][
                "discord_connecting"
            ] = progress.add_task(
                "Connecting to Discord...",
                task_name="discord_connecting",
                start=False,
            )
            progress.update(task_id)
            await super().start(token)

    async def logout(self):
        """Disconnect from Discord and closes all actives connections.

        Todo: add postgresql logout here
        """
        with self._progress["main"] as progress:
            for task in self._progress["tasks"]:
                progress.log("Shutting down", task)

                progress.stop_task(self._progress["tasks"][task])
                progress.remove_task(self._progress["tasks"][task])
            progress.stop()

        pending = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for task in pending:
            self.console.log(
                "Canceling", task.get_name(), f"({task.get_coro()})"
            )
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=False)

        await super().close()

    async def shutdown(self, *, restart: bool = False):
        """Gracefully quit.

        Parameters
        ----------
        restart:bool
            If `True`, systemd or the launcher gonna see custom exit code
            and reboot.

        """

        self.shutdown_code = (
            ExitCodes.RESTART if restart else ExitCodes.SHUTDOWN
        )

        await self.logout()

        sys_e = SystemExit()
        sys_e.code = self.shutdown_code

        raise sys_e
