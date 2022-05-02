"""
tuxbot.cogs.Network.commands.Iplocalise.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows information about given ip/domain
"""

import asyncio
import json
import socket
from typing import Optional, Tuple

from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .converters.InetConverter import InetConverter
from .converters.IPConverter import IPConverter
from .exceptions import VersionNotFound
from .ui.ViewController import ViewController


class IplocaliseCommand(commands.Cog):
    """Shows information about given ip/domain"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_ip(
            ip: str, inet: Optional[int]
    ) -> str:
        """Get ip from domain"""

        throwable = VersionNotFound(
            "Unable to collect information on this in the "
            "given version"
        )

        def _get_ip(_ip: str):
            try:
                key = -1
                kwargs = {}

                if inet == 4:
                    key = 1
                elif inet == 6:
                    kwargs["family"] = socket.AF_INET6

                addr = socket.getaddrinfo(_ip, None, **kwargs)[key][4][0]
                return addr
            except (socket.gaierror, UnicodeError):
                raise throwable

        try:
            return await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_ip, str(ip)
                ),
                timeout=2,
            )
        except asyncio.exceptions.TimeoutError:
            raise throwable

    # =========================================================================
    # =========================================================================

    @commands.command(name="iplocalise", aliases=["localiseip", "ipl"])
    async def _iplocalise(
            self,
            ctx: commands.Context,
            domain: IPConverter,
            inet: InetConverter = None,
    ):
        cache_key = self.bot.utils.gen_key(str(domain), str(inet))

        if data := await self.bot.redis.get(cache_key):
            ip = json.loads(data)
        else:
            ip = await self.__get_ip(str(domain), inet)

            await self.bot.redis.set(
                cache_key, json.dumps(ip), ex=3600
            )
        await ViewController(
            ctx=ctx,
            config=self.bot.config["Network"],
            data={"ip": ip, "domain": domain}
        ).send()
