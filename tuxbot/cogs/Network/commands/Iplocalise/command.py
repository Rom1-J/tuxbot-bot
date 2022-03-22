"""
tuxbot.cogs.Network.commands.Iplocalise.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows information about given ip/domain
"""

import asyncio
import socket
from typing import Optional, Union

import yaml
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .converters.InetConverter import InetConverter
from .converters.IPConverter import IPConverter
from .exceptions import VersionNotFound
from .providers.base import get_all_providers
from .ui.view import ViewController


class IplocaliseCommand(commands.Cog):
    """Shows information about given ip/domain"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_ip(ip: str, inet: Optional[int]) -> str:
        """Get ip from domain"""

        _inet: Union[
            socket.AddressFamily, int  # pylint: disable=no-member
        ] = 0

        if inet:
            _inet = socket.AF_INET6 if inet == 6 else socket.AF_INET

        def _get_ip(_ip: str):
            try:
                return socket.getaddrinfo(_ip, None, _inet)[1][4][0]
            except (socket.gaierror, UnicodeError) as e:
                raise VersionNotFound(
                    "Unable to collect information on this in the "
                    "given version"
                ) from e

        return await asyncio.get_running_loop().run_in_executor(
            None, _get_ip, str(ip)
        )

    # =========================================================================
    # =========================================================================

    @commands.command(name="iplocalise", aliases=["localiseip", "ipl"])
    async def _iplocalise(
        self,
        ctx: commands.Context,
        domain: IPConverter,
        inet: InetConverter = None,
    ):
        if ip := await self.bot.redis.get(self.bot.utils.gen_key(str(domain))):
            ip = ip.decode()
        else:
            ip = await self.__get_ip(str(domain), inet)

            await self.bot.redis.set(
                self.bot.utils.gen_key(str(domain)), str(ip), ex=3600 * 24
            )

        if result := await self.bot.redis.get(
            self.bot.utils.gen_key(f"{domain}+{ip}")
        ):
            result = yaml.load(result, Loader=yaml.Loader)
        else:
            result = await get_all_providers(
                self.bot.config["Network"], data={"ip": ip, "domain": domain}
            )

            await self.bot.redis.set(
                self.bot.utils.gen_key(f"{domain}+{ip}"), str(result)
            )

        controller = ViewController(ctx=ctx, data=result)

        await controller.send()
