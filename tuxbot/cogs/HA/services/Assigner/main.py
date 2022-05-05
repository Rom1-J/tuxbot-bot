"""
tuxbot.cogs.HA.services.Assigner.main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assigner to turn off/on instances
"""
import asyncio
import time
from typing import Set

from discord.ext import commands, tasks  # type: ignore
from websockets.client import connect
from websockets.exceptions import ConnectionClosed
from websockets.legacy.protocol import broadcast
from websockets.server import WebSocketServerProtocol, serve

from tuxbot.core.Tuxbot import Tuxbot


class AssignerService(commands.Cog):
    """Assigner to turn off/on instances"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self.instances_config: dict = self.bot.config["HA"].get(
            "instances", []
        )
        self.instance_config: dict = self.bot.config["HA"].get("instance", {})

        self.__clients: Set[WebSocketServerProtocol] = set()
        self.__ping: float = float('inf')

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

        self.__ping = self.bot.latency * 1000 + redis

    @_ping_updater.before_loop
    async def _ping_updater_before(self):
        await self.bot.wait_until_ready()

    # =========================================================================

    @tasks.loop(count=1, reconnect=False)
    async def _ws_server(self):
        self.bot.logger.info("[AssignerService] '_ws_server' started!")

        async def _handler(websocket: WebSocketServerProtocol):
            try:
                self.__clients.add(websocket)
                broadcast(self.__clients, str(self.__ping))
                self._ws_client.restart()  # pylint: disable=no-member
            except ConnectionClosed:
                self.__clients.remove(websocket)
                broadcast(self.__clients, str(self.__ping))

        async with serve(
                _handler,
                self.instance_config.get("hostname"),
                self.instance_config.get("port")
        ):
            await asyncio.Future()

    @_ws_server.before_loop
    async def _ws_server_before(self):
        await self.bot.wait_until_ready()

    # =========================================================================

    @tasks.loop(count=1, reconnect=False)
    async def _ws_client(self):
        self.bot.logger.info("[AssignerService] '_ws_client' started!")
        running_instance = True

        for client_name in self.instances_config:
            client = self.instances_config.get(client_name)
            try:
                async with connect(
                        f"ws://{client['hostname']}:{client['port']}"
                ) as websocket:
                    if float(await websocket.recv()) < self.__ping:
                        running_instance = False

            except ConnectionRefusedError:
                self.bot.logger.warning(
                    "[AssignerService] '%s' seems to be down...", client_name
                )

        self.bot.change_running_state(running_instance)

    @_ws_client.before_loop
    async def _ws_client_before(self):
        await self.bot.wait_until_ready()
