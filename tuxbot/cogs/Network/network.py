import asyncio
import logging
import time
from datetime import datetime
from typing import Optional

import aiohttp
import discord
from aiohttp import ClientConnectorError, InvalidURL
from jishaku.models import copy_context_with
from discord.ext import commands, tasks
from ipinfo.exceptions import RequestQuotaExceededError
from structured_config import ConfigFile
from tuxbot.cogs.Network.functions.converters import (
    IPConverter,
    IPParamsConverter,
    DomainConverter,
    QueryTypeConverter,
    ASConverter,
)
from tuxbot.cogs.Network.functions.exceptions import (
    RFC18,
    InvalidIp,
    VersionNotFound,
    InvalidDomain,
    InvalidQueryType,
    InvalidAsn,
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
from tuxbot.core.utils.functions.utils import shorten, str_if_empty
from .config import NetworkConfig
from .functions.utils import (
    get_ip,
    get_hostname,
    get_crimeflare_result,
    get_ipinfo_result,
    get_ipwhois_result,
    get_map_bytes,
    get_pydig_result,
    get_peeringdb_net_result,
    merge_ipinfo_ipwhois,
    check_query_type_or_raise,
    check_ip_version_or_raise,
    check_asn_or_raise,
)

log = logging.getLogger("tuxbot.cogs.Network")
_ = Translator("Network", __file__)


class Network(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot
        self.__config: NetworkConfig = ConfigFile(
            str(cogs_data_path("Network") / "config.yaml"),
            NetworkConfig,
        ).config
        self._update_peering_db.start()  # pylint: disable=no-member

    async def cog_command_error(self, ctx: ContextPlus, error):
        if isinstance(
            error,
            (
                RequestQuotaExceededError,
                RFC18,
                InvalidIp,
                InvalidDomain,
                InvalidQueryType,
                VersionNotFound,
                InvalidAsn,
            ),
        ):
            await ctx.send(_(str(error), ctx, self.bot.config))

    async def cog_before_invoke(self, ctx: ContextPlus):
        await ctx.trigger_typing()

    def cog_unload(self):
        self._update_peering_db.cancel()  # pylint: disable=no-member

    @tasks.loop(hours=24.0)
    async def _update_peering_db(self):
        await get_peeringdb_net_result(str(1))

        log.log(logging.INFO, "_update_peering_db")
        self.bot.console.log("[Network]: _update_peering_db")

    # =========================================================================
    # =========================================================================

    @command_extra(name="iplocalise", aliases=["localiseip"], deletable=True)
    async def _iplocalise(
        self,
        ctx: ContextPlus,
        ip: IPConverter,
        *,
        params: Optional[IPParamsConverter] = None,
    ):
        # noinspection PyUnresolvedReferences
        check_ip_version_or_raise(params)  # type: ignore

        # noinspection PyUnresolvedReferences
        ip_address = await get_ip(
            self.bot.loop, str(ip), params  # type: ignore
        )

        ip_hostname = await get_hostname(self.bot.loop, str(ip_address))

        ipinfo_result = await get_ipinfo_result(
            self.__config.ipinfoKey, ip_address
        )
        ipwhois_result = await get_ipwhois_result(self.bot.loop, ip_address)

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

        kwargs: dict = {}

        # noinspection PyUnresolvedReferences
        if (
            params is not None
            and params["map"]
            and (  # type: ignore
                map_bytes := await get_map_bytes(
                    self.__config.geoapifyKey, merged_results["map"]
                )
            )
        ):
            file = discord.File(map_bytes, "map.png")
            e.set_image(url="attachment://map.png")

            kwargs["file"] = file

        kwargs["embed"] = e

        return await ctx.send(f"https://ipinfo.io/[{ip_address}]", **kwargs)

    @command_extra(
        name="cloudflare", aliases=["cf", "crimeflare"], deletable=True
    )
    async def _cloudflare(
        self,
        ctx: ContextPlus,
        ip: DomainConverter,
    ):
        crimeflare_result = await get_crimeflare_result(str(ip))

        if crimeflare_result:
            alt_ctx = await copy_context_with(
                ctx, content=f"{ctx.prefix}iplocalise {crimeflare_result}"
            )
            return await alt_ctx.command.reinvoke(alt_ctx)

        await ctx.send(
            _(
                "Unable to collect information through CloudFlare",
                ctx,
                self.bot.config,
            )
        )

    @command_extra(name="getheaders", aliases=["headers"], deletable=True)
    async def _getheaders(
        self, ctx: ContextPlus, ip: DomainConverter, *, user_agent: str = ""
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

            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                    str(ip),
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=8),
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

                    fail = False

                    for key, value in headers.items():
                        fail, output = await shorten(value, 50, fail)

                        if output["link"]:
                            value = _(
                                "[show all]({})", ctx, self.bot.config
                            ).format(output["link"])
                        else:
                            value = f"```\n{output['text']}```"

                        e.add_field(name=key, value=value, inline=True)

                    await ctx.send(embed=e)
        except (
            ClientConnectorError,
            InvalidURL,
            asyncio.exceptions.TimeoutError,
        ):
            await ctx.send(
                _("Cannot connect to host {}", ctx, self.bot.config).format(ip)
            )

    @command_extra(name="dig", deletable=True)
    async def _dig(
        self,
        ctx: ContextPlus,
        domain: IPConverter,
        query_type: QueryTypeConverter,
        dnssec: str | bool = False,
    ):
        check_query_type_or_raise(str(query_type))

        pydig_result = await get_pydig_result(
            self.bot.loop, str(domain), str(query_type), dnssec
        )

        e = discord.Embed(title=f"DIG {domain} {query_type}", color=0x5858D7)

        for i, value in enumerate(pydig_result):
            e.add_field(name=f"#{i}", value=f"```{value}```")

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

    @command_extra(name="isdown", aliases=["is_down", "down?"], deletable=True)
    async def _isdown(self, ctx: ContextPlus, domain: IPConverter):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                    f"https://isitdown.site/api/v3/{domain}",
                    timeout=aiohttp.ClientTimeout(total=8),
                ) as s:
                    json = await s.json()

                    if json["isitdown"]:
                        title = _("Down...", ctx, self.bot.config)
                        color = 0xDC3545
                    else:
                        title = _("Up!", ctx, self.bot.config)
                        color = 0x28A745

                    e = discord.Embed(title=title, color=color)
                    e.set_thumbnail(
                        url=f"https://http.cat/{json['response_code']}"
                    )

                    await ctx.send(embed=e)

        except (
            ClientConnectorError,
            InvalidURL,
            asyncio.exceptions.TimeoutError,
        ):
            await ctx.send(
                _("Cannot connect to host {}", ctx, self.bot.config).format(
                    domain
                )
            )

    @command_extra(
        name="peeringdb", aliases=["peer", "peering"], deletable=True
    )
    async def _peeringdb(self, ctx: ContextPlus, asn: ASConverter):
        check_asn_or_raise(str(asn))

        data: dict = (await get_peeringdb_net_result(str(asn)))["data"]

        if not data:
            return await ctx.send(
                _(
                    "AS{asn} could not be found in PeeringDB's database.",
                    ctx,
                    self.bot.config,
                ).format(asn=asn)
            )

        data = data[0]

        filtered = {
            "info_type": "Type",
            "info_traffic": "Traffic",
            "info_ratio": "Ratio",
            "info_prefixes4": "Prefixes IPv4",
            "info_prefixes6": "Prefixes IPv6",
        }
        filtered_link = {
            "website": ("Site", "website"),
            "looking_glass": ("Looking Glass", "looking_glass"),
            "policy_general": ("Peering", "policy_url"),
        }

        e = discord.Embed(
            title=f"{data['name']} ({str_if_empty(data['aka'], f'AS{asn}')})",
            color=0x5858D7,
        )

        for key, name in filtered.items():
            e.add_field(
                name=name, value=f"```{str_if_empty(data.get(key), 'N/A')}```"
            )

        for key, names in filtered_link.items():
            if data.get(key):
                e.add_field(
                    name=names[0],
                    value=f"[{str_if_empty(data.get(key), 'N/A')}]"
                    f"({str_if_empty(data.get(names[1]), 'N/A')})",
                )

        if data["notes"]:
            output = (await shorten(data["notes"], 550))[1]
            e.description = output["text"]
        if data["created"]:
            e.timestamp = datetime.strptime(
                data["created"], "%Y-%m-%dT%H:%M:%SZ"
            )

        await ctx.send(f"https://www.peeringdb.com/net/{data['id']}", embed=e)
