import functools
import logging
import socket
from typing import Union, NoReturn

import discord
import ipinfo
import ipwhois
from discord.ext import commands
from ipinfo.exceptions import RequestQuotaExceededError
from ipwhois import Net
from ipwhois.asn import IPASN
from structured_config import ConfigFile

from tuxbot.cogs.Network.functions.converters import (
    IPConverter,
    IPVersionConverter,
)
from tuxbot.cogs.Network.functions.exceptions import RFC18, InvalidIp
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.data_manager import cogs_data_path
from tuxbot.core.utils.functions.extra import (
    ContextPlus,
    command_extra,
)
from .config import NetworkConfig

log = logging.getLogger("tuxbot.cogs.Network")
_ = Translator("Network", __file__)


class Network(commands.Cog, name="Network"):
    def __init__(self, bot: Tux):
        self.bot = bot
        self.config: NetworkConfig = ConfigFile(
            str(
                cogs_data_path(self.bot.instance_name, "Network")
                / "config.yaml"
            ),
            NetworkConfig,
        ).config

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (RequestQuotaExceededError, RFC18, InvalidIp)):
            await ctx.send(_(str(error), ctx, self.bot.config))

    # =========================================================================
    # =========================================================================

    async def _get_ip(self, ctx: ContextPlus, ip: str, inet: str = "") -> str:
        inet_text = ""

        if inet == "6":
            inet = socket.AF_INET6
            inet_text = _("in v{v}", ctx, self.bot.config).format(v=inet)
        elif inet == "4":
            inet = socket.AF_INET
            inet_text = _("in v{v}", ctx, self.bot.config).format(v=inet)
        else:
            inet = 0

        try:
            return socket.getaddrinfo(str(ip), None, inet)[1][4][0]
        except socket.gaierror:
            return await ctx.send(
                _(
                    "Impossible to collect information on this ip {version}".format(
                        version=inet_text
                    ),
                    ctx,
                    self.bot.config,
                )
            )

    @staticmethod
    def _get_hostname(ip: str) -> str:
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return "N/A"

    @staticmethod
    def get_ipwhois_result(ip_address: str) -> Union[NoReturn, dict]:
        try:
            net = Net(ip_address)
            obj = IPASN(net)
            return obj.lookup()
        except ipwhois.exceptions.ASNRegistryError:
            return {}
        except ipwhois.exceptions.IPDefinedError as e:

            def _(x):
                return x

            raise RFC18(
                _(
                    "IP address {ip_address} is already defined as Private-Use"
                    " Networks via RFC 1918."
                )
            ) from e

    async def get_ipinfo_result(
        self, ip_address: str
    ) -> Union[NoReturn, dict]:
        try:
            handler = ipinfo.getHandlerAsync(self.config.ipinfoKey)
            return (await handler.getDetails(ip_address)).all
        except RequestQuotaExceededError:
            return {}

    # =========================================================================
    # =========================================================================

    @command_extra(name="iplocalise", aliases=["localiseip"], deletable=True)
    async def _iplocalise(
        self,
        ctx: ContextPlus,
        ip: IPConverter,
        version: IPVersionConverter = "",
    ):
        tmp = await ctx.send(
            _("*Retrieving information...*", ctx, self.bot.config),
            deletable=False,
        )

        ip_address = await self._get_ip(ctx, str(ip), str(version))
        ip_hostname = self._get_hostname(ip_address)

        ipinfo_result = await self.get_ipinfo_result(ip_address)
        ipwhois_result = await self.bot.loop.run_in_executor(
            None, functools.partial(self.get_ipwhois_result, ip_address)
        )

        e = discord.Embed(
            title=_(
                "Information for ``{ip} ({ip_address})``", ctx, self.bot.config
            ).format(ip=ip, ip_address=ip_address),
            color=0x5858D7,
        )

        if ipinfo_result:
            org = ipinfo_result.get("org", "")
            asn = org.split()[0]

            e.add_field(
                name=_("Belongs to:", ctx, self.bot.config),
                value=f"[{org}](https://bgp.he.net/{asn})",
                inline=True,
            )

            e.add_field(
                name=_("Region:", ctx, self.bot.config),
                value=f"{ipinfo_result.get('city', 'N/A')} - "
                f"{ipinfo_result.get('region', 'N/A')} "
                f"({ipinfo_result.get('country', 'N/A')})",
                inline=False,
            )

            e.set_thumbnail(
                url=f"https://www.countryflags.io/{ipinfo_result['country']}"
                f"/shiny/64.png"
            )
        elif ipwhois_result:
            org = ipwhois_result.get("asn_description", "N/A")
            asn = ipwhois_result.get("asn", "N/A")
            asn_country = ipwhois_result.get("asn_country_code", "N/A")

            e.add_field(
                name=_("Belongs to:", ctx, self.bot.config),
                value=f"{org} ([AS{asn}](https://bgp.he.net/{asn}))",
                inline=True,
            )

            e.add_field(
                name=_("Region:", ctx, self.bot.config),
                value=asn_country,
                inline=False,
            )

            e.set_thumbnail(
                url=f"https://www.countryflags.io/{asn_country}/shiny/64.png"
            )

        if ipwhois_result:
            e.add_field(
                name="RIR :", value=ipwhois_result["asn_registry"], inline=True
            )

        e.set_footer(
            text=_("Hostname: {hostname}", ctx, self.bot.config).format(
                hostname=ip_hostname
            ),
        )

        await tmp.delete()
        await ctx.send(embed=e)
