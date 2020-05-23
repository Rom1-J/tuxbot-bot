import contextlib
import datetime
import logging
from collections import Counter
from typing import List

import aiohttp
import discord
from discord.ext import commands
from tortoise import Tortoise

from configs.bot import settings
from utils.functions.extra import ContextPlus, get_prefix, \
    get_owners, get_blacklist

log = logging.getLogger(__name__)

l_extensions: List[str] = [
    "jishaku",
    "cogs.Logs",
    "cogs.Images",
]


class TuxBot(commands.AutoShardedBot):
    logs_channels: dict
    session: aiohttp.ClientSession
    command_stats: Counter = Counter()
    socket_stats: Counter = Counter()

    def __init__(self):
        self.uptime = datetime.datetime.utcnow()
        self.config = settings
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True
        )

        self.logs_channels = {
            "dm": self.config.logs["dm"],
            "mentions": self.config.logs["mentions"],
            "guilds": self.config.logs["guilds"],
            "errors": self.config.logs["errors"],
        }

        print("\n"*2)

        for extension in l_extensions:
            try:
                self.load_extension(extension)
                print(f"{extension} loaded !")
            except Exception as e:
                print(f"{type(e).__name__}: {e}")

        print("\n"*2)

    async def is_owner(self, user: discord.User):
        return user.id in get_owners()

    async def on_ready(self):
        print(f"Connected !\n"
              f"\n"
              f"==> info: bot username {self.user}\n"
              f"    info: bot id {self.user.id}\n"
              f"    info: bot prefix {self.command_prefix}\n"
              f"==> info: guild count {len(self.guilds)}\n"
              f"    info: member count {len(list(self.get_all_members()))}\n"
              f"    info: channel count {len(list(self.get_all_channels()))}")

        print(f"\n{'='*118}\n\n")

    @staticmethod
    async def on_resumed():
        print("resumed...")

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
        await self.login(self.config.token, bot=True)
        await self.connect()

    def run(self):
        loop = self.loop

        loop.run_until_complete(Tortoise.init(
            db_url=self.config.postgresql,
            modules={
                "models": [
                    "models.__init__"
                ]
            }
        ))
        loop.run_until_complete(Tortoise.generate_schemas())

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
        handler = logging.FileHandler(filename='logs/tuxbot.log',
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
