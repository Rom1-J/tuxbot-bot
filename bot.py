import contextlib
import datetime
import json
import logging
import sys
from collections import deque, Counter
from typing import List

import aiohttp
import discord
import git
import sqlalchemy
from discord.ext import commands

from utils.functions import Config
from utils.functions import Texts
from utils.functions import Version
from utils.functions import ContextPlus

from utils.models import metadata, database

description = """
Je suis TuxBot, le bot qui vit de l'OpenSource ! ;)
"""

build = git.Repo(search_parent_directories=True).head.object.hexsha
version = (2, 0, 0)

log = logging.getLogger(__name__)

l_extensions: List[str] = [
    'cogs.Admin',
    'cogs.API',
    'cogs.Help',
    'cogs.Logs',
    # 'cogs.Monitoring',
    'cogs.Poll',
    'cogs.Useful',
    'cogs.User',
    'jishaku',
]


async def _prefix_callable(bot, message: discord.message) -> list:
    try:
        with open(f'./configs/guilds/{message.guild.id}.json', 'r') as f:
            data = json.load(f)

        custom_prefix = data['prefixes']
    except FileNotFoundError:
        custom_prefix = ['']

    extras = [bot.cluster.get('Name') + '.']
    extras.extend(custom_prefix)

    return commands.when_mentioned_or(*extras)(bot, message)


class TuxBot(commands.AutoShardedBot):

    def __init__(self, ):
        super().__init__(command_prefix=_prefix_callable, pm_help=None,
                         help_command=None, description=description,
                         help_attrs=dict(hidden=True),
                         activity=discord.Game(
                             name=Texts().get('Starting...'))
                         )

        self.socket_stats = Counter()
        self.command_stats = Counter()

        self.config = Config('./configs/config.cfg')
        self.blacklist = Config('./configs/blacklist.cfg')
        self.fallbacks = Config('./configs/fallbacks.cfg')
        self.cluster = self.fallbacks.find('True', key='This', first=True)

        self.uptime: datetime = datetime.datetime.utcnow()
        self._prev_events = deque(maxlen=10)
        self.session = aiohttp.ClientSession(loop=self.loop)

        self.database, self.metadata = database, metadata
        self.engine = sqlalchemy.create_engine(str(self.database.url))
        self.metadata.create_all(self.engine)

        self.version = Version(*version, pre_release='rc2', build=build)
        self.owners_id = [int(owner_id) for owner_id in self.config.get('permissions', 'Owners').split(', ')]
        self.owner_id = int(self.owners_id[0])

        for extension in l_extensions:
            try:
                self.load_extension(extension)
                print(Texts().get("Extension loaded successfully : ")
                      + extension)
                log.info(Texts().get("Extension loaded successfully : ")
                         + extension)
            except Exception as e:
                print(Texts().get("Failed to load extension : ")
                      + extension, file=sys.stderr)
                print(e)
                log.error(Texts().get("Failed to load extension : ")
                          + extension, exc_info=e)

    @property
    def owner(self):
        return self.get_user(self.owner_id)

    @property
    def owners(self):
        return [self.get_user(owner_id) for owner_id in self.owners_id]

    async def is_owner(self, user: discord.User) -> bool:
        return user in self.owners

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or ContextPlus)

    async def on_socket_response(self, msg):
        self._prev_events.append(msg)

    async def on_command_error(self, ctx: discord.ext.commands.Context, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(
                Texts().get("This command cannot be used in private messages.")
            )

        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send(
                Texts().get(
                    "Sorry. This command is disabled and cannot be used."
                )
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(str(error))

    async def process_commands(self, message: discord.message):
        ctx: commands.Context = await self.get_context(message)

        if ctx.command is None:
            return

        await self.invoke(ctx)

    async def on_message(self, message: discord.message):
        if message.author.id in self.blacklist \
                or (message.guild is not None
                    and message.guild.id in self.blacklist):
            return

        if message.author.bot and message.author.id != int(
                self.config.get('bot', 'Tester')):
            return

        await self.process_commands(message)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print('-' * 60)
        print(Texts().get("Ready:") + f' {self.user} (ID: {self.user.id})')
        print(self.version)

        presence: dict = dict(status=discord.Status.dnd)
        if self.config.get("bot", "Activity", fallback=None) is not None:
            presence.update(
                activity=discord.Game(
                    name=self.config.get("bot", "Activity")
                )
            )
        print(f"Discord.py: {discord.__version__}")
        print(f"Server: {self.cluster.get('Name')}")
        print('-' * 60)

        await self.change_presence(**presence)

    @staticmethod
    async def on_resumed():
        print('resumed...')

    @property
    def logs_webhook(self) -> discord.Webhook:
        webhook_config = self.config["webhook"]
        webhook = discord.Webhook.partial(
            id=webhook_config.get('ID'),
            token=webhook_config.get('Token'),
            adapter=discord.AsyncWebhookAdapter(
                self.session
            )
        )

        return webhook

    async def close(self):
        extensions = self.extensions.copy()
        for extension in extensions:
            self.unload_extension(extension)
        await super().close()
        await self.session.close()

    def run(self):
        super().run(self.config.get("bot", "Token"), reconnect=True)


@contextlib.contextmanager
def setup_logging():
    logging.getLogger('discord').setLevel(logging.INFO)
    logging.getLogger('discord.http').setLevel(logging.WARNING)

    log = logging.getLogger()
    log.setLevel(logging.INFO)

    try:
        handler = logging.FileHandler(filename='logs/tuxbot.log',
                                      encoding='utf-8', mode='w')
        fmt = logging.Formatter('[{levelname:<7}] [{asctime}]'
                                ' {name}: {message}',
                                '%Y-%m-%d %H:%M:%S', style='{')

        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)


if __name__ == "__main__":
    print(Texts().get('Starting...'))

    app = TuxBot()

    try:
        with setup_logging():
            app.run()
    except KeyboardInterrupt:
        app.close()
