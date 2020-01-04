import logging
import urllib.request
from datetime import datetime

import discord
from aiohttp import web
from discord.ext import tasks, commands

from bot import TuxBot

log = logging.getLogger(__name__)


class Monitoring(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot
        self.site = web.TCPSite

        self.ping_clusters.start()

        app = web.Application()
        app.add_routes([web.get('/', self.handle)])

        self.runner = web.AppRunner(app)
        self.bot.loop.create_task(self.start_HTTPMonitoring_server())

    def cog_unload(self):
        self.ping_clusters.stop()

    @tasks.loop(seconds=10.0)
    async def ping_clusters(self):
        for cluster in self.bot.fallbacks:
            if cluster == 'DEFAULT':
                pass
            else:
                cluster = self.bot.fallbacks[cluster]
                if not cluster.get('This', False):
                    host = cluster.get('Host')
                    port = cluster.get('Port')

                    try:
                        req = urllib.request.urlopen(
                            f"http://{host}:{port}",
                            timeout=2
                        )
                    except Exception:
                        global_channel = await self.bot.fetch_channel(
                            661347412463321098
                        )

                        e = discord.Embed(
                            title=f"Server `{cluster.get('Name')}`",
                            color=discord.colour.Color.red(),
                            description=f"Server **`{cluster.get('Name')}`** with address **`http://{host}:{port}`** is down ! ",
                            timestamp=datetime.now()
                        )
                        e.set_thumbnail(
                            url='https://upload.wikimedia.org/wikipedia/commons/7/75/Erroricon404.PNG'
                        )

                        await global_channel.send(embed=e)
                    else:
                        print(req.read().decode())

    @ping_clusters.before_loop
    async def before_pinging(self):
        await self.bot.wait_until_ready()

        cluster = self.bot.cluster
        host = cluster.get('Host')
        port = cluster.get('Port')

        global_channel = await self.bot.fetch_channel(
            661347412463321098
        )

        e = discord.Embed(
            title=f"Server `{cluster.get('Name')}`",
            color=discord.colour.Color.green(),
            description=f"Server **`{cluster.get('Name')}`** with address **`http://{host}:{port}`** is started ! ",
            timestamp=datetime.now()
        )
        e.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/MW-Icon-CheckMark.svg/1024px-MW-Icon-CheckMark.svg.png'
        )

        await global_channel.send(embed=e)

    async def start_HTTPMonitoring_server(self):
        host = self.bot.cluster.get('WebPage')
        port = self.bot.cluster.get('Port')

        print(f"Starting HTTP Monitoring server on {host}:{port}")

        await self.runner.setup()
        self.site = web.TCPSite(self.runner, host, port)
        await self.site.start()

    async def handle(self, _):
        return web.json_response(
            {
                'message': "I'm alive !",
                'ws': self.bot.latency * 1000
            }
        )


def setup(bot: TuxBot):
    bot.add_cog(Monitoring(bot))
