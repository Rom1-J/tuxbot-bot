import functools
import logging


import discord

from discord.ext import commands
from ipinfo.exceptions import RequestQuotaExceededError

from structured_config import ConfigFile

from tuxbot.cogs.Network.functions.converters import (
    IPConverter,
    IPVersionConverter,
)
from tuxbot.cogs.Network.functions.exceptions import (
    RFC18,
    InvalidIp,
    VersionNotFound,
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
from .config import NetworkConfig
from .functions.utils import (
    get_ip,
    get_hostname,
    get_ipinfo_result,
    get_ipwhois_result,
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
            (RequestQuotaExceededError, RFC18, InvalidIp, VersionNotFound),
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

            if ipwhois_result:
                e.add_field(
                    name="RIR :",
                    value=f"```{ipwhois_result['asn_registry']}```",
                    inline=True,
                )

            e.add_field(
                name=_("Region:", ctx, self.bot.config),
                value=f"```{ipinfo_result.get('city', 'N/A')} - "
                f"{ipinfo_result.get('region', 'N/A')} "
                f"({ipinfo_result.get('country', 'N/A')})```",
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
                name="RIR :",
                value=f"```{ipwhois_result['asn_registry']}```",
                inline=True,
            )

            e.add_field(
                name=_("Region:", ctx, self.bot.config),
                value=f"```{asn_country}```",
                inline=False,
            )

            e.set_thumbnail(
                url=f"https://www.countryflags.io/{asn_country}/shiny/64.png"
            )

        e.set_footer(
            text=_("Hostname: {hostname}", ctx, self.bot.config).format(
                hostname=ip_hostname
            ),
        )

        await self._tmp.delete()
        await ctx.send(embed=e)
