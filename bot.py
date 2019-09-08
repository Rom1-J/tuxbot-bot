import datetime
import logging
import sys
import traceback

import aiohttp
import discord
from discord.ext import commands

import config
from cogs.utils.lang import _

description = """
Je suis TuxBot, le bot qui vit de l'OpenSource ! ;)
"""

log = logging.getLogger(__name__)

l_extensions = (
    'cogs.admin',
    'cogs.basaics',
)


async def _prefix_callable(bot, message):
    base = [] if config.prefix is None else config.prefix

    # if message.guild is not None:
    #     base.extend(bot.prefixes.get(message.guild.id))
    return commands.when_mentioned_or(base)


class TuxBot(commands.AutoShardedBot):
    __slots__ = ('uptime', 'config', 'session')

    def __init__(self, unload):
        super().__init__(command_prefix=_prefix_callable,
                         description=description, pm_help=None,
                         help_command=None, help_attrs=dict(hidden=True))

        self.uptime = datetime.datetime.utcnow()
        self.config = config
        self.prefixes = {}
        self.session = aiohttp.ClientSession(loop=self.loop)

        for extension in l_extensions:
            if extension not in unload:
                try:
                    self.load_extension(extension)
                except Exception as e:
                    print(_("Failed to load extension : ") + extension,
                          file=sys.stderr)
                    traceback.print_exc()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(
                _('This command cannot be used in private messages.')
            )
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send(
                _('Sorry. This command is disabled and cannot be used.')
            )
        elif isinstance(error, commands.CommandInvokeError):
            print(_('In ') + f'{ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(f'{error.original.__class__.__name__}: {error.original}',
                  file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(_('Ready:') + f' {self.user} (ID: {self.user.id})')

        await self.change_presence(status=discord.Status.dnd,
                                   activity=discord.Game(
                                       name=self.config.activity
                                   ))

    @staticmethod
    async def on_resumed():
        print('resumed...')

    @property
    def logs_webhook(self):
        logs_webhook = self.config.logs_webhook
        webhook = discord.Webhook.partial(id=logs_webhook.get('id'),
                                          token=logs_webhook.get('token'),
                                          adapter=discord.AsyncWebhookAdapter(
                                              self.session))
        return webhook

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(config.token, reconnect=True)
