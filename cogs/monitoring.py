import asyncio
import threading
from aiohttp import web

from discord.ext import commands
from bot import TuxBot


class Monitoring(commands.Cog):

    def __init__(self):
        self.app = web.Application()

        t = threading.Thread(
            target=self.run_server,
            args=(self.aiohttp_server(),)
        )
        t.start()

    def aiohttp_server(self):
        async def hi(request):
            return web.Response(text="I'm alive !")

        self.app.add_routes([web.get('/', hi)])
        runner = web.AppRunner(self.app)

        return runner

    @staticmethod
    def run_server(runner):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, '0.0.0.', 3389)
        loop.run_until_complete(site.start())
        loop.run_forever()


def setup(bot: TuxBot):
    bot.add_cog(Monitoring())
