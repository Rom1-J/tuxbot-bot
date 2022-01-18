"""
tuxbot.cogs.Network.commands.Iplocalise.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows information about given ip/domain
"""

import yaml
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .converters.IPConverter import IPConverter
from .converters.InetConverter import InetConverter

from .providers.base import get_all_providers
from .ui.view import ViewController
from .utils import get_ip


class IplocaliseCommand(commands.Cog):
    """Shows information about given ip/domain"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="iplocalise", aliases=["localiseip", "ipl"])
    async def _iplocalise(
        self,
        ctx: commands.Context,
        domain: IPConverter,
        inet: InetConverter = None,
    ):
        ip = await self.bot.redis.get(self.bot.utils.gen_key(str(domain)))

        if not ip:
            ip = await get_ip(self.bot.loop, str(domain), inet)

            await self.bot.redis.set(
                self.bot.utils.gen_key(str(domain)), str(ip), ex=3600 * 24
            )
        else:
            ip = ip.decode()

        result = await self.bot.redis.get(
            self.bot.utils.gen_key(f"{domain}+{ip}")
        )

        if not result:
            result = await get_all_providers(
                self.bot.config["Network"], data={"ip": ip, "domain": domain}
            )

            await self.bot.redis.set(
                self.bot.utils.gen_key(f"{domain}+{ip}"), str(result)
            )
        else:
            result = yaml.load(result, Loader=yaml.Loader)

        controller = ViewController(ctx=ctx, author=ctx.author, data=result)

        await controller.send()
