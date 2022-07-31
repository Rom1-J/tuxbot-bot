"""
Instances manager
"""
import json

from websockets import client as ws_client
from websockets import server as ws_server
from websockets.exceptions import ConnectionClosed

from tuxbot.core.Tuxbot import Tuxbot

from .Instance import Instance


class Manager:
    """Instances manager"""

    __instances: set[Instance] = set()
    __connected_instances: set[Instance] = set()
    __me: Instance = None  # type: ignore

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        for instance_name in self.bot.config["HA"].get("instances", []):
            instance = Instance(
                instance_name,
                self.bot.config["HA"]["instances"].get(instance_name)[
                    "hostname"
                ],
                self.bot.config["HA"]["instances"].get(instance_name)["port"],
            )
            self.instances.add(instance)
            self.bot.logger.info(
                "[Manager] Adding instance '%s' (%s)",
                instance.name,
                instance.uri,
            )

        self.me = Instance(
            self.bot.config["HA"].get("instance")["name"],
            self.bot.config["HA"].get("instance")["hostname"],
            self.bot.config["HA"].get("instance")["port"],
        )

    # =========================================================================
    # =========================================================================

    @property
    def instances(self) -> set[Instance]:
        """Set of all bot instances"""
        return self.__instances

    @instances.setter
    def instances(self, value: set[Instance]):
        self.__instances = value

    # =========================================================================

    @property
    def connected_instances(self) -> set[Instance]:
        """Set of all connected instances"""
        return self.__connected_instances

    @connected_instances.setter
    def connected_instances(self, value: set[Instance]):
        self.__connected_instances = value

    # =========================================================================

    @property
    def me(self) -> Instance:
        """This instance"""
        return self.__me

    @me.setter
    def me(self, value: Instance):
        self.__me = value

    # =========================================================================
    # =========================================================================

    async def handler(self, ws: ws_server.WebSocketServerProtocol):
        """Websocket server handler"""
        async for message in ws:
            instance, request, _ = self.parse(message)

            match request:
                case "connect":
                    instance.client = ws
                    self.connected_instances = {
                        i for i in self.instances if i.client and i.client.open
                    }
                    await self.check_transfer_of_power(instance)

                case "disconnect":
                    self.connected_instances = {
                        i for i in self.instances if i.client and i.client.open
                    }

    # =========================================================================

    async def refresh(self):
        """Refresh all connections"""

        for instance in self.instances:
            try:
                if instance.client and instance.client.open:
                    continue

                async with ws_client.connect(instance.uri) as websocket:
                    payload = json.dumps(
                        self.forge_payload(
                            "connect",
                            data={
                                "name": self.me.name,
                                "alive": True,
                                "ping": self.me.ping,
                                "hostname": self.me.hostname,
                                "port": self.me.port,
                            },
                        )
                    )
                    await websocket.send(payload)
                    self.bot.logger.info(
                        "[Manager] '%s' is up!", instance.name
                    )

            except (ConnectionRefusedError, ConnectionClosed):
                self.bot.logger.warning(
                    "[Manager] '%s' seems to be down...", instance.name
                )

    # =========================================================================

    async def check_transfer_of_power(self, instance: Instance):
        """Check for power transfer"""

        if self.bot.running_instance and instance.ping < self.me.ping:
            self.bot.logger.info(
                "[Manager] Passing power to '%s'!", instance.name
            )
            self.bot.change_running_state(False)
            await instance.client.send(
                json.dumps(
                    self.forge_payload("change_power", data={"state": True})
                )
            )

    # =========================================================================
    # =========================================================================

    def parse(self, message: str):
        """Parse message"""
        payload = json.loads(message)

        if (
            not (token := payload.get("__token"))
            or token != self.bot.http.token
        ):
            raise ValueError("Improper token given")

        request, data = payload["request"], payload["data"]

        if _instance := [i for i in self.instances if i.name == data["name"]]:
            instance = _instance[0]
        else:
            instance = Instance(
                data["name"],
                hostname=data["hostname"],
                port=data["port"],
            )
            self.instances.add(instance)
            self.bot.logger.info(
                "[Manager] Creating unknown instance '%s'", data["name"]
            )

        instance.alive = data["alive"]
        instance.ping = data["ping"]

        return instance, request, data

    # =========================================================================
    # =========================================================================

    def forge_payload(
        self, request: str, data: dict, auth: bool = True
    ) -> dict:
        """Forge json payload"""
        payload = {"request": request, "data": data}

        if auth:
            payload["__token"] = self.bot.http.token

        return payload
