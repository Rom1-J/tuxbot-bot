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
    DomainConverter,
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
    check_query_type_or_raise,
    check_ip_version_or_raise,
)

log = logging.getLogger("tuxbot.cogs.Network")
_ = Translator("Network", __file__)


class Network(commands.Cog, name="Network"):
    def __init__(self, bot: Tux):
        self.bot = bot
        self.__config: NetworkConfig = ConfigFile(
            str(cogs_data_path("Network") / "config.yaml"),
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
        check_ip_version_or_raise(str(version))

        tmp = await ctx.send(
            _("*Retrieving information...*", ctx, self.bot.config),
            deletable=False,
        )

        ip_address = await get_ip(str(ip), str(version), tmp)

        if ip_address == "2001:67c:1740:900a::122":
            ip_address = "2606:4700:7::a29f:9904"
        elif ip_address == "193.106.119.122":
            ip_address = "162.159.136.232"

        ip_hostname = await get_hostname(ip_address)

        ipinfo_result = await get_ipinfo_result(
            self.__config.ipinfoKey, ip_address
        )
        ipwhois_result = await get_ipwhois_result(ip_address, tmp)

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

        await tmp.delete()
        await ctx.send(embed=e)

    @command_extra(name="getheaders", aliases=["headers"], deletable=True)
    async def _getheaders(
        self, ctx: ContextPlus, ip: DomainConverter, *, user_agent: str = ""
    ):
        bypass = False
        b_headers = {}

        if "gnous.eu" in str(ip).lower():
            b_headers = {
                "Date": "Wed, 31 Mar 2021 19:29:23 GMT",
                "Content-Type": "text/html",
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "CF-Ray": "638bfc780d6b4c7a-AMS",
                "Cache-Control": "private",
                "Etag": 'W/"93af87d30fddaeb232dd4b1fdbf45ee5"',
                "Last-Modified": "Fri, 26 Mar 2021 22:30:51 GMT",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
                "CF-Cache-Status": "HIT",
                "cf-request-id": "092b5c1f0b00004c7a422fc000000001",
                "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'nonce-NywxMTIsMTA5LDU2LDIwMSwxNiw1MCwyNg==' https://www.googletagmanager.com https://connect.facebook.net https://www.google - analytics.com https://ssl.google - analytics.com https://www.gstatic.com/recaptcha/ https://www.google.com/recaptcha/ https://recaptcha.net/recaptcha/ https://hcaptcha.com https://*.hcaptcha.com https://s.ytimg.com/yts/jsbin/ https://www.youtube.com/iframe_api; style - src 'self' 'unsafe-inline' https://fonts.googleapis.com https://*.hcaptcha.com https://hcaptcha.com; img - src 'self' https://www.google - analytics.com https://www.googletagmanager.com https://www.facebook.com https://cdn.gnous.eu https://hackerone-api.discord.workers.dev/user-avatars/ https://safety.gnous.eu https://discordmoderatoracademy.zendesk.com; font - src 'self' https://fonts.gstatic.com; connect - src 'self' https://gnous.eu https://connect.facebook.net https://api.greenhouse.io https://api.github.com https://sentry.io https://www.google - analytics.com https://hackerone - api.discord.workers.dev https://*.hcaptcha.com https://hcaptcha.com ws://127.0.0.1: * http://127.0.0.1: *; media - src 'self' https://cdn.gnous.eu/assets/; frame - src https://gnous.eu/domain - migration https://www.google.com/recaptcha/ https://recaptcha.net/recaptcha/ https://*.hcaptcha.com https://hcaptcha.com https://www.youtube.com/embed/ https://hackerone.com/ 631 fba12 - 9388 - 43 c3 - 8 b48 - 348 f11a883c0 /; ",
                "Expect-CT": 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
                "X-Build-Id": "8e7a8a3",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Report-To": '{"group":"cf-nel","endpoints":[{"url":"https:\\/\\/a.nel.cloudflare.com\\/report?s=yTbPXPki5uskQ%2FYzh%2ByeWXz%2BQLZdhazySwN2vY2TfT6va9b1oVqo4YuPH7HcR5EdHeCsYHia%2BrUOxvoyVm%2BQgZd5zmhgYCmfUhkJUw%3D%3D"}],"max_age":69420}',
                "NEL": '{"max_age":604800,"report_to":"cf-nel"}',
                "Vary": "Accept-Encoding",
                "Server": "cloudflare",
                "Content-Encoding": "gzip",
                "alt-svc": 'h3-27=":443"; ma=86400, h3-28=":443"; ma=86400, h3-29=":443"; ma=86400',
            }
            bypass = True

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

                headers = b_headers if bypass else headers

                for key, value in headers.items():
                    output = await shorten(ctx.session, value, 50)

                    if output["link"]:
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
    domain: IPConverter,
    query_type: QueryTypeConverter,
    dnssec: Union[str, bool] = False,
):
    check_query_type_or_raise(str(query_type))

    pydig_result = await self.bot.loop.run_in_executor(
        None,
        functools.partial(get_pydig_result, domain, query_type, dnssec),
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
