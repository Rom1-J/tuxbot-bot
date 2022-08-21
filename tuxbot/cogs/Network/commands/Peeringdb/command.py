"""
tuxbot.cogs.Network.commands.Peeringdb.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows information from peeringdb about an ASN
"""

import asyncio
import typing
from datetime import datetime

import aiohttp
import discord
from aiohttp import TCPConnector
from discord.ext import commands, tasks

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from .converters.ASConverter import ASConverter
from .exceptions import InvalidAsn


class PeeringdbCommand(commands.Cog):
    """Shows information about given ASN"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        self._peeringdb_net = None
        self._update_peering_db.start()  # pylint: disable=no-member

    # =========================================================================

    async def cog_unload(self) -> None:
        """Stop task updater"""
        self.bot.logger.info(
            "[PeeringdbCommand] Canceling '_update_peering_db'"
        )
        self._update_peering_db.cancel()  # pylint: disable=no-member

    # =========================================================================
    # =========================================================================

    @staticmethod
    def __check_asn_or_raise(asn: str) -> bool | typing.NoReturn:
        """Validate asn format"""

        if asn.isdigit() and int(asn) < 4_294_967_295:
            return True

        raise InvalidAsn("Invalid ASN provided")

    # =========================================================================
    # =========================================================================

    @tasks.loop(hours=6.00)
    async def _update_peering_db(self) -> None:
        headers = {}
        if key := self.bot.config["Network"].get("peeringdb_key"):
            headers["Authorization"] = f"Api-Key {key}"

        try:
            async with aiohttp.ClientSession(
                connector=TCPConnector(verify_ssl=False)
            ) as cs, cs.get(
                "https://peeringdb.com/api/net",
                timeout=aiohttp.ClientTimeout(total=60),
                headers=headers,
            ) as s:
                self._peeringdb_net = await s.json()
        except asyncio.exceptions.TimeoutError:
            self.bot.logger.error(
                "[PeeringdbCommand] '_update_peering_db' failed!"
            )
        else:
            self.bot.logger.info(
                "[PeeringdbCommand] '_update_peering_db' done!"
            )

    # =========================================================================
    # =========================================================================

    @commands.command(name="peeringdb", aliases=["peer", "peering"])
    async def _peeringdb(
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> None:
        if (
            # pylint: disable=no-member
            not self._update_peering_db.is_running()
        ):
            self._peeringdb_net = None
            self._update_peering_db.start()  # pylint: disable=no-member

        asn = await ASConverter().convert(ctx, argument)
        self.__check_asn_or_raise(asn)

        data: dict[str, typing.Any] = {}

        self.bot.logger.debug(self._peeringdb_net)

        if self._peeringdb_net is None or not self._peeringdb_net.get("data"):
            await ctx.send("Please retry in few seconds.")
            return

        for _data in self._peeringdb_net["data"]:
            if _data.get("asn", None) == int(str(asn)):
                data = _data
                break

        if not data:
            await ctx.send(
                f"AS{asn} could not be found in PeeringDB's database."
            )
            return

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
            title=f"{data['name']} ({data.get('aka') or f'AS{asn}'})",
            color=0x5858D7,
        )

        for key, name in filtered.items():
            e.add_field(name=name, value=f"```{data.get(key) or 'N/A'}```")

        for key, names in filtered_link.items():
            if data.get(key):
                e.add_field(
                    name=names[0],
                    value=f"[{data.get(key) or 'N/A'}]"
                    f"({data.get(names[1]) or 'N/A'})",
                )

        if data["notes"]:
            output = await self.bot.utils.shorten(data["notes"], 550)
            e.description = output["text"]
        if data["created"]:
            e.timestamp = datetime.strptime(
                data["created"], "%Y-%m-%dT%H:%M:%SZ"
            )

        await ctx.send(f"https://www.peeringdb.com/net/{data['id']}", embed=e)
