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
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn
from rich.table import Table
from tortoise import Tortoise

from tuxbot import version_info
from tuxbot.core.utils.data_manager import (
    logs_data_path,
    data_path,
    config_dir,
)
from .config import (
    Config,
    ConfigFile,
    search_for,
    AppConfig,
    set_for_key,
)
from . import __version__, ExitCodes
from . import exceptions
from .utils.functions.extra import ContextPlus
from .utils.functions.prefix import get_prefixes

log = logging.getLogger("tuxbot")
console = Console()

packages: List[str] = [
    "jishaku",
    "tuxbot.cogs.Admin",
    "tuxbot.cogs.Logs",
    "tuxbot.cogs.Dev",
    "tuxbot.cogs.Utils",
]


class Tux(commands.AutoShardedBot):
    _loading: asyncio.Task
    _progress = {
        "main": Progress(
            TextColumn("[bold blue]{task.fields[task_name]}", justify="right"),
            BarColumn(),
        ),
        "tasks": {},
    }

    def __init__(self, *args, cli_flags=None, **kwargs):
        # by default, if the bot shutdown without any intervention,
        # it's a crash
        self.shutdown_code = ExitCodes.CRITICAL
        self.cli_flags = cli_flags
        self.instance_name = self.cli_flags.instance_name
        self.last_exception = None
        self.logs = logs_data_path(self.instance_name)

        self.console = console

        self.stats = {"commands": Counter(), "socket": Counter()}

        self.config: Config = ConfigFile(
            str(data_path(self.instance_name) / "config.yaml"), Config
        ).config

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
        self._app_owners_fetched = False  # to prevent abusive API calls

        super().__init__(
            *args, help_command=None, intents=discord.Intents.all(), **kwargs
        )
        self.session = aiohttp.ClientSession(loop=self.loop)

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
        self.uptime = datetime.datetime.now()
        app_config = ConfigFile(config_dir / "config.yaml", AppConfig).config
        set_for_key(
            app_config.Instances,
            self.instance_name,
            AppConfig.Instance,
            active=True,
            last_run=datetime.datetime.timestamp(self.uptime),
        )

        self._progress["main"].stop_task(self._progress["tasks"]["connecting"])
        self._progress["main"].remove_task(
            self._progress["tasks"]["connecting"]
        )
        self._progress["tasks"].pop("connecting")
        console.clear()

        console.print(
            Panel(f"[bold blue]Tuxbot V{version_info.major}", style="blue"),
            justify="center",
        )
        console.print()

        columns = Columns(expand=True, align="center")

        table = Table(style="dim", border_style="not dim", box=box.HEAVY_HEAD)
        table.add_column(
            "INFO",
        )
        table.add_row(str(self.user))
        table.add_row(f"Prefixes: {', '.join(self.config.Core.prefixes)}")
        table.add_row(f"Language: {self.config.Core.locale}")
        table.add_row(f"Tuxbot Version: {__version__}")
        table.add_row(f"Discord.py Version: {discord.__version__}")
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
                status = f"[green]:heavy_check_mark: {extension}"
            else:
                status = f"[red]:heavy_multiplication_x: {extension}"

            table.add_row(status)
        columns.add_renderable(table)

        console.print(columns)
        console.print()

    async def is_owner(
        self, user: Union[discord.User, discord.Member]
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
        return await super().get_context(message, cls=ContextPlus)

    async def process_commands(self, message: discord.Message):
        """Check for blacklists."""
        if message.author.bot:
            return

        if (
            search_for(self.config.Servers, message.guild.id, "blacklisted")
            or search_for(
                self.config.Channels, message.channel.id, "blacklisted"
            )
            or search_for(self.config.Users, message.author.id, "blacklisted")
        ):
            return

        ctx: ContextPlus = await self.get_context(message)

        if ctx is None or ctx.valid is False:
            self.dispatch("message_without_command", message)
        else:
            if ctx.command in search_for(
                self.config.Servers, message.guild.id, "disabled_command", []
            ):
                raise exceptions.DisabledCommandByServerOwner

            if ctx.command in self.config.Core.disabled_command:
                raise exceptions.DisabledCommandByBotOwner

            await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

    async def start(self, token, bot):  # pylint: disable=arguments-differ
        """Connect to Discord and start all connections.

        Todo: add postgresql connect here
        """
        with self._progress.get("main") as progress:
            task_id = self._progress.get("tasks")[
                "connecting"
            ] = progress.add_task(
                "connecting",
                task_name="Connecting to PostgreSQL...",
                start=False,
            )

            models = []

            for extension, _ in self.extensions.items():
                if extension == "jishaku":
                    continue

                if importlib.import_module(extension).HAS_MODELS:
                    models.append(f"{extension}.models.__init__")

            progress.update(task_id)
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

        self._progress["main"].stop_task(self._progress["tasks"]["connecting"])
        self._progress["main"].remove_task(
            self._progress["tasks"]["connecting"]
        )
        self._progress["tasks"].pop("connecting")

        with self._progress.get("main") as progress:
            task_id = self._progress.get("tasks")[
                "connecting"
            ] = progress.add_task(
                "connecting", task_name="Connecting to Discord...", start=False
            )
            progress.update(task_id)
            await super().start(token, bot=bot)

    async def logout(self):
        """Disconnect from Discord and closes all actives connections.

        Todo: add postgresql logout here
        """
        app_config = ConfigFile(config_dir / "config.yaml", AppConfig).config
        set_for_key(
            app_config.Instances,
            self.instance_name,
            AppConfig.Instance,
            active=False,
        )

        for task in self._progress["tasks"]:
            self._progress["main"].log("Shutting down", task)

            self._progress["main"].stop_task(self._progress["tasks"][task])
            self._progress["main"].remove_task(
                self._progress["tasks"]["connecting"]
            )
        self._progress["main"].stop()

        pending = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for task in pending:
            console.log("Canceling", task.get_name(), f"({task.get_coro()})")
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=False)

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

        sys_e = SystemExit()
        sys_e.code = self.shutdown_code

        raise sys_e
