"""
tuxbot.cogs.HA.services.Assigner.main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assigner to turn off/on instances
"""
import asyncio
import time

from discord.ext import commands, tasks  # type: ignore
from websockets import server as ws_server

from tuxbot.core.Tuxbot import Tuxbot

from .Manager import Manager


class AssignerService(commands.Cog):
    """Assigner to turn off/on instances"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self.manager = Manager(self.bot)

        self._ping_updater.start()  # pylint: disable=no-member

        self._ws_server.start()  # pylint: disable=no-member
        self._ws_client.start()  # pylint: disable=no-member

    # =========================================================================

    async def cog_unload(self):
        """Stop server task"""
        self.bot.logger.info("[AssignerService] Canceling '_ping_updater'")
        self._ping_updater.cancel()  # pylint: disable=no-member

        self.bot.logger.info("[AssignerService] Canceling '_ws_server'")
        self._ws_server.cancel()  # pylint: disable=no-member

        self.bot.logger.info("[AssignerService] Canceling '_ws_client'")
        self._ws_client.cancel()  # pylint: disable=no-member

    # =========================================================================
    # =========================================================================

    @tasks.loop(hours=1)
    async def _ping_updater(self):
        self.bot.logger.info("[AssignerService] '_ping_updater' started!")

        start = time.perf_counter()
        await self.bot.redis.ping()
        end = time.perf_counter()
        redis = (end - start) * 1000

        self.manager.me.ping = self.bot.latency * 1000 + redis

    @_ping_updater.before_loop
    async def _ping_updater_before(self):
        await self.bot.wait_until_ready()

    # =========================================================================

    @tasks.loop(count=1, reconnect=False)
    async def _ws_server(self):
        self.bot.logger.info("[AssignerService] '_ws_server' started!")

        async with ws_server.serve(
            self.manager.handler,
            self.manager.me.hostname,
            self.manager.me.port,
        ):
            await asyncio.Future()

    @_ws_server.before_loop
    async def _ws_server_before(self):
        await self.bot.wait_until_ready()

    # =========================================================================

    @tasks.loop(count=1, reconnect=False)
    async def _ws_client(self):
        self.bot.logger.info("[AssignerService] '_ws_client' started!")

        await self.manager.refresh()

    @_ws_client.before_loop
    async def _ws_client_before(self):
        await self.bot.wait_until_ready()
