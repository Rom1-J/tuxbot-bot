"""
tuxbot.cogs.HA.services.HTTPServer.main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTTP Monitoring Server for tuxbot
"""

from aiohttp import web
from discord.ext import commands, tasks  # type: ignore

from tuxbot.core.Tuxbot import Tuxbot


class HTTPServerService(commands.Cog):
    """HTTP Monitoring Server for tuxbot"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot
        self.server_config: dict = self.bot.config["HA"].get("http_server", {})

        self._http_monitoring.start()  # pylint: disable=no-member

    # =========================================================================

    async def cog_unload(self):
        """Stop server task"""
        self.bot.logger.info("[HTTPServerService] Canceling _http_monitoring")
        self._http_monitoring.cancel()  # pylint: disable=no-member

    # =========================================================================
    # =========================================================================

    @tasks.loop()
    async def _http_monitoring(self):
        async def _home(_):
            return web.Response(text="I'm alive bitches 😎")

        app = web.Application()
        app.router.add_get('/', _home)
        runner = web.AppRunner(app)

        await runner.setup()
        site = web.TCPSite(
            runner,
            host=self.server_config.get("host", '127.0.0.1'),
            port=self.server_config.get("port", 8080)
        )
        await site.start()
        self.bot.logger.info("[HTTPServerService] _http_monitoring started!")
