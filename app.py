import contextlib
import datetime
import logging
from collections import Counter
from typing import List

import aiohttp
import discord
from colorama import Fore, Style, init
from discord.ext import commands

from configs.bot import settings
from utils.functions.cli import bordered
from utils.functions.extra import ContextPlus, get_prefix, \
    get_owners, get_blacklist
from version import __version__

log = logging.getLogger(__name__)
init()

NAME = r"""
  _____           _           _        _           _   
 |_   _|   ___  _| |__   ___ | |_     | |__   ___ | |_ 
   | || | | \ \/ / '_ \ / _ \| __|____| '_ \ / _ \| __|
   | || |_| |>  <| |_) | (_) | ||_____| |_) | (_) | |_ 
   |_| \__,_/_/\_\_.__/ \___/ \__|    |_.__/ \___/ \__|                                    
"""

l_extensions: List[str] = [
    "jishaku",
    "cogs.Logs",
    "cogs.Images",
    "cogs.Network",
    "cogs.Useless",
]


class TuxBot(commands.AutoShardedBot):
    logs_channels: dict
    session: aiohttp.ClientSession
    command_stats: Counter = Counter()
    socket_stats: Counter = Counter()

    def __init__(self):
        self.uptime = datetime.datetime.utcnow()
        self._config = settings
        self.locale = self._config.default_locale

        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True
        )

        self.logs_channels = {
            "dm": self._config.logs["dm"],
            "mentions": self._config.logs["mentions"],
            "guilds": self._config.logs["guilds"],
            "errors": self._config.logs["errors"],
            "gateway": self._config.logs["gateway"],
        }

        for extension in l_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                log.warning(f"{type(e).__name__}: {e}")

    async def is_owner(self, user: discord.User):
        return user.id in get_owners()

    async def on_ready(self):
        INFO = {
            'title': "INFO",
            'rows': [
                str(self.user),
                f"Prefixes: {', '.join(self._config.prefixes)}",
                f"Language: {self.locale}",
                f"Tuxbot Version: {__version__}",
                f"Discord.py Version: {discord.__version__}",
                f"Shards: {self.shard_count}",
                f"Servers: {len(self.guilds)}",
                f"Users: {len(self.users)}"
            ]
        }

        COGS = {
            'title': "COGS",
            'rows': []
        }
        for extension in l_extensions:
            COGS['rows'].append(
                f"[{'X' if extension in self.extensions else ' '}] {extension}"
            )

        print(Fore.LIGHTBLUE_EX + NAME)
        print(Style.RESET_ALL)
        print(bordered(INFO, COGS))

        print(f"\n{'=' * 118}\n\n")

    async def on_resumed(self):
        print(f"resumed... {self.uptime}")

    async def get_context(self, message: discord.Message, *, cls=None):
        return await super().get_context(message, cls=ContextPlus)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.author.id in get_blacklist()['users'] \
                or message.channel.id in get_blacklist()['channels'] \
                or (message.channel.guild
                    and message.channel.guild.id in get_blacklist()['guilds']):
            return

        try:
            await self.process_commands(message)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    async def bot_logout(self):
        await super().logout()
        await self.session.close()

    async def bot_start(self):
        self.session = aiohttp.ClientSession(loop=self.loop)
        await self.login(self._config.token, bot=True)
        await self.connect()

    def run(self):
        loop = self.loop

        # loop.run_until_complete(
        #     Tortoise.init(
        #         db_url=self._config.postgresql,
        #         modules={
        #             "models": [
        #                 "models.__init__"
        #             ]
        #         }
        #     )
        # )
        # loop.run_until_complete(Tortoise.generate_schemas())

        try:
            loop.run_until_complete(self.bot_start())
        except KeyboardInterrupt:
            loop.run_until_complete(self.bot_logout())


@contextlib.contextmanager
def setup_logging():
    logging.getLogger('discord').setLevel(logging.INFO)
    logging.getLogger('discord.http').setLevel(logging.WARNING)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        handler = logging.FileHandler(filename='tuxbot.log',
                                      encoding='utf-8', mode='w')
        fmt = logging.Formatter('[{levelname:<7}] [{asctime}]'
                                ' {name}: {message}',
                                '%Y-%m-%d %H:%M:%S', style='{')

        handler.setFormatter(fmt)
        logger.addHandler(handler)

        yield
    finally:
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)


if __name__ == "__main__":
    tutux = TuxBot()
    with setup_logging():
        tutux.run()
