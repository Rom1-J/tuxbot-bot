import asyncio
import functools
import logging
import time
from typing import Union

import aiohttp
import discord
from aiohttp import ClientConnectorError
from discord.ext import commands
from ipinfo.exceptions import RequestQuotaExceededError
from structured_config import ConfigFile
from tuxbot.cogs.Network.functions.converters import (
    IPConverter,
    IPVersionConverter,
    IPCheckerConverter,
    DomainCheckerConverter,
    QueryTypeConverter,
)
from tuxbot.cogs.Network.functions.exceptions import (
    RFC18,
    InvalidIp,
    VersionNotFound,
    InvalidDomain,
    InvalidQueryType,
)
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.data_manager import cogs_data_path
from tuxbot.core.utils.functions.extra import (
    ContextPlus,
    command_extra,
)
from tuxbot.core.utils.functions.utils import shorten
from .config import NetworkConfig
from .functions.utils import (
    get_ip,
    get_hostname,
    get_ipinfo_result,
    get_ipwhois_result,
    merge_ipinfo_ipwhois,
    get_pydig_result,
)

log = logging.getLogger("tuxbot.cogs.Network")
_ = Translator("Network", __file__)


class Network(commands.Cog, name="Network"):
    _tmp: discord.Message

    def __init__(self, bot: Tux):
        self.bot = bot
        self.__config: NetworkConfig = ConfigFile(
            str(
                cogs_data_path(self.bot.instance_name, "Network")
                / "config.yaml"
            ),
            NetworkConfig,
        ).config

    async def cog_command_error(self, ctx, error):
        if isinstance(
            error,
            (
                RequestQuotaExceededError,
                RFC18,
                InvalidIp,
                InvalidDomain,
                InvalidQueryType,
                VersionNotFound,
            ),
        ):
            if self._tmp:
                await self._tmp.delete()

            await ctx.send(_(str(error), ctx, self.bot.config))

    # =========================================================================
    # =========================================================================

    @command_extra(name="iplocalise", aliases=["localiseip"], deletable=True)
    async def _iplocalise(
        self,
        ctx: ContextPlus,
        ip: IPConverter,
        version: IPVersionConverter = "",
    ):
        self._tmp = await ctx.send(
            _("*Retrieving information...*", ctx, self.bot.config),
            deletable=False,
        )

        ip_address = await get_ip(str(ip), str(version))
        ip_hostname = get_hostname(ip_address)

        ipinfo_result = await get_ipinfo_result(
            self.__config.ipinfoKey, ip_address
        )
        ipwhois_result = await self.bot.loop.run_in_executor(
            None, functools.partial(get_ipwhois_result, ip_address)
        )

        merged_results = merge_ipinfo_ipwhois(ipinfo_result, ipwhois_result)

        e = discord.Embed(
            title=_(
                "Information for ``{ip} ({ip_address})``", ctx, self.bot.config
            ).format(ip=ip, ip_address=ip_address),
            color=0x5858D7,
        )

        e.add_field(
            name=_("Belongs to:", ctx, self.bot.config),
            value=merged_results["belongs"],
            inline=True,
        )
        e.add_field(
            name="RIR :",
            value=merged_results["rir"],
            inline=True,
        )
        e.add_field(
            name=_("Region:", ctx, self.bot.config),
            value=merged_results["region"],
            inline=False,
        )

        e.set_thumbnail(url=merged_results["flag"])

        e.set_footer(
            text=_("Hostname: {hostname}", ctx, self.bot.config).format(
                hostname=ip_hostname
            ),
        )

        await self._tmp.delete()
        await ctx.send(embed=e)

    @command_extra(name="getheaders", aliases=["headers"], deletable=True)
    async def _getheaders(
        self, ctx: ContextPlus, ip: IPCheckerConverter, *, user_agent: str = ""
    ):
        try:
            headers = {"User-Agent": user_agent}
            colors = {
                "1": 0x17A2B8,
                "2": 0x28A745,
                "3": 0xFFC107,
                "4": 0xDC3545,
                "5": 0x343A40,
            }

            async with ctx.session.get(
                str(ip),
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=4),
            ) as s:
                e = discord.Embed(
                    title=f"Headers : {ip}",
                    color=colors.get(str(s.status)[0], 0x6C757D),
                )
                e.add_field(
                    name="Status", value=f"```{s.status}```", inline=True
                )
                e.set_thumbnail(url=f"https://http.cat/{s.status}")

                headers = dict(s.headers.items())
                headers.pop("Set-Cookie", headers)

                for key, value in headers.items():
                    output = await shorten(ctx, value, 50)

                    if output["link"] is not None:
                        value = _(
                            "[show all]({})", ctx, self.bot.config
                        ).format(output["link"])
                    else:
                        value = f"```\n{output['text']}```"

                    e.add_field(name=key, value=value, inline=True)

                await ctx.send(embed=e)
        except (ClientConnectorError, asyncio.exceptions.TimeoutError):
            await ctx.send(
                _("Cannot connect to host {}", ctx, self.bot.config).format(ip)
            )

    @command_extra(name="dig", deletable=True)
    async def _dig(
        self,
        ctx: ContextPlus,
        domain: DomainCheckerConverter,
        query_type: QueryTypeConverter,
        dnssec: Union[str, bool] = False,
    ):
        pydig_result = await self.bot.loop.run_in_executor(
            None,
            functools.partial(get_pydig_result, domain, query_type, dnssec),
        )

        e = discord.Embed(title=f"DIG {domain} {query_type}", color=0x5858D7)

        for value in pydig_result:
            e.add_field(
                name=f"DIG {domain} IN {query_type}", value=f"```{value}```"
            )

        if not pydig_result:
            e.add_field(
                name=f"DIG {domain} IN {query_type}",
                value=_("No result...", ctx, self.bot.config),
            )

        await ctx.send(embed=e)

    @command_extra(name="ping", deletable=True)
    async def _ping(self, ctx: ContextPlus):
        start = time.perf_counter()
        await ctx.trigger_typing()
        end = time.perf_counter()

        latency = round(self.bot.latency * 1000, 2)
        typing = round((end - start) * 1000, 2)

        e = discord.Embed(title="Ping", color=discord.Color.teal())
        e.add_field(name="Websocket", value=f"{latency}ms")
        e.add_field(name="Typing", value=f"{typing}ms")
        await ctx.send(embed=e)
