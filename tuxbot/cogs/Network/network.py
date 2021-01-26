import functools
import logging
import discord
from aiohttp import ClientConnectorError
from discord.ext import commands
from ipinfo.exceptions import RequestQuotaExceededError
from structured_config import ConfigFile
from tuxbot.cogs.Network.functions.converters import (
    IPConverter,
    IPVersionConverter,
    IPCheckerConverter,
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
from tuxbot.core.utils.functions.utils import shorten
from .config import NetworkConfig
from .functions.utils import (
    get_ip,
    get_hostname,
    get_ipinfo_result,
    get_ipwhois_result,
    merge_ipinfo_ipwhois,
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

            async with ctx.session.get(str(ip), headers=headers) as s:
                e = discord.Embed(title=f"Headers : {ip}", color=0xD75858)
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
                        value = f"```{output['text']}```"

                    e.add_field(name=key, value=value, inline=True)

                await ctx.send(embed=e, deletable=False)
        except ClientConnectorError:
            await ctx.send(
                _("Cannot connect to host {}", ctx, self.bot.config).format(ip)
            )
